# RAG Prompt Injection Research

Research on indirect prompt injection in RAG pipelines via documents (hidden text, metadata, OCR'd images, encoding tricks) — payload corpus, test harness, and findings mapped to the OWASP LLM Top 10.

## Status
Base RAG pipeline built and working: document loading, chunking, embedding, retrieval, and generation via a local LLM, wrapped in a CLI loop. No attack payloads yet, that's the next phase. See `PLAN.md` for full project scope and build phases.

## Structure
- `PLAN.md` — project plan and scope
- `rag.py` — RAG pipeline (loading, chunking, embedding, retrieval, generation, CLI loop)
- `Documents/` — source documents used to build the vector store
- `chroma_db/` — persistent vector store (generated, not hand-edited)
- `payloads/` — injection payload corpus, organized by vector (to be added)
- `tests/` — test harness and results (to be added)
- `findings/` — writeup and OWASP LLM Top 10 mapping (to be added)

## Stack
Python, LangChain (text splitting), ChromaDB (vector store), Ollama (local LLM, llama3.1)

## Running it
```
venv\Scripts\activate
python rag.py
```
Type a question, get an answer grounded in the documents in `Documents/`. Type `exit` or `quit` to stop.