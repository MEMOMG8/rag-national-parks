from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("national_parks")

def retrieve(query, k=4):
    embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=k
    )
    print(f"\nQuery: {query}")
    print("-" * 60)
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"Result {i+1} | Source: {meta['source']} | Distance: {dist:.3f}")
        print(doc[:200])
        print()

# Test with our 3 evaluation questions
retrieve("What wildlife can visitors see at Yellowstone?")
retrieve("How do I get a camping permit at the Grand Canyon?")
retrieve("What are the most popular hikes in Yosemite?")