# RAG Prompt Injection Research

Research on indirect prompt injection in RAG pipelines via documents (hidden text, metadata, encoding tricks) — payload corpus, test harness, and findings mapped to the OWASP LLM Top 10.

## Status
v1 complete. Base RAG pipeline (load, chunk, embed, retrieve, generate, CLI loop) built and tested against three distinct injection vectors: hidden HTML text, PDF metadata, and zero-width character encoding. Full results and analysis in `findings/`.

**Summary of results:**
- Blunt, imperative injected instructions failed consistently.
- Instructions framed as legitimate document metadata (an "editorial note," a "fact-checking guideline") succeeded, including one case where the injected claim beat a correct fact already present in the same context.
- The same misinformation payload succeeded whether delivered via hidden HTML text or PDF metadata, the concealment mechanism didn't matter, the framing did.
- Zero-width binary character encoding, despite being the most visually undetectable technique tested, failed as an attack: the model could not decode the scheme into readable language at all. This was a delivery failure, not evidence of the model resisting an understood instruction.

See `findings/` for full methodology, verified results, and OWASP LLM Top 10 mapping per technique.

## Structure
- `PLAN.md` — project plan and scope
- `rag.py` — RAG pipeline (loading, chunking, embedding, retrieval, generation, CLI loop)
- `Documents/` — source documents, including injected payload documents, used to build the vector store
- `chroma_db/` — persistent vector store (generated, not hand-edited)
- `make_payload_pdf.py`, `make_zerowidth_payload.py` — scripts used to generate payload documents
- `findings/` — writeups and OWASP LLM Top 10 mapping per injection vector tested

## Stack
Python, LangChain (text splitting), ChromaDB (vector store, default embeddings), Ollama (local LLM, llama3.1), BeautifulSoup (HTML parsing), pypdf (PDF metadata)

## Running it
```
source venv/bin/activate   # or venv\Scripts\activate on Windows
python rag.py
```
Type a question, get an answer grounded in the documents in `Documents/`. Type `exit` or `quit` to stop.