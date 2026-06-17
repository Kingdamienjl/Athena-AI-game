import re
import json
import os

# --- MOCK SAVE/LOAD FUNCTIONS (Mirroring your game_logic.py) ---
def save_game(client_id, state_dict):
    os.makedirs("saves", exist_ok=True)
    with open(f"saves/{client_id}_save.json", "w") as f:
        json.dump(state_dict, f, indent=4)
    print(f"[SYSTEM] Game saved for client: {client_id}")


def load_game(client_id):
    try:
        with open(f"saves/{client_id}_save.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- MOCK PARSER FUNCTION ---
def process_ai_response(ai_text, player_state):
    print("\n--- ORIGINAL AI TEXT ---")
    print(ai_text)
    
    segments = [segment.strip() for segment in ai_text.split('>') if segment.strip()]

    # 1. Parse Objective >
    if len(segments) >= 3:
        new_objective = segments[2]
        player_state["objective"] = new_objective
        print(f"[PARSED] Objective updated: {new_objective}")

    # 2. Parse Item >
    if "find exactly what you were looking for" in ai_text.lower():
        new_item = "Data Spike"
        if new_item not in player_state["inventory"]:
            player_state["inventory"].append(new_item)
            print(f"[PARSED] Item added to inventory: {new_item}")

    # 3. Parse Damage >
    damage = None
    damage_match = re.search(r"(\d+)\s*(?:damage|hit|burn)", ai_text, re.IGNORECASE)
    if damage_match:
        damage = int(damage_match.group(1))
    elif "burning your leg" in ai_text.lower():
        damage = 15

    if damage is not None:
        player_state["hp"] -= damage
        print(f"[PARSED] Player took {damage} damage! Current HP: {player_state['hp']}")

    # Clean up any trailing whitespace left by stripping tags
    clean_text = re.sub(r'>', '', ai_text).strip()
    
    # Save the updated state
    save_game(player_state["client_id"], player_state)
    
    print("\n--- CLEAN TEXT FOR FRONTEND ---")
    print(clean_text)
    
    return clean_text, player_state

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Mock starting state for a new player
    mock_player_state = {
        "client_id": "test_user_001",
        "role": "hacker",
        "level": 1,
        "hp": 100,
        "inventory": [],
        "objective": "Survive the interrogation."
    }

    # Simulated response from the LLM containing the new tags
    simulated_llm_response = (
        "You pry the loose floorboard up with bleeding fingers. Beneath the rusted metal, "
        "you find exactly what you were looking for. > "
        "Suddenly, a spark of loose coolant circuitry arcs across the floor, burning your leg! "
        "> The door down the hall unlocks with a heavy clank. You need to get to the "
        "server room before the AEGIS guards realize the power is out. "
        ">"
    )

    # Run the test
    clean_text, updated_state = process_ai_response(simulated_llm_response, mock_player_state)
    
    print("\n--- FINAL PLAYER STATE DICTIONARY ---")
    print(json.dumps(updated_state, indent=4))
