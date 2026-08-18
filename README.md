# BFSI RAG Platform

An enterprise-style Retrieval-Augmented Generation (RAG) platform that lets employees ask natural-language questions over BFSI documents (policies, SOPs, claims guidelines, regulatory documents) and receive grounded, source-cited answers.

## Business Problem

BFSI organizations hold large volumes of policies, SOPs, claims guidelines, and regulatory documents. Employees currently search these manually, which is slow and error-prone. This project builds a system to answer natural-language questions directly from these documents, with traceable citations back to the source page.

## Architecture

PDF/DOCX/TXT -> Document Ingestion -> Parsing -> Cleaning -> Chunking -> Metadata Enrichment -> Embeddings -> Vector DB -> Retrieval -> Reranking -> Context -> LLM -> Grounded Answer + Citation

## Tech Stack

- Python
- PyMuPDF / Unstructured (document processing)
- LangChain
- Hugging Face / OpenAI-compatible embeddings
- Chroma (vector DB)
- OpenAI-compatible LLM
- FastAPI
- Docker
- RAGAS / custom evaluation
- AWS (later phase)

## Build Phases

1. Ingestion - load, parse, clean, attach metadata
2. Chunking - 500-800 token chunks, 50-100 token overlap
3. Embeddings - vectorize each chunk
4. Retrieval - top-K similarity search
5. Generation - LLM answers grounded strictly in retrieved context
6. Citation - every answer includes source document and page number
7. Evaluation - Precision, Recall, Faithfulness, Answer Relevance, Context Relevance, Latency

## Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Status

In progress: Ingestion done, Chunking done, Embeddings done, Retrieval next, then Generation, Evaluation, API, Docker, AWS deployment.

## Author

Shiv Kumar
