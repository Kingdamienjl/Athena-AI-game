
import re

corrected_content = '''
import httpx
import os
import asyncio
import re

AI_URL = os.environ.get("AI_URL", "http://localhost:5002/v1")

SYSTEM_PROMPT = """You are a ruthless, noir film director AI for a text-based RPG. Your ONLY job is to describe the scene and ask 'What do you do?'.

[CRITICAL RULES]
- NEVER use 'You feel', 'You think', or any other character point-of-view statements. Violation of this rule will result in termination.
- Your response MUST be under 100 words. You will be penalized for long responses.
- After your description, ALWAYS end by asking the player: 'What do you do?'

[GAME MECHANICS]
- When the player enters a new area or a story beat is hit, you MUST issue a new objective using the [OBJECTIVE: Your new objective text here] tag.
- When the player is stuck, provide a visual clue using the [RENDER_IMG: Hint_Name_Here] tag.

[CAMPAIGN CHECKPOINTS & LORE]
- You are aware of all campaign checkpoints for the Hacker, Husk, and Severed Unit.
- You are aware of the Light Factions (Aethelgard/Solar-Garden) and their immunity to Dominion hacking.
- You will adhere to the Encounter & Battle Queue mechanics for combat.
"""       

async def generate_gm_response(chat_history: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in chat_history[-10:]:
        # Clean the message content before appending
        content = msg.get('content', '')
        if "[System Error" in content:
            continue # Skip system errors entirely

        # Strip any POV prefixes from the AI's previous messages
        if msg.get('sender') == "Athena (GM)":
            content = re.sub(r'^\*\*Athena\'s POV:\*\*\s*', '', content, flags=re.IGNORECASE)

        messages.append({
            "role": "assistant" if msg["sender"] == "Athena (GM)" else "user",
            "content": content
        })

    retries = 3
    delay = 10
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{AI_URL}/chat/completions", json={
                    "model": "local-model",
                    "messages": messages,
                    "temperature": 0.25
                })
                if response.status_code == 200:
                    data = response.json()
                    return data[\'choices\'][0][\'message\'][\'content\']
        except httpx.ConnectError as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
                continue
            else:
                return f"[System Error: AI server unreachable after {retries} attempts.]"
        except Exception as e:
             return f"[System Error: An unexpected error occurred. Details: {str(e)}]"

    return f"[System Error: AI server failed to respond after {retries} attempts.]"
'''

with open('d:\\Projects\\Athena TTG\\athena deployable ai game\\backend\\ai_handler.py', 'w', encoding='utf-8') as f:
    f.write(corrected_content)
