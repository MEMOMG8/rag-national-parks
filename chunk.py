import os
import json

CHUNK_SIZE = 400
OVERLAP = 50

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

all_chunks = []

for filename in os.listdir("docs"):
    if filename.endswith(".txt"):
        source = filename.replace(".txt", "")
        with open(f"docs/{filename}", "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": source,
                "chunk_index": i,
                "text": chunk
            })
        print(f"{source}: {len(chunks)} chunks")

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)

print(f"\nTotal chunks: {len(all_chunks)}")
print("Saved to chunks.json")