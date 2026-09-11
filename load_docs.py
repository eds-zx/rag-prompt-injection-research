import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

documents = {}

for filename in os.listdir("Documents"):
    if filename.endswith(".txt"):
        with open(os.path.join("Documents", filename), "r", encoding="utf-8") as f:
            documents[filename] = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = []
for filename, content in documents.items():
    for chunk in splitter.split_text(content):
        chunks.append({"filename": filename, "text": chunk})

chunk_counts = {}
for chunk in chunks:
    chunk_counts[chunk["filename"]] = chunk_counts.get(chunk["filename"], 0) + 1

for filename, count in chunk_counts.items():
    print(f"{filename}: {count} chunks")

print("\n--- Sample chunk ---")
print(chunks[0]["filename"])
print(chunks[0]["text"])