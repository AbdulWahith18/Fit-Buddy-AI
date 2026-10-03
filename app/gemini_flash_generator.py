"""Nutrition / recovery tip generation (Gemini Flash tier)."""
import random

from .config import settings
from .gemini_client import generate_text
from .mock_ai import mock_nutrition_tip

SYSTEM_INSTRUCTION = (
    "You are a sports nutrition and recovery coach. Reply with plain text only, no markdown, no lists."
)

# Used only if the AI call fails, so the result page still has a useful tip.
FALLBACK_TIPS = {
    "weight loss": "Build each meal around lean protein and vegetables, and drink water before meals to stay full.",
    "muscle gain": "Include protein in your post-workout meal and eat in a small calorie surplus.",
    "flexibility": "Stretch when your muscles are warm and stay hydrated to keep tissue supple.",
    "general wellness": "Aim for a balanced plate, 7-9 hours of sleep and regular water intake.",
}
DEFAULT_TIP = "Prioritize protein in every meal, drink enough water and sleep 7-9 hours for recovery."


def get_fallback_tip(goal: str) -> str:
    key = goal.strip().lower()
    for name, tip in FALLBACK_TIPS.items():
        if name in key or key in name:
            return tip
    return DEFAULT_TIP


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """Return one concise nutrition or recovery tip (max ~2 sentences) for the goal."""
    if settings.mock_ai:
        return mock_nutrition_tip(goal)

    angle = random.choice(["nutrition", "hydration", "recovery", "meal timing"])
    prompt = (
        f"Give ONE concise, practical {angle} tip for someone whose fitness goal is '{goal}'. "
        "Maximum 2 sentences. Be specific and actionable."
    )
    return generate_text(prompt, "flash", system_instruction=SYSTEM_INSTRUCTION, temperature=0.9)
