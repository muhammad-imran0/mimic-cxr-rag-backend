import asyncio
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, LOG_LEVEL
from qdrant import close_qdrant_client
from routes import router

load_dotenv()

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("mimic-cxr-rag")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MIMIC-CXR RAG backend (model loads on first request)...")
    yield
    close_qdrant_client()
    logger.info("Shutdown complete.")


app = FastAPI(title="MIMIC-CXR RAG API", version="1.0.0", lifespan=lifespan)

# Allow all origins for public API access on Hugging Face Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "mimic-cxr-rag-backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
