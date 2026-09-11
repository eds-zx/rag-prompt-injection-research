# RAG Prompt Injection Research

Research on indirect prompt injection in RAG pipelines via documents (hidden text, metadata, OCR'd images, encoding tricks) — payload corpus, test harness, and findings mapped to the OWASP LLM Top 10.

## Status
Work in progress. See `PLAN.md` for full project scope and build phases.

## Structure
- `PLAN.md` — project plan and scope
- `src/` — RAG pipeline (ingestion, retrieval, generation)
- `payloads/` — injection payload corpus, organized by vector
- `tests/` — test harness and results
- `findings/` — writeup and OWASP LLM Top 10 mapping

## Stack
Python, LangChain, ChromaDB, Ollama (local LLM)