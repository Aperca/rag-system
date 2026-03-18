# ingestion/chunker.py
from typing import List

def chunk_text(documents: List[dict], chunk_size: int = 500):
    """
    Split text documents into semantic chunks.
    Images are returned as-is (no chunking).
    """
    chunks = []
    for doc in documents:
        if doc["type"] == "text":
            text = doc["text"]
            start = 0
            while start < len(text):
                chunk = text[start:start + chunk_size]
                chunks.append({"text": chunk, "source": doc["source"], "type": "text"})
                start += chunk_size
        else:
            # Keep images as single chunks
            chunks.append(doc)
    return chunks