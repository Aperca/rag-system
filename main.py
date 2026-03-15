from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_text_chunks, embed_images


docs = load_documents()

chunks = chunk_documents(docs)

text_embeddings = embed_text_chunks(chunks)

image_embeddings = embed_images()

print("TEXT EMBEDDINGS:", len(text_embeddings))
print("IMAGE EMBEDDINGS:", len(image_embeddings))