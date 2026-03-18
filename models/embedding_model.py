# models/embedding_model.py

import streamlit as st 
import open_clip

import torch

@st.cache_resource
def load_clip_model():

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32",
        pretrained="openai"
    )

    model = model.to(device)

    return model, preprocess, device