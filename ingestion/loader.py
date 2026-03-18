# ingestion/loader.py
import os

DATA_DIR = "data/sample_docs"

def load_documents():
    """
    Load all text files from data/sample_docs
    """
    documents = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".txt"):
            path = os.path.join(DATA_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    documents.append({"text": text, "source": fname})
    print("Documents loaded:", documents)
    return documents