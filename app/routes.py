"""All FitBuddy routes: HTML pages (Jinja2) and a small JSON API."""
import logging
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .config import TEMPLATE_DIR
from .database import (
    Plan,
    User,
    delete_user,
    get_all_plans,
    get_all_users,
    get_db,
    get_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
    update_tip,
)
from .gemini_client import AIServiceError
from .gemini_flash_generator import generate_nutrition_tip_with_flash, get_fallback_tip
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, PlanOut, TipOut, UserInput
from .updated_plan import update_workout_plan

logger = logging.getLogger("fitbuddy.routes")

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

GOALS = ["Weight Loss", "Muscle Gain", "Flexibility", "General Wellness", "Endurance"]
INTENSITIES = ["low", "medium", "high"]


# ======================================================================
# Shared logic (used by both the HTML routes and the JSON API)
# ======================================================================
class PlanNotFound(Exception):
    pass


def _safe_tip(goal: str) -> Tuple[str, Optional[str]]:
    """Get a Flash tip; fall back to a static tip so a tip failure never blocks the plan."""
    try:
        return generate_nutrition_tip_with_flash(goal), None
    except AIServiceError as exc:
        logger.warning("Nutrition tip failed, using fallback: %s", exc)
        return get_fallback_tip(goal), "The AI tip service was unavailable, so a general tip is shown."


def create_plan(db: Session, data: UserInput) -> Tuple[User, Plan, Optional[str]]:
    workout = generate_workout_gemini(data.age, data.weight, data.goal, data.intensity)
    tip, note = _safe_tip(data.goal)
    user = save_user(db, data)
    plan = save_plan(db, data.user_id, workout, tip)
    return user, plan, note


def revise_plan(db: Session, req: FeedbackRequest) -> Tuple[User, Plan]:
    user = get_user(db, req.user_id)
    plan = get_plan(db, req.user_id)
    if user is None or plan is None:
        raise PlanNotFound(f"No plan found for user ID '{req.user_id}'. Generate a plan first.")
    current = plan.updated_plan or plan.original_plan  # successive feedback builds on the latest version
    revised = update_workout_plan(current, req.feedback, user.goal, user.intensity)
    try:
        tip: Optional[str] = generate_nutrition_tip_with_flash(user.goal)
    except AIServiceError:
        tip = None  # keep the previous tip
    plan = update_plan(db, req.user_id, revised, req.feedback, tip)
    return user, plan


def _plan_out(user: User, plan: Optional[Plan]) -> PlanOut:
    return PlanOut(
        user_id=user.user_id,
        username=user.username,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
        original_plan=plan.original_plan if plan else None,
        updated_plan=plan.updated_plan if plan else None,
        feedback=plan.feedback if plan else None,
        nutrition_tip=plan.nutrition_tip if plan else None,
    )


def _error_list(exc: ValidationError) -> List[str]:
    out = []
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"]) or "input"
        out.append(f"{field}: {err['msg']}")
    return out


# ======================================================================
# Template helpers
# ======================================================================
def _index(request: Request, form: Optional[dict] = None, errors: Optional[List[str]] = None, status: int = 200):
    return templates.TemplateResponse(
        request, "index.html",
        {"goals": GOALS, "intensities": INTENSITIES, "form": form or {}, "errors": errors or []},
        status_code=status,
    )


def _feedback_page(request: Request, user_id: str = "", feedback: str = "",
                   errors: Optional[List[str]] = None, status: int = 200):
    return templates.TemplateResponse(
        request, "feedback.html",
        {"user_id": user_id, "feedback": feedback, "errors": errors or []},
        status_code=status,
    )


def _result(request: Request, user: User, plan: Plan, message: Optional[str] = None,
            error: Optional[str] = None, notice: Optional[str] = None, status: int = 200):
    return templates.TemplateResponse(
        request, "result.html",
        {
            "user": user,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": plan.updated_plan or plan.original_plan,
            "original_plan": plan.original_plan,
            "is_updated": bool(plan.updated_plan),
            "last_feedback": plan.feedback,
            "nutrition_tip": plan.nutrition_tip,
            "message": message,
            "error": error,
            "notice": notice,
        },
        status_code=status,
    )


