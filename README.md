---
title: MIMIC-CXR RAG API
emoji: 🩻
colorFrom: blue
colorTo: cyan
sdk: docker
app_port: 7860
---

# MIMIC-CXR RAG Backend

FastAPI service — BiomedCLIP image encoding + Qdrant vector retrieval.

## Secrets (Settings → Variables)

- `QDRANT_URL`
- `QDRANT_API_KEY`
- `QDRANT_COLLECTION` = `mimic_cxr_vectors`
- `CORS_ORIGINS` = `https://muhammad-imran0.github.io`

## Live URL

```
https://imranyasin7866-mimic-cxr-rag-api.hf.space/health
```
