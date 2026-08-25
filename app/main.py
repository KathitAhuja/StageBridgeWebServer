from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.services.script_service import ScriptService

app = FastAPI(title="Stage Bridge Embedded Server", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

script_service = ScriptService()

@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/v1/stream")
async def stream_theater_lines(lang: str = Query(...)):
    normalized_lang = lang.lower()
    if normalized_lang not in ["spanish", "es", "chinese", "zh"]:
        raise HTTPException(status_code=400, detail="Unsupported language selected.")

    return StreamingResponse(
        script_service.stream_script(language=normalized_lang, interval=2.0),
        media_type="text/event-stream"
    )