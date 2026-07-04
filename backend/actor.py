import httpx

async def generate_npc_dialogue(npc_name, player_input, retrieved_lore, director_instruction):
    """
    Acts as the NPC. Reads the true canon lore and strictly follows
    the Director's pacing instructions to generate dialogue.
    """
    
    system_prompt = f"""You are the Game Master for the Athena Universe RPG. 
    YOUR ONLY ROLE is to narrate the player's environment and the consequences of their actions in the second person ('You see...', 'You feel...'). 
    
    CRITICAL RULES: 
    1. NEVER speak as an NPC unless specifically directed to do so in the prompt. 
    2. NEVER write 'Athena's POV'. 
    3. If the player is talking to an NPC, ONLY output the dialogue for that NPC. 
    4. Maintain the Noir/Cyberpunk tone. 
    5. Always end your narration by asking what the player does next. 

    WORLD LORE: 
    {retrieved_lore} 
    
    PACING: 
    {director_instruction} 
    """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:5002/api/generate", json={
                "model": "qwen2.5",  # Change this to your preferred local model
                "prompt": system_prompt + f"\n\nPlayer Action: {player_input}\n{npc_name}:",
                "stream": False
            }, timeout=60.0)
            response.raise_for_status()
            
            npc_dialogue = response.json().get("response", "").strip()
            return npc_dialogue
            
    except Exception as e:
        print(f"[!] Actor AI failed: {e}")
        return f"*{npc_name} stares at you in silence.*"