# ======================================================================
# HTML routes
# ======================================================================
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return _index(request)


@router.get("/feedback", response_class=HTMLResponse, include_in_schema=False)
def feedback_page(request: Request, user_id: str = ""):
    return _feedback_page(request, user_id=user_id)


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: str = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    form = {"username": username, "user_id": user_id, "age": age,
            "weight": weight.replace(",", "."), "goal": goal, "intensity": intensity}
    try:
        data = UserInput(**form)
    except ValidationError as exc:
        return _index(request, form, _error_list(exc), status=422)
    try:
        user, plan, note = create_plan(db, data)
    except AIServiceError as exc:
        return _index(request, form, [str(exc)], status=502)
    return _result(request, user, plan, message="Your 7-day plan is ready.", notice=note)


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        req = FeedbackRequest(user_id=user_id, feedback=feedback)
    except ValidationError as exc:
        return _feedback_page(request, user_id, feedback, _error_list(exc), status=422)
    try:
        user, plan = revise_plan(db, req)
    except PlanNotFound as exc:
        return _feedback_page(request, req.user_id, req.feedback, [str(exc)], status=404)
    except AIServiceError as exc:
        user, plan = get_user(db, req.user_id), get_plan(db, req.user_id)
        return _result(request, user, plan, error=str(exc), status=502)
    return _result(request, user, plan, message="Plan updated! Your feedback has been applied.")


@router.post("/nutrition-tip", response_class=HTMLResponse)
def new_tip(request: Request, user_id: str = Form(...), db: Session = Depends(get_db)):
    user, plan = get_user(db, user_id.strip()), get_plan(db, user_id.strip())
    if user is None or plan is None:
        return _feedback_page(request, user_id, errors=[f"No plan found for user ID '{user_id}'."], status=404)
    try:
        tip = generate_nutrition_tip_with_flash(user.goal)
        plan = update_tip(db, user.user_id, tip)
    except AIServiceError as exc:
        return _result(request, user, plan, error=str(exc), status=502)
    return _result(request, user, plan, message="Here is a fresh tip.")


@router.get("/result/{user_id}", response_class=HTMLResponse, include_in_schema=False)
def view_result(request: Request, user_id: str, db: Session = Depends(get_db)):
    user, plan = get_user(db, user_id), get_plan(db, user_id)
    if user is None or plan is None:
        return _index(request, errors=[f"No saved plan for user ID '{user_id}'."], status=404)
    return _result(request, user, plan)


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    plans = get_all_plans(db)
    return templates.TemplateResponse(request, "all_users.html", {"users": users, "plans": plans})


@router.post("/delete-user", include_in_schema=False)
def remove_user(user_id: str = Form(...), db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)


@router.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


# ======================================================================
# JSON API (try these in /docs)
# ======================================================================
@router.post("/api/generate-workout", response_model=PlanOut, tags=["api"])
def api_generate(data: UserInput, db: Session = Depends(get_db)):
    try:
        user, plan, _ = create_plan(db, data)
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return _plan_out(user, plan)


@router.post("/api/submit-feedback", response_model=PlanOut, tags=["api"])
def api_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    try:
        user, plan = revise_plan(db, req)
    except PlanNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return _plan_out(user, plan)


@router.get("/api/nutrition-tip", response_model=TipOut, tags=["api"])
def api_tip(goal: str = Query(..., min_length=2, max_length=60)):
    tip, _ = _safe_tip(goal)
    return TipOut(goal=goal, nutrition_tip=tip)


@router.get("/api/users", response_model=List[PlanOut], tags=["api"])
def api_users(db: Session = Depends(get_db)):
    plans = get_all_plans(db)
    return [_plan_out(u, plans.get(u.user_id)) for u in get_all_users(db)]


@router.get("/api/users/{user_id}", response_model=PlanOut, tags=["api"])
def api_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _plan_out(user, get_plan(db, user_id))
