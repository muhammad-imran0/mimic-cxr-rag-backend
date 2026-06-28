FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0.0 \
    && rm -rf /var/lib/apt/lists/*

# CPU-only PyTorch (avoids ~2GB of CUDA packages that cause OOM on Render)
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HF_HOME=/app/.cache/huggingface
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

EXPOSE 7860

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1
