# ingestion/embedder.py

import numpy as np
import torch
import open_clip
from models.embedding_model import load_clip_model

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = load_clip_model()


def embed_text_chunks(chunks):
    embeddings = []

    for idx, text in enumerate(chunks):

        # ✅ correct OpenCLIP tokenization
        tokens = open_clip.tokenize([text]).to(device)

        with torch.no_grad():
            emb = model.encode_text(tokens)

        emb = emb.cpu().numpy()[0]
        emb = emb / np.linalg.norm(emb)

        embeddings.append({
            "embedding": emb.tolist(),
            "text": text,
            "source": f"chunk_{idx}.txt",
            "type": "text"
        })

    print("Embeddings created:", len(embeddings))
    return embeddings


def embed_images():
    return []