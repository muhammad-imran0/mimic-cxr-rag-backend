import asyncio
import io
import json

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response, StreamingResponse
from PIL import Image, UnidentifiedImageError

from embedder import embed_image
from cases import case_to_png_bytes, get_case
from retriever import search_similar

router = APIRouter(prefix="/api/v1", tags=["RAG"])


def with_image_url(results: list[dict]) -> list[dict]:
    for row in results:
        case_id = row["case_id"]
        row["image_url"] = f"/api/v1/cases/{case_id}/image"
    return results


def read_image(file_bytes: bytes) -> Image.Image:
    try:
        return Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=422, detail="File is not a valid image.") from exc


async def diagnosis_stream(image: Image.Image):
    yield json.dumps({"type": "status", "content": "Encoding image..."}) + "\n"
    vector = embed_image(image)

    yield json.dumps({"type": "status", "content": "Searching similar cases..."}) + "\n"
    matches = with_image_url(search_similar(vector, limit=3))
    yield json.dumps({
        "type": "retrieval_context",
        "count": len(matches),
        "records": matches,
    }) + "\n"

    report = ["\n--- CLINICAL REPORT ---\n\n", "RETRIEVED SIMILAR CASES:\n"]
    if matches:
        for i, case in enumerate(matches, 1):
            report.append(
                f"  [{i}] case_id={case['case_id']} score={case['score']:.4f}\n"
                f"      impression: {case['impression'][:200]}\n"
            )
    else:
        report.append("  No matches found.\n")

    for line in report:
        yield json.dumps({"type": "token", "content": line}) + "\n"
        await asyncio.sleep(0.03)

    yield json.dumps({"type": "done"}) + "\n"


@router.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    image = read_image(image_bytes)
    return StreamingResponse(diagnosis_stream(image), media_type="application/x-ndjson")


@router.get("/search/text")
async def search_by_text(q: str, limit: int = 5):
    from embedder import embed_text

    vector = embed_text(q)
    return {"query": q, "results": with_image_url(search_similar(vector, limit=limit))}


@router.post("/search/image")
async def search_by_image(file: UploadFile = File(...), limit: int = 5):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    image = read_image(image_bytes)
    vector = embed_image(image)
    return {"results": with_image_url(search_similar(vector, limit=limit))}


@router.get("/cases/{case_id}")
def get_case_metadata(case_id: int):
    try:
        case = get_case(case_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "case_id": case["case_id"],
        "findings": case["findings"],
        "impression": case["impression"],
        "source": case["source"],
        "image_url": f"/api/v1/cases/{case_id}/image",
    }


@router.get("/cases/{case_id}/image")
def get_case_image(case_id: int):
    try:
        png_bytes = case_to_png_bytes(case_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600"},
    )
