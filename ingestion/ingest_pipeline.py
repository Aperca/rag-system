# ingestion/ingest_pipeline.py

import chromadb
from chromadb.config import Settings

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_text_chunks


def run_ingestion():

    print("Starting ingestion pipeline...")

    # load documents
    docs = load_documents()

    # chunk them
    chunks = chunk_documents(docs)

    # create embeddings
    embeddings = embed_text_chunks(chunks)

    print("Total embeddings:", len(embeddings))

    # connect to vector DB

    client = chromadb.PersistentClient(path="vector_store")
    collection = client.get_or_create_collection(
        name="research_knowledge_base"
    )

    # store embeddings
    for i, item in enumerate(embeddings):
        collection.add(
            ids=[str(i)],
            embeddings=[item["embedding"]],
            documents=[item["text"]],
            metadatas=[{"source": item["source"], "type": item["type"]}],
        )

    print("Collection count:", collection.count())
    print("Ingestion complete.")
