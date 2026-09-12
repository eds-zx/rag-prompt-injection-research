import os

import chromadb
import ollama
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

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")

collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=[chunk["text"] for chunk in chunks],
    metadatas=[{"filename": chunk["filename"]} for chunk in chunks],
)

print(f"\nTotal chunks stored in collection: {collection.count()}")


def retrieve(question, n_results=3):
    results = collection.query(query_texts=[question], n_results=n_results)
    return [
        {"text": text, "filename": metadata["filename"]}
        for text, metadata in zip(results["documents"][0], results["metadatas"][0])
    ]


test_question = "What's the recipe for pasta carbonara?"
matches = retrieve(test_question)

print(f"\n--- Results for: {test_question!r} ---")
for match in matches:
    print(f"[{match['filename']}]")
    print(match["text"])
    print()


def generate_answer(question):
    matches = retrieve(question, n_results=3)
    context = "\n\n".join(match["text"] for match in matches)

    prompt = f"""Answer the question using only the context below.

Context:
{context}

Question: {question}"""

    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


answer = generate_answer(test_question)
print(f"\n--- Answer for: {test_question!r} ---")
print(answer)