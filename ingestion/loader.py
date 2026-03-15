from pathlib import Path


def load_documents(data_path="data/sample_docs"):
    """
    Load text documents from the data directory.
    Returns a list of dictionaries containing text and metadata.
    """

    documents = []

    data_dir = Path(data_path)

    for file_path in data_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "text": text,
            "source": str(file_path)
        })

    return documents