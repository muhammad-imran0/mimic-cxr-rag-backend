import torch
import torch.nn.functional as F
import open_clip
from PIL import Image

from config import MODEL_ID

_model = None
_preprocess = None
_tokenizer = None
_device = None


def get_embedder():
    global _model, _preprocess, _tokenizer, _device

    if _model is None:
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _model, _, _preprocess = open_clip.create_model_and_transforms(MODEL_ID)
        _tokenizer = open_clip.get_tokenizer(MODEL_ID)
        _model.to(_device).eval()

    return _model, _preprocess, _tokenizer, _device


def embed_image(image: Image.Image) -> list[float]:
    model, preprocess, _, device = get_embedder()
    if image.mode != "RGB":
        image = image.convert("RGB")

    tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        features = model.encode_image(tensor)
        features = F.normalize(features, p=2, dim=-1)
    return features.squeeze(0).cpu().tolist()


def embed_text(text: str) -> list[float]:
    model, _, tokenizer, device = get_embedder()
    tokens = tokenizer([text]).to(device)
    with torch.no_grad():
        features = model.encode_text(tokens)
        features = F.normalize(features, p=2, dim=-1)
    return features.squeeze(0).cpu().tolist()
