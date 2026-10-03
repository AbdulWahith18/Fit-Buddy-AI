"""Central configuration. Values come from environment variables / .env."""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent          # .../fitbuddy/app
PROJECT_ROOT = BASE_DIR.parent                      # .../fitbuddy
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

load_dotenv(PROJECT_ROOT / ".env")


def _csv(value: str) -> List[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def _bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    google_api_key: str = field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
    )
    pro_model: str = field(default_factory=lambda: os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview"))
    pro_fallbacks: List[str] = field(
        default_factory=lambda: _csv(os.getenv("GEMINI_PRO_FALLBACKS", "gemini-pro-latest,gemini-2.5-pro"))
    )
    flash_model: str = field(default_factory=lambda: os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash"))
    flash_fallbacks: List[str] = field(
        default_factory=lambda: _csv(os.getenv("GEMINI_FLASH_FALLBACKS", "gemini-flash-latest,gemini-2.5-flash"))
    )
    allow_flash_fallback: bool = field(
        default_factory=lambda: _bool(os.getenv("GEMINI_ALLOW_FLASH_FALLBACK", "true"))
    )
    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'fitbuddy.db'}")
    )
    mock_ai: bool = field(default_factory=lambda: _bool(os.getenv("FITBUDDY_MOCK_AI", "false")))
    request_timeout_ms: int = 120_000

    def models_for(self, tier: str) -> List[str]:
        primary, fallbacks = (
            (self.pro_model, self.pro_fallbacks) if tier == "pro" else (self.flash_model, self.flash_fallbacks)
        )
        ordered = [primary, *fallbacks]
        return list(dict.fromkeys(m for m in ordered if m))  # de-duplicate, keep order


settings = Settings()
