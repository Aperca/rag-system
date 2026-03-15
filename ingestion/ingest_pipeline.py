import chromadb

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_text_chunks, embed_images


def run_ingestion():

    print("Starting ingestion pipeline...")

    # Load documents
    documents = load_documents()

    # Chunk documents
    chunks = chunk_documents(documents)

    # Create text embeddings
    text_embeddings = embed_text_chunks(chunks)

    # Create image embeddings
    image_embeddings = embed_images()

    # Combine them
    all_embeddings = text_embeddings + image_embeddings

    print("Total embeddings:", len(all_embeddings))

    # Initialize Chroma client
    client = chromadb.Client()

    collection = client.get_or_create_collection(name="research_knowledge_base")

    # Store embeddings
    for idx, item in enumerate(all_embeddings):

        collection.add(
            embeddings=[item["embedding"].tolist()],
            ids=[str(idx)],
            metadatas=[{
                "source": item["source"],
                "type": item["type"]
            }],
            documents=[item.get("text", "image")]
        )

    print("Ingestion complete.")