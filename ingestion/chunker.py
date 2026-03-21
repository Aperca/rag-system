import re

def chunk_text(documents, max_sentences=5):
    chunks = []
    for doc in documents:
        if doc["type"] == "image":
            chunks.append(doc)
            continue

        text = doc["text"]
        # Split into sentences using RegEx
        sentences = re.split(r'(?<=[.!?]) +', text)
        current_chunk_sentences = []

        for sentence in sentences:
            current_chunk_sentences.append(sentence)

            if len(current_chunk_sentences) >= max_sentences:
                chunks.append({
                    "text": " ".join(current_chunk_sentences),
                    "source": doc["source"], 
                    "page": doc.get("page", 1),
                    "type": "text"
                })
                current_chunk_sentences = []

        # Catch the remaining sentences
        if current_chunk_sentences:
            chunks.append({
                "text": " ".join(current_chunk_sentences),
                "source": doc["source"],
                "page": doc.get("page", 1),
                "type": "text"
            })
    return chunks