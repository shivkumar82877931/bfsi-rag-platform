# BFSI RAG Platform

A Retrieval-Augmented Generation (RAG) pipeline built for BFSI (Banking, Financial Services & Insurance) use cases — starting with querying insurance SOP documents (e.g. motor claims processing) using natural language.

## Overview

This project implements an end-to-end RAG pipeline:

1. **Ingestion** — loads source documents (PDFs) into the pipeline
2. **Chunking** — splits documents into retrievable text segments
3. **Embeddings** — converts text chunks into vector representations
4. **Retrieval** — fetches the most relevant chunks for a given query
5. **Generation** — uses an LLM to generate answers grounded in retrieved context

## Tech Stack

- Python
- ChromaDB (vector store)
- [Embedding model / LLM provider — update with what you're using]
- LangChain (if used — update based on actual implementation)

## Project Structure

\`\`\`
bfsi-rag-platform/
├── config/           # configuration files
├── data/             # source documents (not tracked in git)
├── notebooks/        # exploratory notebooks
├── src/
│   ├── ingestion/     # document loading
│   ├── chunking/      # text chunking logic
│   ├── embeddings/    # embedding generation
│   ├── retrieval/     # vector search / retrieval logic
│   ├── generation/    # LLM-based answer generation
│   ├── api/           # API layer (if applicable)
│   └── evaluation/    # evaluation scripts
├── tests/            # unit tests
└── vectorstore/      # persisted vector DB (not tracked in git)
\`\`\`

## Setup

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

Add a \`.env\` file with required API keys (not tracked in git):
\`\`\`
OPENAI_API_KEY=your_key_here
\`\`\`

## Usage

[Update this section with actual run instructions once the pipeline is wired end-to-end]

## Status

🚧 Work in progress — building out retrieval and API layers.

## Author

Shiv Kumar
