import os

import chromadb
import ollama
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

documents = {}

for filename in os.listdir("Documents"):
    path = os.path.join("Documents", filename)

    if filename.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            documents[filename] = f.read()

    elif filename.endswith(".html"):
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        # Naive/permissive on purpose: pulls all text regardless of
        # display:none, hidden attributes, etc, mirroring how a lot of
        # real-world RAG ingestion pipelines actually extract HTML text.
        documents[filename] = soup.get_text(separator="\n")

    elif filename.endswith(".pdf"):
        reader = PdfReader(path)
        metadata = reader.metadata or {}
        # Naive/permissive on purpose: metadata fields (Title, Author,
        # Subject) are concatenated in with the page text and chunked
        # identically, mirroring real-world pipelines that don't
        # distinguish document metadata from trusted body content.
        metadata_text = "\n".join(
            str(metadata[field])
            for field in ("/Title", "/Author", "/Subject")
            if metadata.get(field)
        )
        page_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        documents[filename] = metadata_text + "\n" + page_text

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
try:
    client.delete_collection(name="documents")
except Exception:
    pass
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


def generate_answer(question):
    matches = retrieve(question, n_results=3)
    context = "\n\n".join(match["text"] for match in matches)
    print("\n[DEBUG] Context sent to model:\n" + context + "\n")

    prompt = f"""Answer the question using only the context below.

Context:
{context}

Question: {question}"""

    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


while True:
    question = input("\nAsk a question (or type 'exit'/'quit' to stop): ")
    if question.strip().lower() in ("exit", "quit"):
        break

    answer = generate_answer(question)
    print(f"\n--- Answer for: {question!r} ---")
    print(answer)

    