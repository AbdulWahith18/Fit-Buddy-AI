"""7-day workout plan generation (Gemini Pro tier)."""
from .config import settings
from .gemini_client import generate_text
from .mock_ai import mock_workout_plan

SYSTEM_INSTRUCTION = (
    "You are FitBuddy, an experienced certified personal trainer. You write safe, practical, "
    "well-structured workout plans in plain text only. Never use markdown symbols such as ** or #."
)

PLAN_FORMAT = """Format the answer EXACTLY like this for each of the 7 days (plain text, no markdown):

Day 1 - <focus of the day>
Warm-up (5-10 min): <activities>
Main workout:
- <exercise>: <sets> x <reps or duration>, rest <seconds>
- <exercise>: <sets> x <reps or duration>, rest <seconds>
Cooldown/Recovery: <stretching or recovery tip>

Rules:
- Cover Day 1 through Day 7. Include at least one rest or active-recovery day.
- 3 to 6 exercises on each training day.
- Match the intensity: low = beginner friendly, medium = intermediate, high = advanced.
- Keep exercises appropriate for the person's age.
- Finish with one short line reminding the person to check with a doctor before starting if they have any medical condition."""


def generate_workout_gemini(age: int, weight: float, goal: str, intensity: str) -> str:
    """Return a structured 7-day workout plan as plain text."""
    if settings.mock_ai:
        return mock_workout_plan(age, weight, goal, intensity)

    prompt = (
        "Create a personalized 7-day workout plan for this person:\n"
        f"- Age: {age}\n"
        f"- Weight: {weight} kg\n"
        f"- Fitness goal: {goal}\n"
        f"- Preferred workout intensity: {intensity}\n\n"
        f"{PLAN_FORMAT}"
    )
    return generate_text(prompt, "pro", system_instruction=SYSTEM_INSTRUCTION, temperature=0.7)
