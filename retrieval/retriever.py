# retrieval/retriever.py

import chromadb
import numpy as np
import torch
import open_clip
from chromadb.config import Settings
from models.embedding_model import load_clip_model

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess, device = load_clip_model()

client = chromadb.PersistentClient(path="vector_store")
collection = client.get_or_create_collection("research_knowledge_base")


def retrieve(query, top_k=3):

    # tokenize query correctly
    tokens = open_clip.tokenize([query]).to(device)

    with torch.no_grad():
        query_embedding = model.encode_text(tokens)

    query_embedding = query_embedding.cpu().numpy()[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results= 2
    )

    return results