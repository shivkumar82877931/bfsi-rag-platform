import sys
sys.path.append('.')

from sentence_transformers import SentenceTransformer
import chromadb
from src.ingestion.document_loader import load_all_documents
from src.chunking.text_chunker import chunk_documents


def get_embedding_model():
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Embedding model loaded")
    return model


def store_in_vectordb(chunks: list, collection_name: str = "bfsi_documents"):
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="vectorstore")
    
    # Delete collection if exists
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(collection_name)
    
    # Load embedding model
    model = get_embedding_model()
    
    # Prepare data
    texts = [chunk["content"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts).tolist()
    
    # Store in ChromaDB
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Stored {len(chunks)} chunks in vector database")
    return collection


def search(query: str, collection, top_k: int = 3):
    model = get_embedding_model()
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    return results


if __name__ == "__main__":
    # Load and chunk documents
    documents = load_all_documents("data")
    chunks = chunk_documents(documents)
    
    # Store in vector DB
    collection = store_in_vectordb(chunks)
    
    # Test search
    query = "What documents are required for motor insurance claim?"
    print(f"\nSearching: {query}")
    results = search(query, collection)
    
    print("\n--- Search Results ---")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\nResult {i+1}:")
        print(f"Content: {doc[:200]}")
        print(f"Source: {results['metadatas'][0][i]['document_name']}")
        print(f"Page: {results['metadatas'][0][i]['page_number']}")
