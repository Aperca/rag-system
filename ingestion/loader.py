# ingestion/loader.py
from typing import List
from langchain_core.documents import Document
from PIL import Image
import io

def load_documents_from_files(files: List):
    """
    Accepts a list of uploaded files (text or images) and returns a list of Documents.
    """
    documents = []
    for file in files:
        filename = file.name
        content = file.read()
        if filename.endswith(".txt"):
            text = content.decode("utf-8")
            documents.append({"text": text, "source": filename, "type": "text"})
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(io.BytesIO(content)).convert("RGB")
            documents.append({"image": img, "source": filename, "type": "image"})
        else:
            print(f"Skipping unsupported file type: {filename}")
    return documents