from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="ComicCraft API", version="1.0.0", description="AI comic story creator")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "ComicCraft"}
