"""FitBuddy - AI Fitness Plan Generator. Run with:  uvicorn app.main:app --reload"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import STATIC_DIR, settings
from .database import init_db
from .routes import router

logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger("fitbuddy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    if settings.mock_ai:
        logger.warning("FITBUDDY_MOCK_AI is on: Gemini is NOT being called.")
    elif not settings.google_api_key:
        logger.warning("GOOGLE_API_KEY is not set. Add it to .env or generation will fail.")
    yield


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="Personalized 7-day workout plans and nutrition tips powered by Google Gemini.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(router)
