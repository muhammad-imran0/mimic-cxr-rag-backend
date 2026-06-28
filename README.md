# MIMIC-CXR RAG Backend

**Author:** Muhammad Imran (u3004795)

FastAPI service for multimodal chest X-ray retrieval — upload an image or search by text, get similar MIMIC-CXR cases from Qdrant.

Vectors must be indexed first using the separate [`biomedclip-embedding-pipeline`](../biomedclip-embedding-pipeline) repo.

---

## Project layout

```
main.py         FastAPI app entry point
config.py       Environment settings
qdrant.py       Qdrant client
embedder.py     BiomedCLIP image/text encoding
retriever.py    Vector search
cases.py        Load X-ray images by case_id from parquet
routes.py       API endpoints

scripts/
  verify_qdrant.py   Check Qdrant connection + point count
```

---

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # same Qdrant credentials as pipeline

python3 scripts/verify_qdrant.py
python3 main.py
```

Server runs at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/diagnose` | Upload X-ray → streamed report + similar cases |
| GET | `/api/v1/search/text?q=...` | Text query → similar cases |
| POST | `/api/v1/search/image` | Upload X-ray → similar cases (JSON) |
| GET | `/api/v1/cases/{case_id}` | Case metadata (findings, impression) |
| GET | `/api/v1/cases/{case_id}/image` | X-ray PNG for a matched case |

**Example — text search:**
```bash
curl "http://localhost:8000/api/v1/search/text?q=pleural+effusion&limit=3"
```

**Example — view matched X-ray in browser:**
```
http://localhost:8000/api/v1/cases/0/image
http://localhost:8000/api/v1/cases/10529/image
```

**Example — image search:**
```bash
curl -F "file=@samples/sample_0000.png" http://localhost:8000/api/v1/search/image
```

---

## Environment (`.env`)

```bash
QDRANT_URL=https://YOUR-CLUSTER.cloud.qdrant.io
QDRANT_API_KEY=your-key
QDRANT_COLLECTION=mimic_cxr_vectors
MIMIC_DATA_DIR=../biomedclip-embedding-pipeline/data/mimic-cxr/data

PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```
