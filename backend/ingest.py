
import os
import re
import httpx
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams

# --- Configuration ---
LORE_DIR = "/mnt/c/Users/Pimpn/Documents/Athena Universe/Issues"
COLLECTION_NAME = "athena_lore"
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_URL = "http://172.21.64.1:11434/api/embeddings"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# --- 1. Qdrant Client Initialization ---
client = QdrantClient(url="http://127.0.0.1:6333", prefer_grpc=False)

# --- 2. YAML Frontmatter Parsing ---
def parse_frontmatter(content):
    """Extracts YAML frontmatter and content from a markdown file."""
    frontmatter = {}
    match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        content = content[match.end():]
    return frontmatter, content

# --- 3. Text Chunking ---
def chunk_text(text, size, overlap):
    """Splits text into overlapping chunks."""
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks

# --- 4. Main Ingestion Logic ---
def ingest_lore():
    """Reads, chunks, and ingests lore files into Qdrant."""
    # Recreate collection to ensure it's fresh
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' created.")

    all_chunks = []
    all_metadata = []

    for filename in os.listdir(LORE_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(LORE_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                full_content = f.read()
            
            metadata, content = parse_frontmatter(full_content)
            if not metadata.get('issue_title'):
                metadata['issue_title'] = filename # Fallback title
            
            chunks = chunk_text(content, CHUNK_SIZE, CHUNK_OVERLAP)
            
            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadata.append(metadata)

    print(f"Generated {len(all_chunks)} chunks from {len(os.listdir(LORE_DIR))} files.")

    # Batch embed and upsert
    try:
        with httpx.Client(timeout=30.0) as http_client:
            for i in range(0, len(all_chunks), 32): # Process in batches of 32
                batch_chunks = all_chunks[i:i+32]
                batch_meta = all_metadata[i:i+32]
                
                # Get embeddings
                response = http_client.post(EMBEDDING_URL, json={"model": EMBEDDING_MODEL, "prompt": batch_chunks})
                response.raise_for_status()
                embeddings = [r['embedding'] for r in response.json()]

                # Upsert to Qdrant
                client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=models.Batch(
                        ids=[f"{meta.get('issue_title', 'doc')}_{i+j}" for j, meta in enumerate(batch_meta)],
                        vectors=embeddings,
                        payloads=[{"text": chunk, **meta} for chunk, meta in zip(batch_chunks, batch_meta)]
                    )
                )
        print("Ingestion complete!")
    except Exception as e:
        print(f"[!] Ingestion failed: {e}")

if __name__ == "__main__":
    ingest_lore()
    client.close()

