import re


def split_into_sentences(text):
    """
    Splits text into sentences using regex.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences


def create_chunks(sentences, chunk_size=3):
    """
    Groups sentences into chunks.
    Example: 3 sentences per chunk
    """
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def chunk_documents(documents, chunk_size=3):
    """
    Takes loaded documents and returns chunked text.
    """

    chunked_docs = []

    for doc in documents:
        sentences = split_into_sentences(doc["text"])
        chunks = create_chunks(sentences, chunk_size)

        for chunk in chunks:
            chunked_docs.append({
                "text": chunk,
                "source": doc["source"]
            })

    return chunked_docs