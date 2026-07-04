from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from memory import LoreMemory
from director import evaluate_pacing
from actor import generate_npc_dialogue
from game_logic import GameStateManager

app = FastAPI()

# Updated CORS matrix to support your new Port 5180+ configuration
origins = [
    "http://localhost:5173", "http://127.0.0.1:5173",
    "http://localhost:5174", "http://127.0.0.1:5174",
    "http://localhost:5176", "http://127.0.0.1:5176",
    "http://localhost:5180", "http://127.0.0.1:5180",
    "http://localhost:5181", "http://127.0.0.1:5181",
    "http://localhost:5182", "http://127.0.0.1:5182",
    "http://localhost:5183", "http://127.0.0.1:5183",
    "http://localhost:5184", "http://127.0.0.1:5184",
    "http://localhost:5185", "http://127.0.0.1:5185",
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
    lore_memory = LoreMemory()
    action_str = request.action_text.strip()

    # Role assignment intercept
    if action_str.startswith("/role "):
        target_role = action_str.replace("/role ", "").strip()
        game_state.assign_role(request.client_id, target_role)
        player_data = game_state.get_player_data(request.client_id)
        
        return {
            "speaker": "System",
            "dialogue": f"[SYSTEM: Identity sequence compiled for: {player_data['name']}.]",
            "player_data": player_data,
            "img_variant": None # No image for system commands
        }

    player_data = game_state.get_player_data(request.client_id)
    if not player_data:
        game_state.assign_role(request.client_id, 'husk')
        player_data = game_state.get_player_data(request.client_id)

    current_npc = player_data.get('current_npc', 'Athena (GM)')

    # Core engine flow
    retrieved_lore = await lore_memory.search_lore(action_str)
    director_instruction = await evaluate_pacing(action_str, retrieved_lore, player_data.get('objective', ''))
    dialogue = await generate_npc_dialogue(current_npc, action_str, retrieved_lore, director_instruction)
    
    # Process response and extract the image asset key
    processed_dialogue, updated_player_data, img_variant = game_state.process_ai_response(dialogue, player_data)
    game_state.save_game(request.client_id)

    # Return structured data to frontend, including the asset variant key
    return {
        "speaker": current_npc,
        "dialogue": processed_dialogue,
        "player_data": updated_player_data,
        "img_variant": img_variant 
    }