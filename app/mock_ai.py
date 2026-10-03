"""Canned responses used when FITBUDDY_MOCK_AI=true (demos, offline work, automated tests)."""

_FOCUS = ["Full Body", "Upper Body", "Cardio", "Lower Body", "Core & Mobility", "Active Recovery", "Rest Day"]


def mock_workout_plan(age: int, weight: float, goal: str, intensity: str) -> str:
    sets = {"low": "2 sets x 10 reps", "medium": "3 sets x 12 reps", "high": "4 sets x 12 reps"}[intensity]
    rest = {"low": "90 sec", "medium": "60 sec", "high": "45 sec"}[intensity]
    blocks = []
    for i, focus in enumerate(_FOCUS, start=1):
        if focus == "Rest Day":
            blocks.append(f"Day {i} - {focus}\nRest or a 20-30 minute easy walk. Sleep 7-9 hours.")
            continue
        blocks.append(
            f"Day {i} - {focus}\n"
            "Warm-up (5-10 min): light jog, arm circles, bodyweight squats\n"
            "Main workout:\n"
            f"- Exercise A: {sets}, rest {rest}\n"
            f"- Exercise B: {sets}, rest {rest}\n"
            f"- Exercise C: {sets}, rest {rest}\n"
            "Cooldown (5 min): slow walk and static stretches"
        )
    blocks.append(f"[MOCK PLAN for goal '{goal}', {intensity} intensity, age {age}, {weight} kg]")
    return "\n\n".join(blocks)


def mock_nutrition_tip(goal: str) -> str:
    return f"[MOCK TIP] For {goal}: eat protein with every meal and drink water through the day."


def mock_updated_plan(current_plan: str, feedback: str) -> str:
    return f"{current_plan}\n\nUPDATED (mock) - changes applied for feedback: {feedback}"
