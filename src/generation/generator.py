import sys
sys.path.append('.')

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)


def generate_answer(query: str, retrieved_chunks: list) -> dict:
    """
    Generate answer from retrieved chunks using Groq LLM.
    Returns answer with citations.
    """
    client = get_groq_client()

    # Build context from retrieved chunks
    context_parts = []
    citations = []

    for i, chunk in enumerate(retrieved_chunks):
        content = chunk["content"]
        metadata = chunk["metadata"]
        
        context_parts.append(f"[Source {i+1}]: {content}")
        citations.append({
            "source_num": i + 1,
            "document": metadata.get("document_name", "Unknown"),
            "page": metadata.get("page_number", "Unknown"),
            "domain": metadata.get("business_domain", "Unknown")
        })

    context = "\n\n".join(context_parts)

    # Build prompt
    prompt = f"""You are a BFSI document assistant. Answer the question using ONLY the context provided below.

If the answer is not in the context, say: "I don't have this information in the available documents."

Always end your answer with: "Sources: [list the source numbers you used]"

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    # Call Groq LLM
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful BFSI document assistant. Answer only from provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=500
    )

    answer = response.choices[0].message.content

    return {
        "query": query,
        "answer": answer,
        "citations": citations
    }


if __name__ == "__main__":
    from src.ingestion.document_loader import load_all_documents
    from src.chunking.text_chunker import chunk_documents
    from src.embeddings.embedder import store_in_vectordb, search, get_embedding_model

    # Load pipeline
    documents = load_all_documents("data")
    chunks = chunk_documents(documents)
    collection = store_in_vectordb(chunks)

    # Test query
    query = "What documents are required for motor insurance claim?"
    print(f"\nQuery: {query}")

    # Retrieve
    results = search(query, collection)
    retrieved_chunks = []
    for i, doc in enumerate(results['documents'][0]):
        retrieved_chunks.append({
            "content": doc,
            "metadata": results['metadatas'][0][i]
        })

    # Generate
    response = generate_answer(query, retrieved_chunks)

    print(f"\n--- Answer ---")
    print(response["answer"])
    print(f"\n--- Citations ---")
    for c in response["citations"]:
        print(f"Source {c['source_num']}: {c['document']} | Page {c['page']} | {c['domain']}")
