"""Check your Gemini API key and list the models it can use.

Run from the project root:   python scripts/list_models.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings  # noqa: E402
from app.gemini_client import AIServiceError, _client, generate_text  # noqa: E402


def main() -> int:
    if not settings.google_api_key:
        print("GOOGLE_API_KEY is not set. Create .env from .env.example first.")
        return 1

    print("Models available to your key (text generation):\n")
    try:
        for m in _client().models.list():
            actions = getattr(m, "supported_actions", None) or []
            if "generateContent" in actions:
                print("  ", (m.name or "").replace("models/", ""))
    except Exception as exc:
        print("Could not list models:", exc)
        return 1

    print("\nConfigured Pro   :", settings.models_for("pro"))
    print("Configured Flash :", settings.models_for("flash"))

    print("\nLive test (one short call per tier)...")
    for tier in ("flash", "pro"):
        try:
            reply = generate_text("Reply with the single word: ready", tier, temperature=0)
            print(f"  {tier:5} OK -> {reply[:40]!r}")
        except AIServiceError as exc:
            print(f"  {tier:5} FAILED -> {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
