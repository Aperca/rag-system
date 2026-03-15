from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents


docs = load_documents()

chunks = chunk_documents(docs)

for chunk in chunks:
    print(chunk["text"])
    print("SOURCE:", chunk["source"])
    print("-----")