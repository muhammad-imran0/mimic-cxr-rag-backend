from qdrant_client import QdrantClient

from config import QDRANT_API_KEY, QDRANT_URL

_client = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30.0)
    return _client


def close_qdrant_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None
