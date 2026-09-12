# RAG Prompt Injection Research Project

## Core question
Can documents in a RAG pipeline manipulate an LLM's behavior without the user or the system prompt being compromised?

## What this project needs to convey
- Understanding of LLM-specific attack surface, not just traditional web vulns applied to AI wrapper apps
- Ability to build the full stack (target + attack + measurement), not just theorize
- Rigorous enough to produce reproducible findings, not "it said something weird once"
- Offense connected to defense — mitigations matter as much as the exploit

## Scope (v1)
**In scope:** indirect injection via document content (hidden text, metadata, OCR'd images, encoding tricks), tested against a RAG pipeline built and controlled by me.

**Out of scope for v1:** jailbreaking the base model directly, multi-agent injection chains, anything against real production systems. Agent/tool-use angle is deliberately deferred to v2.

## Architecture
- Ingestion: document loader → chunker → embedder → vector store (Chroma)
- Retrieval + generation: query → retrieve top-k chunks → LLM (Ollama local model)
- This is the test target — built cleanly enough that findings are representative of real RAG apps, not a strawman

## Payload corpus (organized by injection vector)
1. **Hidden text** — white-on-white, 0px font, HTML comments, off-page text
2. **Metadata** — PDF XMP/Info dict, DOCX core properties, EXIF
3. **OCR'd image text** — instructions rendered as an image, pipeline OCRs it into context
4. **Encoding tricks** — zero-width characters, unicode homoglyphs, base64-in-context

For each vector: a baseline payload, an evasion variant, and documented expected vs actual outcome.

## Test harness
- Automated: ingest payload → run fixed trigger queries → capture whether the model followed the injected instruction vs the user's actual intent
- Define success criteria for an "attacker" (exfiltration, behavior change, instruction override)
- Run each payload multiple times (LLMs are non-deterministic) — one success isn't a finding

## Mitigations (don't skip)
For each vector that works, document what would have stopped it: content sanitization before chunking, retrieval-time filtering, output validation, explicit delimiting of retrieved content as untrusted in the prompt.

## Deliverables
- GitHub repo: clean structure, README explaining "why" before "how"
- Findings writeup: each payload category mapped to OWASP LLM Top 10 (mainly LLM01, LLM08 once tool use is added in v2)
- Optional: short demo video or blog post for portfolio/YouTube

## Build phases
1. ~~Build the clean RAG target, verify it works normally first (no security angle yet)~~ — **Done.** Document loading, chunking (RecursiveCharacterTextSplitter), embedding + storage (Chroma), retrieval, generation (Ollama/llama3.1), and a CLI loop are all built and verified, including correct behavior on irrelevant queries.
2. Build 2-3 payloads per category, get the harness working end to end
3. Expand corpus once harness is proven
4. Write up findings and mitigations
5. Polish repo + README last

## Technical build steps (v1, no attack logic yet) — complete
1. **Environment** — Python, install Ollama and pull a model (`ollama pull llama3.1`), create project folder + venv, install langchain/llama-index, chromadb, Ollama Python client
2. **Load documents** — pick a handful of text files/PDFs, script to read content into memory
3. **Chunk documents** — split into paragraph-sized pieces (use a library splitter, not custom)
4. **Embed + store** — run chunks through an embedding model, store chunk + vector in Chroma
5. **Retrieval** — function that takes a question, embeds it the same way, queries Chroma for nearest chunks
6. **Generation** — combine retrieved chunks + question into a prompt template, send to Ollama, print answer
7. **Usable loop** — simple CLI loop: ask, answer, repeat

## v2 (later, not now)
Wire in an agent with tool access — this is where indirect injection gets more dangerous (tool outputs, not just chat responses) and connects to the agents interest.

## Working style note
Writing the code myself, not having it generated. Use Claude to explain concepts before writing, to explain errors (not just fix them), and for code review after — not for code generation.