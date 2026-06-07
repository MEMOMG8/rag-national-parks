import json
from sentence_transformers import SentenceTransformer
import chromadb

# Load chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("national_parks")

# Embed and store
print("Embedding and storing chunks...")
texts = [c["text"] for c in chunks]
ids = [f"{c['source']}_{c['chunk_index']}" for c in chunks]
metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

embeddings = model.encode(texts, show_progress_bar=True)

collection.add(
    documents=texts,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
    ids=ids
)

print(f"\nStored {len(chunks)} chunks in ChromaDB")
print("Done!")