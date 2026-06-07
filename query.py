from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("national_parks")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question, k=4):
    # Retrieve relevant chunks
    embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=k)

    chunks = results["documents"][0]
    sources = list(set(m["source"] for m in results["metadatas"][0]))

    context = "\n\n".join(chunks)

    prompt = f"""You are a helpful assistant that answers questions about US National Parks.
Answer the question using ONLY the information provided in the context below.
If the context does not contain enough information to answer, say "I don't have enough information on that."
Always end your answer with: Sources: {', '.join(sources)}

Context:
{context}

Question: {question}
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    result = ask("What wildlife can visitors see at Yellowstone?")
    print(result["answer"])
    print("\nSources:", result["sources"])