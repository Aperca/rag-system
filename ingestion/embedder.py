from PIL import Image
import torch
from pathlib import Path

from models.embedding_model import load_clip_model


model, preprocess, tokenizer = load_clip_model()


def embed_text_chunks(chunks):
    """
    Convert text chunks into CLIP embeddings
    """

    texts = [chunk["text"] for chunk in chunks]

    tokens = tokenizer(texts)

    with torch.no_grad():
        text_features = model.encode_text(tokens)

    embeddings = text_features.cpu().numpy()

    embedded_docs = []

    for chunk, emb in zip(chunks, embeddings):
        embedded_docs.append({
            "embedding": emb,
            "text": chunk["text"],
            "source": chunk["source"],
            "type": "text"
        })

    return embedded_docs


def embed_images(image_folder="data/images"):
    """
    Convert images into CLIP embeddings
    """

    image_embeddings = []

    image_dir = Path(image_folder)

    for img_path in image_dir.glob("*"):

        image = preprocess(Image.open(img_path)).unsqueeze(0)

        with torch.no_grad():
            image_features = model.encode_image(image)

        embedding = image_features.cpu().numpy()[0]

        image_embeddings.append({
            "embedding": embedding,
            "source": str(img_path),
            "type": "image"
        })

    return image_embeddings