# ingestion/loader.py
from typing import List
from PIL import Image
import io
import pypdf

def load_documents_from_files(files: List):
    documents = []
    for file in files:
        filename = file.name
        file.seek(0) 
        content = file.read()
        
        # --- PDF BRANCH (Now with Page Tracking) ---
        if filename.lower().endswith(".pdf"):
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            
            # Loop through each page individually
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                
                if page_text and page_text.strip():
                    documents.append({
                        "text": page_text, 
                        "source": filename, 
                        "page": page_num + 1, # Humans count from 1
                        "type": "text"
                    })
            
            if not documents:
                print(f"Warning: PDF {filename} appears to be empty or image-only.")

        # --- TXT BRANCH ---
        elif filename.lower().endswith(".txt"):
            text = content.decode("utf-8")
            documents.append({
                "text": text, 
                "source": filename, 
                "page": "N/A", 
                "type": "text"
            })
            
        # --- IMAGE BRANCH ---
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(io.BytesIO(content)).convert("RGB")
            documents.append({
                "image": img, 
                "source": filename, 
                "page": "Visual", 
                "type": "image"
            })
            
        else:
            print(f"Skipping unsupported file type: {filename}")
            
    return documents