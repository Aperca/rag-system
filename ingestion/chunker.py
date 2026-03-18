# ingestion/chunker.py

def chunk_documents(documents):
    """
    Very simple semantic chunking: for now, each document is a chunk.
    """
    chunks = []
    for doc in documents:
        chunks.append(doc["text"])
    print("Chunks:", chunks)
    return chunks
