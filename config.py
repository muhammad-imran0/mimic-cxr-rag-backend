import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "mimic_cxr_vectors")

_default_cors = (
    "http://localhost:3000,"
    "http://localhost:5173,"
    "https://muhammad-imran0.github.io"
)
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_cors).split(",")
    if origin.strip()
]

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MODEL_ID = "hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224"

_default_data = ROOT.parent / "biomedclip-embedding-pipeline" / "data" / "mimic-cxr" / "data"
MIMIC_DATA_DIR = Path(os.getenv("MIMIC_DATA_DIR", _default_data))
