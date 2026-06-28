# Deploy Backend Live (Render)

Frontend is on GitHub Pages. Backend goes on **Render** (Docker).

## 1. Push backend to GitHub

```bash
cd mimic-cxr-rag-backend
git add .
git commit -m "Add Docker deploy for Render"
git push origin main
```

## 2. Create Render service

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect repo: `muhammad-imran0/mimic-cxr-rag-backend`
3. Settings:
   - **Runtime:** Docker
   - **Plan:** Starter (512MB may be tight; use Standard 2GB if model fails to load)
   - **Health check path:** `/health`

## 3. Set environment variables on Render

| Key | Value |
|-----|-------|
| `QDRANT_URL` | Your Qdrant Cloud URL |
| `QDRANT_API_KEY` | Your Qdrant API key |
| `QDRANT_COLLECTION` | `mimic_cxr_vectors` |
| `CORS_ORIGINS` | `https://muhammad-imran0.github.io,http://localhost:5173` |

Copy values from your local `.env`.

## 4. Deploy

Render builds the Docker image and deploys. First build takes ~10–15 min (PyTorch + BiomedCLIP).

Your live URL will be something like:
```
https://mimic-cxr-rag-backend.onrender.com
```

Test:
```bash
curl https://YOUR-URL.onrender.com/health
```

## 5. Point frontend to live backend

Rebuild and redeploy the UI with your Render URL:

```bash
cd ../mimic-cxr-rag-web-ui
VITE_API_URL=https://YOUR-URL.onrender.com npm run deploy
```

## Notes

- **Qdrant Cloud** must already have vectors indexed (from pipeline repo).
- **Matched X-ray images** (`/cases/{id}/image`) need parquet data on the server. On Render, retrieval + reports work; images may not load unless you add persistent storage with the MIMIC parquet files.
- **Cold starts:** free/starter tier sleeps after inactivity; first request may take 30–60s.
- **RAM:** BiomedCLIP needs ~1–2 GB. If deploy crashes, upgrade Render plan to Standard (2 GB).
