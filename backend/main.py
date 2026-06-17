
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from game_logic import GameStateManager
from ai_handler import generate_gm_response
import json

app = FastAPI()

game_state = GameStateManager()
chat_history = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5176"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

    async def send_player_data(self, client_id: str, player_data: dict):
        websocket = self.active_connections.get(client_id)
        if websocket:
            await websocket.send_json({"sender": "PlayerData", "content": player_data})

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()

            player_name = game_state.get_player_name(client_id) or "User"
            user_message = {"sender": player_name, "content": data}
            await manager.broadcast(user_message)

            response_message = None
            if data.startswith("/"):
                system_msg, hidden_prompt, should_trigger_ai = game_state.process_command(client_id, data)
                if system_msg:
                    response_message = {"sender": "System", "content": system_msg}
                    await manager.broadcast(response_message)
                if hidden_prompt:
                    chat_history.append({"sender": "System", "content": hidden_prompt})
                if data.lower().startswith("/role"):
                    player_data = game_state.get_player_data(client_id)
                    if player_data:
                        await manager.send_player_data(client_id, player_data)

            else:
                should_trigger_ai = True
                chat_history.append(user_message)

            if should_trigger_ai:
                try:
                    gm_text = await generate_gm_response(chat_history)
                    gm_response, player_data, image_url = game_state.process_ai_response(gm_text, game_state.get_player_data(client_id))
                    
                    gm_message = {"sender": "Athena (GM)", "content": gm_response, "imageUrl": image_url}
                    chat_history.append(gm_message)
                    await manager.broadcast(gm_message)

                    if player_data:
                        await manager.send_player_data(client_id, player_data)

                except Exception as e:
                    error_message = {"sender": "Athena (GM)", "content": f"[System Error: Cannot connect to local AI instance. Is it running? Details: {e}]"}
                    await manager.broadcast(error_message)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
