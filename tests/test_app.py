"""End-to-end tests (Gemini is mocked via FITBUDDY_MOCK_AI=true in conftest.py)."""
from unittest.mock import patch

from app.gemini_client import AIServiceError, clean_text

from .conftest import FORM


def test_home_page(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Generate plan" in r.text


def test_health_and_docs(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200


def test_static_css(client):
    assert client.get("/static/css/style.css").status_code == 200


# Scenario 1: generate a plan
def test_generate_workout(client):
    r = client.post("/generate-workout", data=FORM)
    assert r.status_code == 200
    assert "Day 1" in r.text and "Day 7" in r.text
    assert "Alex" in r.text
    assert "protein" in r.text.lower()  # mock nutrition tip


def test_generate_workout_validation_error(client):
    r = client.post("/generate-workout", data={**FORM, "age": "5"})
    assert r.status_code == 422
    assert "age" in r.text.lower()


def test_generate_workout_bad_user_id(client):
    r = client.post("/generate-workout", data={**FORM, "user_id": "bad id!"})
    assert r.status_code == 422


def test_weight_decimal_comma(client):
    r = client.post("/generate-workout", data={**FORM, "weight": "72,5"})
    assert r.status_code == 200


# Scenario 2: feedback updates the plan
def test_submit_feedback(client):
    client.post("/generate-workout", data=FORM)
    r = client.post("/submit-feedback", data={"user_id": "alex_01", "feedback": "More cardio please"})
    assert r.status_code == 200
    assert "Plan updated" in r.text
    assert "More cardio please" in r.text
    assert "Show original plan" in r.text


def test_feedback_unknown_user(client):
    r = client.post("/submit-feedback", data={"user_id": "ghost", "feedback": "more cardio"})
    assert r.status_code == 404
    assert "No plan found" in r.text


def test_feedback_too_short(client):
    client.post("/generate-workout", data=FORM)
    r = client.post("/submit-feedback", data={"user_id": "alex_01", "feedback": "x"})
    assert r.status_code == 422


# Scenario 3: nutrition tip
def test_new_tip_route(client):
    client.post("/generate-workout", data=FORM)
    r = client.post("/nutrition-tip", data={"user_id": "alex_01"})
    assert r.status_code == 200
    assert "fresh tip" in r.text


def test_api_tip(client):
    r = client.get("/api/nutrition-tip", params={"goal": "weight loss"})
    assert r.status_code == 200
    assert r.json()["nutrition_tip"]


# Scenario 4: admin dashboard
def test_view_all_users_and_delete(client):
    assert "No users yet" in client.get("/view-all-users").text
    client.post("/generate-workout", data=FORM)
    client.post("/submit-feedback", data={"user_id": "alex_01", "feedback": "add yoga"})
    page = client.get("/view-all-users").text
    assert "alex_01" in page and "add yoga" in page and "Alex" in page
    r = client.post("/delete-user", data={"user_id": "alex_01"}, follow_redirects=True)
    assert "No users yet" in r.text


def test_regenerate_same_user_replaces_plan(client):
    client.post("/generate-workout", data=FORM)
    client.post("/submit-feedback", data={"user_id": "alex_01", "feedback": "add yoga"})
    client.post("/generate-workout", data={**FORM, "goal": "Flexibility"})
    data = client.get("/api/users/alex_01").json()
    assert data["goal"] == "Flexibility"
    assert data["updated_plan"] is None


# JSON API
def test_api_flow(client):
    body = {"username": "Sam", "user_id": "sam", "age": 30, "weight": 80, "goal": "weight loss", "intensity": "HIGH"}
    r = client.post("/api/generate-workout", json=body)
    assert r.status_code == 200
    assert r.json()["intensity"] == "high"
    r = client.post("/api/submit-feedback", json={"user_id": "sam", "feedback": "include more rest days"})
    assert r.status_code == 200
    assert r.json()["updated_plan"]
    assert len(client.get("/api/users").json()) == 1
    assert client.get("/api/users/nobody").status_code == 404


def test_api_validation(client):
    r = client.post("/api/generate-workout", json={"username": "x"})
    assert r.status_code == 422


# AI failure handling
def test_ai_failure_shows_friendly_error(client):
    with patch("app.routes.generate_workout_gemini", side_effect=AIServiceError("Gemini is down")):
        r = client.post("/generate-workout", data=FORM)
    assert r.status_code == 502
    assert "Gemini is down" in r.text
    assert 'value="alex_01"' in r.text  # form is preserved


def test_tip_failure_does_not_block_plan(client):
    with patch("app.routes.generate_nutrition_tip_with_flash", side_effect=AIServiceError("flash down")):
        r = client.post("/generate-workout", data=FORM)
    assert r.status_code == 200
    assert "general tip is shown" in r.text


def test_clean_text():
    raw = "```\n**Day 1** - Legs\n# Header\n* item\n```"
    out = clean_text(raw)
    assert "**" not in out and "```" not in out and "- item" in out
