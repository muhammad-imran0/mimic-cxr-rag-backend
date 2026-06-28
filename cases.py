from io import BytesIO
from pathlib import Path

import pyarrow.parquet as pq
from PIL import Image

from config import MIMIC_DATA_DIR


def to_pil(img) -> Image.Image:
    if isinstance(img, Image.Image):
        return img.convert("RGB")
    if isinstance(img, bytes):
        return Image.open(BytesIO(img)).convert("RGB")
    if isinstance(img, dict) and "bytes" in img:
        return Image.open(BytesIO(img["bytes"])).convert("RGB")
    raise TypeError(f"Unsupported image type: {type(img)}")


def parquet_files():
    if not MIMIC_DATA_DIR.exists():
        return []
    return sorted(MIMIC_DATA_DIR.glob("*.parquet"))


def get_case(case_id: int) -> dict:
    seen = 0
    for path in parquet_files():
        table = pq.read_table(path, columns=["image", "findings", "impression"])
        for row in table.to_pylist():
            if seen == case_id:
                return {
                    "case_id": case_id,
                    "image": to_pil(row["image"]),
                    "findings": row.get("findings") or "",
                    "impression": row.get("impression") or "",
                    "source": "mimic-cxr",
                }
            seen += 1

    raise KeyError(f"case_id {case_id} not found ({seen} cases in dataset)")


def case_to_png_bytes(case_id: int) -> bytes:
    image = get_case(case_id)["image"]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
