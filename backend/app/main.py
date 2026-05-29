from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .pipeline import (
    create_batch,
    dedupe_batch,
    export_adi,
    get_batch,
    init_db,
    normalize_batch,
    resolve_conflict,
)
from .messages import message


def _frontend_dist() -> Path | None:
    """Locate the built SPA (PyInstaller bundle when frozen, else frontend/dist)."""
    if getattr(sys, "frozen", False):
        candidate = Path(getattr(sys, "_MEIPASS", ".")) / "frontend_dist"
    else:
        candidate = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    return candidate if (candidate / "index.html").exists() else None


class MappingRequest(BaseModel):
    mapping: dict[str, str] = Field(default_factory=dict)
    inference: dict[str, bool] = Field(default_factory=dict)


class DedupeRequest(BaseModel):
    tolerance_minutes: int = 15


class ResolveRequest(BaseModel):
    strategy: str = "merge"
    field_choices: dict[str, str] = Field(default_factory=dict)


app = FastAPI(title="6SNT.ADIF-HUB API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ready", "service": "6SNT.ADIF-HUB"}


@app.post("/api/imports")
async def import_files(files: list[UploadFile] = File(...)) -> dict:
    if not files:
        raise HTTPException(status_code=400, detail=message("no_files_uploaded"))
    payload = [(file.filename or "upload.bin", await file.read()) for file in files]
    try:
        return create_batch(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/imports/{batch_id}")
def read_import(batch_id: str) -> dict:
    try:
        return get_batch(batch_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=message("batch_not_found")) from exc


@app.post("/api/imports/{batch_id}/mapping")
def apply_mapping(batch_id: str, request: MappingRequest) -> dict:
    try:
        return normalize_batch(batch_id, request.mapping, request.inference)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=message("batch_not_found")) from exc


@app.post("/api/imports/{batch_id}/normalize")
def normalize_import(batch_id: str, request: MappingRequest) -> dict:
    return apply_mapping(batch_id, request)


@app.post("/api/imports/{batch_id}/dedupe")
def dedupe_import(batch_id: str, request: DedupeRequest) -> dict:
    try:
        return dedupe_batch(batch_id, request.tolerance_minutes)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=message("batch_not_found")) from exc


@app.post("/api/imports/{batch_id}/conflicts/{conflict_id}/resolve")
def resolve_import_conflict(
    batch_id: str, conflict_id: str, request: ResolveRequest
) -> dict:
    try:
        return resolve_conflict(
            batch_id, conflict_id, request.strategy, request.field_choices
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=message("conflict_not_found")) from exc


@app.get("/api/exports/{batch_id}.adi")
def download_export(batch_id: str) -> FileResponse:
    try:
        path = export_adi(batch_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=message("batch_not_found")) from exc
    return FileResponse(path, media_type="text/plain", filename=f"{batch_id}.adi")


# Serve the built SPA last so /api/* routes keep precedence. When the frontend
# has not been built (pure-dev backend) this mount is simply skipped.
_dist = _frontend_dist()
if _dist is not None:
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="frontend")
