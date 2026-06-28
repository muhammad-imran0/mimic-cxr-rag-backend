from config import QDRANT_COLLECTION
from qdrant import get_qdrant_client


def search_similar(vector: list[float], limit: int = 5) -> list[dict]:
    client = get_qdrant_client()
    response = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=vector,
        limit=limit,
        with_payload=True,
    )

    results = []
    for point in response.points:
        payload = point.payload or {}
        results.append({
            "case_id": payload.get("case_id", point.id),
            "score": float(point.score),
            "findings": payload.get("findings", ""),
            "impression": payload.get("impression", ""),
            "source": payload.get("source", "mimic-cxr"),
        })
    return results
