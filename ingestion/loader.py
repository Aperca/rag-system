import os
from pypdf import PdfReader

def load_documents_from_files(files):
    documents = []

    for file in files:
        filename = file.name

        # TXT FILES
        if filename.endswith(".txt"):
            text = file.read().decode("utf-8")

        # PDF FILES
        elif filename.endswith(".pdf"):
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        else:
            continue

        documents.append({
            "text": text,
            "source": filename
        })

    return documents