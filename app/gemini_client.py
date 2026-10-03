"""Thin wrapper around the Google Gen AI SDK (google-genai).

Responsibilities
- one shared client built from GOOGLE_API_KEY
- try the configured model first, then fallbacks (Google retires models often)
- retry transient errors (429 / 5xx) once
- turn every SDK failure into a single, user-friendly AIServiceError
"""
import logging
import re
import time
from functools import lru_cache
from typing import Iterator, List, Optional

from google import genai
from google.genai import errors, types

from .config import settings

logger = logging.getLogger("fitbuddy.ai")

# Names containing any of these are not text-generation chat models.
_EXCLUDE = (
    "image", "tts", "audio", "live", "embedding", "computer-use", "robotics",
    "native", "transcribe", "omni", "imagen", "veo", "lyria", "gemma", "learnlm", "aqa",
)


class AIServiceError(Exception):
    """Raised when Gemini cannot produce a usable answer. The message is safe to show to users."""


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    if not settings.google_api_key:
        raise AIServiceError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env, add your Gemini API key and restart the server."
        )
    return genai.Client(
        api_key=settings.google_api_key,
        http_options=types.HttpOptions(timeout=settings.request_timeout_ms),
    )


def _discover_models(tier: str) -> List[str]:
    """Ask the API which models this key can use (last resort when configured names 404)."""
    try:
        found = []
        for m in _client().models.list():
            name = (m.name or "").replace("models/", "")
            actions = getattr(m, "supported_actions", None) or []
            if actions and "generateContent" not in actions:
                continue
            if tier not in name or any(x in name for x in _EXCLUDE):
                continue
            if "lite" in name and tier == "flash":
                continue
            found.append(name)
        found.sort(key=lambda n: (("preview" in n), n))  # stable models first
        return found
    except Exception as exc:  # discovery is best-effort
        logger.warning("Model discovery failed: %s", exc)
        return []


def _candidates(tier: str) -> Iterator[str]:
    seen = set()
    for name in settings.models_for(tier):
        seen.add(name)
        yield name
    for name in _discover_models(tier):
        if name not in seen:
            seen.add(name)
            yield name
    if tier == "pro" and settings.allow_flash_fallback:
        logger.warning("No Pro model worked; falling back to Flash models for this request.")
        for name in settings.models_for("flash"):
            if name not in seen:
                seen.add(name)
                yield name


def clean_text(text: str) -> str:
    """Make model output safe for <pre> display: strip markdown fences/bold/headers."""
    text = re.sub(r"^```[a-zA-Z]*\n?|\n?```$", "", text.strip())
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\*\s+", "- ", text, flags=re.MULTILINE)
    return text.strip()


def _call(model: str, prompt: str, system_instruction: Optional[str], temperature: float) -> str:
    response = _client().models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise AIServiceError("Gemini returned an empty response (it may have been blocked). Please try again.")
    return clean_text(text)


def generate_text(
    prompt: str,
    tier: str,
    *,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    """Generate text with the 'pro' or 'flash' tier, with fallbacks and one retry."""
    last_error = "No Gemini model could be reached."
    for model in _candidates(tier):
        for attempt in (1, 2):
            try:
                logger.info("Gemini call: model=%s tier=%s attempt=%d", model, tier, attempt)
                return _call(model, prompt, system_instruction, temperature)
            except AIServiceError:
                raise
            except errors.APIError as exc:
                code = getattr(exc, "code", None)
                detail = getattr(exc, "message", None) or str(exc)
                logger.warning("Gemini error on %s: %s %s", model, code, detail[:200])
                if code in (401, 403) or "API key" in detail:
                    raise AIServiceError(
                        "Gemini rejected the API key. Check GOOGLE_API_KEY in your .env file."
                    ) from exc
                if code in (429, 500, 503, 504) and attempt == 1:
                    time.sleep(2)
                    continue  # retry same model once
                last_error = f"{model}: {code} {detail[:160]}"
                break  # next model
            except Exception as exc:  # network, timeout, etc.
                logger.warning("Gemini call failed on %s: %s", model, exc)
                last_error = f"{model}: {exc}"
                break
    raise AIServiceError(
        "Gemini could not generate a response. Check your API key, quota and model names "
        f"(run scripts/list_models.py). Last error: {last_error}"
    )
