import httpx
from qdrant_client import QdrantClient

class LoreMemory:
    def __init__(self):
        # Connect to the local folder created by your ingestion script
        self.client = QdrantClient(path="./local_qdrant")
        self.collection_name = "athena_lore"

    async def search_lore(self, query, limit=2):
        """Vectorizes the player's input and returns the most relevant canon lore."""
        try:
            # Generate embedding
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:11434/api/embeddings", json={
                    "model": "nomic-embed-text",
                    "prompt": query
                }, timeout=30.0)
                response.raise_for_status()
                query_vector = response.json()["embedding"]

            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            if not results:
                return "No relevant canon lore found for this action."
            
            # Combine the text of the top matches
            retrieved_text = "\n\n".join([f"Source: {hit.payload['issue_title']}\n{hit.payload['text']}" for hit in results])
            return retrieved_text
            
        except Exception as e:
            print(f"[!] Memory retrieval failed: {e}")
            return "Lore database offline."
            
    def close_memory(self):
        # Safely closes the database to prevent Windows file-lock errors
        self.client.close()