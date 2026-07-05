# backend/ai_handler.py 
import httpx 

# Update the URL to point to your local KoboldCPP instance 
# Ensure KoboldCPP is running and pointing to the model in your GameBrain folder 
AI_URL = "http://localhost:5002/v1" 

# The system prompt ensures the AI respects the RPG mechanics 
SYSTEM_PROMPT = """You are the Game Master AI for the Athena Universe. 
Speak in 2nd person. Use the following tags for game state management: 
<<ITEM:Name>>, <<OBJECTIVE:Task>>, <<IMAGE:filename.png>>, [XP:X], [SET_LOCATION:New Location]. 
End every turn with 'What do you do?'""" 

# Ensure the prompt handling sends the full context to the model 
async def get_ai_response(client_id, player_input, game_state): 
    # Your generation logic calling the KoboldCPP endpoint at 5002 
    # ... 
    pass