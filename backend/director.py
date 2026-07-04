import httpx

async def evaluate_pacing(player_input, retrieved_lore, current_objective):
    """
    Acts as the hidden AI Game Master. Evaluates the player's action against the
    lore and objective, and outputs a 1-2 sentence stage direction for the Actor.
    """
    
    system_prompt = f"""You are the hidden Game Director of the Athena Universe RPG.
Your ONLY job is to control pacing and guide the player toward their objective.
DO NOT write dialogue. DO NOT speak to the player.
Output ONLY a 1-2 sentence stage direction for the NPC to follow.

CURRENT OBJECTIVE: {current_objective}

RELEVANT LORE:
{retrieved_lore}

PLAYER ACTION: {player_input}

DIRECTOR RULES:
1. If the player is actively advancing the objective, instruct the NPC to be helpful and reveal information based on the lore.
2. If the player's action violates the lore (e.g., trying to use magic that doesn't exist), instruct the NPC to react with confusion and reject the action.
3. If the player is off-topic, meandering, or stalling, instruct the NPC to introduce a complication, refuse cooperation, or escalate tension to force the player back on track.

Output your stage direction now:"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:5002/api/generate", json={
                "model": "qwen2.5",
                "prompt": system_prompt,
                "stream": False
            }, timeout=30.0)
            response.raise_for_status()
            
            director_instruction = response.json().get("response", "").strip()
            return director_instruction
            
    except Exception as e:
        print(f"'\u274c Director AI failed: {e}")
        # Fallback instruction so the game doesn't crash if the AI glitches
        return "The NPC stares blankly, waiting for the player to make a clearer move."