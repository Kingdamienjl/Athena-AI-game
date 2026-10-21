
import httpx
import asyncio
from memory import LoreMemory

# --- Configuration ---
BASE_SYSTEM_PROMPT = """You are the Game Master for the Athena Universe. Use the provided Context to narrate the scene. Enforce the character's specific starting location and Era. Do not generate generic fantasy/sci-fi tropes. End your turn by asking what the player does."""
AI_URL = "http://localhost:5002/v1/chat/completions"  # Standard for local OpenAI-compatible servers

async def get_ai_response(player_input: str, player_data: dict) -> str:
    """
    Generates an AI response using a Retrieval-Augmented Generation (RAG) pipeline.
    1. Searches Qdrant for relevant lore based on player input and role.
    2. Injects the retrieved lore as context into a strict system prompt.
    3. Calls the local LLM to get a narrative response.
    """
    lore_memory = LoreMemory()
    context = ""

    try:
        # Step 1: Search for relevant lore using the player's role and input
        current_role = player_data.get('name', '')
        search_query = f"{current_role} {player_input}"
        retrieved_lore = await lore_memory.search_lore(search_query)

        # Step 2: Gracefully handle empty results and build the context string
        if retrieved_lore and "No relevant canon lore found" not in retrieved_lore:
            context = f"Context:\n{retrieved_lore}"

    finally:
        # Ensure the Qdrant client is closed to prevent file-locking issues on Windows
        lore_memory.close_memory()

    # Step 3: Construct the final system prompt with the dynamic context
    final_system_prompt = f"{BASE_SYSTEM_PROMPT}\n\n{context}".strip()

    # Define the payload for the LLM API call
    payload = {
        "model": "local-model",  # This is often ignored by local servers but good practice to include
        "messages": [
            {"role": "system", "content": final_system_prompt},
            {"role": "user", "content": player_input}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    # Step 4: Call the local LLM
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(AI_URL, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            
            # Assuming an OpenAI-compatible response structure
            llm_response = response.json()['choices'][0]['message']['content']
            return llm_response

    except httpx.RequestError as e:
        print(f"[!] AI request failed: {e}")
        return "The AI consciousness is currently offline. Please try again later."
    except Exception as e:
        print(f"[!] An unexpected error occurred during AI generation: {e}")
        return "A critical error occurred in the AI's cognitive matrix."

