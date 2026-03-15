import open_clip


def load_clip_model():
    """
    Load CLIP model for multimodal embeddings
    """

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32",
        pretrained="openai"
    )

    tokenizer = open_clip.get_tokenizer("ViT-B-32")

    return model, preprocess, tokenizer