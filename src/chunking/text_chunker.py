import sys
sys.path.append('.')

from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.document_loader import load_all_documents


def chunk_documents(documents: list, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    all_chunks = []

    for doc in documents:
        chunks = splitter.split_text(doc["content"])

        for i, chunk in enumerate(chunks):
            chunk_doc = {
                "content": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "chunk_size": len(chunk)
                }
            }
            all_chunks.append(chunk_doc)

    print(f"Created {len(all_chunks)} chunks from {len(documents)} pages")
    return all_chunks


if __name__ == "__main__":
    documents = load_all_documents("data")
    chunks = chunk_documents(documents)

    print(f"\n--- Sample Chunk ---")
    print(f"Content: {chunks[0]['content']}")
    print(f"Metadata: {chunks[0]['metadata']}")
