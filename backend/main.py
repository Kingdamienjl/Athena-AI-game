
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from game_logic import GameStateManager
from ai_handler import get_ai_response # <-- Import the new RAG function

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173", "http://127.0.0.1:5173",
    "http://localhost:5174", "http://127.0.0.1:5174",
    "http://localhost:5176", "http://127.0.0.1:5176",
    # Add any other ports you might use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_state = GameStateManager()

class ActionRequest(BaseModel):
    action_text: str
    client_id: str

@app.post("/api/take_action")
async def take_action(request: ActionRequest):
    action_str = request.action_text.strip()

    # Handle /role command
    if action_str.startswith("/role "):
        if game_state.get_player_data(request.client_id):
            return {
                "speaker": "System",
                "dialogue": "Role selection is locked. Start a new session to change characters.",
                "player_data": game_state.get_player_data(request.client_id)
            }
        
        target_role = action_str.replace("/role ", "").strip()
        game_state.assign_role(request.client_id, target_role)
        player_data = game_state.get_player_data(request.client_id)
        return {
            "speaker": "System",
            "dialogue": f"Identity confirmed: {player_data.get('name', 'Unknown')}. Welcome to the Athena Universe.",
            "player_data": player_data
        }

    # Ensure a player exists for the session
    player_data = game_state.get_player_data(request.client_id)
    if not player_data:
        game_state.assign_role(request.client_id, 'husk1') # Default to Husk Stage 1
        player_data = game_state.get_player_data(request.client_id)

    # --- New Core Logic using RAG --- #
    # The ai_handler now manages lore retrieval, context injection, and the LLM call.
    dialogue = await get_ai_response(action_str, player_data)
    
    # The game_logic processor now primarily handles mechanical changes from AI tags
    processed_dialogue, updated_player_data, img_variant = game_state.process_ai_response(dialogue, player_data)
    
    game_state.save_game(request.client_id) # Placeholder for future save logic

    return {
        "speaker": player_data.get('current_npc', 'Athena (GM)'),
        "dialogue": processed_dialogue,
        "player_data": updated_player_data,
        "img_variant": img_variant
    }
