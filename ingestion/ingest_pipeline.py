# ingestion/ingest_pipeline.py
import time
import chromadb
from ingestion.loader import load_documents_from_files
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_text_chunks, embed_images

client = chromadb.PersistentClient(path="vector_store")
collection = client.get_or_create_collection("research_knowledge_base")

def run_ingestion_from_files(files):
    print(f"--- Starting Ingestion for {len(files)} files ---")
    documents = load_documents_from_files(files)
    chunks = chunk_text(documents)

    # Separate text and images
    text_data = [c for c in chunks if c["type"] == "text"]
    image_data = [c for c in chunks if c["type"] == "image"]

    if text_data:
        text_embeddings = embed_text_chunks([c["text"] for c in text_data])
        for i, emb in enumerate(text_embeddings):
            # Map back to original chunk for metadata
            orig_chunk = text_data[i]
            unique_id = f"text_{int(time.time())}_{i}"
            collection.add(
                ids=[unique_id],
                embeddings=[emb["embedding"]],
                metadatas=[{"source": orig_chunk["source"], "page": orig_chunk.get("page", 1), "type": "text"}],
                documents=[orig_chunk["text"]]
            )

    if image_data:
        image_embeddings = embed_images([c["image"] for c in image_data])
        for i, emb in enumerate(image_embeddings):
            orig_chunk = image_data[i]
            unique_id = f"img_{int(time.time())}_{i}"
            collection.add(
                ids=[unique_id],
                embeddings=[emb["embedding"]],
                metadatas=[{"source": orig_chunk["source"], "page": "Visual", "type": "image"}],
                documents=["[Image Content]"] # Chroma needs a doc string
            )
    
    print(f"Ingestion complete. Current Database Size: {collection.count()} chunks.")