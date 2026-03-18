# ingestion/ingest_pipeline.py

import chromadb
from chromadb.config import Settings

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_text_chunks

from ingestion.loader import load_documents_from_files
from ingestion.chunker import chunk_text
from vectorstore.chroma_store import store_embeddings

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


def run_ingestion_from_files(files):
    print("Processing uploaded files...")

    documents = load_documents_from_files(files)

    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        all_chunks.extend(chunks)

    embeddings = embed_text_chunks(all_chunks)

    store_embeddings(embeddings)

    print("Upload ingestion complete.")