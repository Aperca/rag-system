# ingestion/ingest_pipeline.py
from ingestion.loader import load_documents_from_files
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_text_chunks, embed_images
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="vector_store")
collection = client.get_or_create_collection("research_knowledge_base")
def run_ingestion_from_files(files):
    print("Starting ingestion pipeline...")
    documents = load_documents_from_files(files)
    print("Documents loaded:", documents)

    chunks = chunk_text(documents)
    print("Chunks:", [c.get("text") or c.get("image") for c in chunks])

    text_embeddings = embed_text_chunks([c["text"] for c in chunks if c["type"]=="text"])
    image_embeddings = embed_images([c["image"] for c in chunks if c["type"]=="image"])

    all_embeddings = text_embeddings + image_embeddings
    print("Total embeddings:", len(all_embeddings))

    # Add to Chroma
    for idx, emb in enumerate(all_embeddings):
        collection.add(
            ids=[str(idx)],
            embeddings=[emb["embedding"]],
            metadatas=[{"source": emb["source"], "type": emb["type"]}],
            documents=[emb.get("text", "")]  # images can be empty string
        )
    print("Collection count:", collection.count())
    print("Ingestion complete.")