# ingestion/loader.py
from typing import List
from PIL import Image
import io
import pypdf

def load_documents_from_files(files: List):
    documents = []
    for file in files:
        filename = file.name
        # Reset file pointer to the beginning in case it was read elsewhere
        file.seek(0) 
        content = file.read()
        
        # --- PDF BRANCH (Missing earlier) ---
        if filename.lower().endswith(".pdf"):
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if text.strip():
                documents.append({"text": text, "source": filename, "type": "text"})
            else:
                print(f"Warning: PDF {filename} appears to be empty or image-only.")

        # --- EXISTING BRANCHES ---
        elif filename.lower().endswith(".txt"):
            text = content.decode("utf-8")
            documents.append({"text": text, "source": filename, "type": "text"})
            
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(io.BytesIO(content)).convert("RGB")
            documents.append({"image": img, "source": filename, "type": "image"})
            
        else:
            print(f"Skipping unsupported file type: {filename}")
            
    return documents