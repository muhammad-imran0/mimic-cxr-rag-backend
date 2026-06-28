FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HF_HOME=/app/.cache/huggingface
ENV PORT=8000

# Pre-cache BiomedCLIP weights at build time (faster cold starts)
RUN python -c "\
import open_clip; \
open_clip.create_model_and_transforms(\
'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224'\
)"

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
