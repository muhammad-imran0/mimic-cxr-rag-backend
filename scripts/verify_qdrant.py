"""Check Qdrant connection and collection size."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import QDRANT_COLLECTION, QDRANT_URL
from qdrant import get_qdrant_client


def main():
    print(f"Qdrant: {QDRANT_URL}")
    print(f"Collection: {QDRANT_COLLECTION}")

    client = get_qdrant_client()
    names = [c.name for c in client.get_collections().collections]
    print(f"Collections: {names}")

    if QDRANT_COLLECTION not in names:
        print("Collection not found. Run the ingestion pipeline first.")
        return

    info = client.get_collection(QDRANT_COLLECTION)
    print(f"Points: {info.points_count}")
    print("OK")


if __name__ == "__main__":
    main()
