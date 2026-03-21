import ollama 
from PIL import Image
import io
import numpy as np
import torch
from models.embedding_model import load_clip_model
import open_clip
model, preprocess, device = load_clip_model()  # returns model, preprocess, device

def embed_text_chunks(text_chunks_data): # Pass the WHOLE dictionary, not just text
    embeddings = []
    for idx, chunk_data in enumerate(text_chunks_data):
        text = chunk_data["text"]
        tokens = open_clip.tokenize([text]).to(device)
        
        with torch.no_grad():
            emb = model.encode_text(tokens)
        
        emb = emb.cpu().numpy()[0]
        emb = emb / np.linalg.norm(emb)
        
        embeddings.append({
            "embedding": emb.tolist(),
            "text": text,
            "source": chunk_data["source"], # Use the REAL filename
            "page": chunk_data.get("page", "N/A"), # Keep the Page Number
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

def describe_image(image_obj):
    """
    Uses Ollama (moondream or llama3.2-vision) to describe an image.
    """
    # Convert PIL Image to bytes for Ollama
    img_byte_arr = io.BytesIO()
    image_obj.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()

    try:
        #  'moondream' because it is very fast and small
        response = ollama.generate(
            model='moondream', 
            prompt='Describe this image in detail for a research database.',
            images=[img_bytes]
        )
        return response['response']
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "A research-related image or diagram."