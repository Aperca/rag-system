# ingestion/embedder.py
import numpy as np
import torch
from models.embedding_model import load_clip_model
import open_clip
model, preprocess, device = load_clip_model()  # returns model, preprocess, device

def embed_text_chunks(text_chunks):
    embeddings = []
    for idx, text in enumerate(text_chunks):
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
    return embeddings

def embed_images(images):
    embeddings = []
    for idx, img in enumerate(images):
        img_tensor = preprocess(img).unsqueeze(0).to(device)
        with torch.no_grad():
            emb = model.encode_image(img_tensor)
        emb = emb.cpu().numpy()[0]
        emb = emb / np.linalg.norm(emb)
        embeddings.append({
            "embedding": emb.tolist(),
            "source": f"image_{idx}.png",
            "type": "image"
        })
    return embeddings