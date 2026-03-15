from ingestion.loader import load_documents

docs = load_documents()

for doc in docs:
    print(doc["source"])
    print(doc["text"])
    print("----")