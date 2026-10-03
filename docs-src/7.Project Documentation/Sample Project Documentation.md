# Sample Project Documentation

{{HEADER:2 Marks}}

## Project Name
**FitBuddy: AI Fitness Plan Generator**

## Objective
FitBuddy is an AI-assisted fitness planning application that converts a user's profile, fitness goal, and workout intensity into a personalized seven-day workout plan. It also provides a nutrition/recovery tip and allows the user to submit natural-language feedback to refine the generated plan.

## Main Modules
- FastAPI web/API layer
- Pydantic input validation
- SQLAlchemy/SQLite persistence
- Gemini workout-plan generation
- Gemini nutrition/recovery-tip generation
- Feedback-based workout-plan revision
- Jinja2 web interface
- Automated tests and mock-AI fallback

## Typical User Flow
1. Enter the user's name, user ID, age, weight, fitness goal, and workout intensity.
2. Generate a personalized seven-day workout plan.
3. Review the generated plan together with the nutrition/recovery tip.
4. Submit natural-language feedback to request changes.
5. View the revised plan while retaining the original plan version.
6. Inspect saved users and plans from the All Users view.

## Technical Architecture
The application uses a FastAPI backend, Jinja2 templates for the web interface, Pydantic for request validation, SQLAlchemy with SQLite for persistence, and Google Gemini for AI-generated fitness content. A mock-AI/fallback path is available when the external AI service is unavailable. The API documentation is available through FastAPI's `/docs` endpoint.

## Pre-requisites
1. Python 3.10+
2. FastAPI, Uvicorn and the packages listed in `requirements.txt`
3. Google Gemini API key configured through `.env` when live AI generation is required
4. Git and a GitHub account for repository management
5. A modern web browser

## Project Workflow

| Milestone | Activities | Where in the code |
|---|---|---|
| 1. Project setup and validation | Configure environment, validate profile fields, prepare database and application routes | `app/config.py`, `app/schemas.py`, `app/database.py`, `app/routes.py` |
| 2. AI generation | Build prompts and generate seven-day workout plans and nutrition/recovery tips | `app/gemini_generator.py`, `app/gemini_flash_generator.py`, `app/gemini_client.py` |
| 3. Backend integration | Connect routes, persistence, feedback revision and result rendering | `app/main.py`, `app/routes.py`, `app/updated_plan.py` |
| 4. UI development | Build the FitBuddy form, feedback page, result page and All Users view | `app/templates/`, `app/static/css/style.css` |
| 5. Testing and reliability | Validate routes, input handling, persistence and AI fallback behavior | `tests/`, `tests/perf_load.py` |

## Milestone 1: Project Setup and Workout Input

The user starts from the **New Plan** interface. The form collects the name, unique user ID, age, weight, fitness goal and workout intensity before sending the request to the backend.

![New workout plan form](assets/01_workout_plan_form.jpeg)

**Figure 1 — New Workout Plan Form.** The FitBuddy landing interface captures the user's basic fitness profile and preferences before generating the seven-day plan. The User ID is used to associate feedback and saved plan information with the same user.

## Milestone 2: AI-Generated Workout Plan

After successful generation, FitBuddy presents the personalized seven-day workout schedule, including the selected goal, intensity, user details, warm-up, main workout, and cooldown information.

![Generated workout plan](assets/05_generated_workout_plan.jpeg)

**Figure 2 — Generated Seven-Day Workout Plan.** This screen demonstrates the primary AI-assisted output of FitBuddy: a structured weekly workout plan with day-wise workout content and plan metadata.

## Milestone 3: Nutrition / Recovery and Feedback-Based Revision

The result interface provides a nutrition/recovery tip and a feedback form. The user can describe changes such as increasing cardio or adding more rest days, after which the application sends the feedback for plan revision.

![Nutrition and feedback section](assets/04_nutrition_and_feedback.jpeg)

**Figure 3 — Nutrition / Recovery Tip and Feedback Revision.** The screen combines a goal-aware recovery/nutrition tip with the natural-language feedback workflow used to refine an existing plan.

The dedicated feedback page provides a focused interface for entering the User ID and requested changes.

![Feedback form](assets/02_feedback_form.jpeg)

**Figure 4 — Feedback Form.** The user supplies the saved User ID and describes the desired changes. FitBuddy uses this feedback to produce an updated version of the workout plan while retaining the original version.

## Milestone 4: Saved Users and Plan Management

The All Users view provides a consolidated record of registered users and their plan information. It shows profile attributes, fitness goal, intensity, original plan availability, updated-plan status, feedback and a delete action.

![All Users view](assets/03_all_users_view.jpeg)

**Figure 5 — All Users View.** This screen demonstrates the application's persistence and administrative-style view for inspecting saved FitBuddy users and their associated plan/revision state.

## Milestone 5: Testing and Demonstration Evidence

The five screenshots above are actual screenshots supplied by the FitBuddy project team from the implemented application UI. They are included as visual evidence for the main workflow: plan creation, AI-generated output, nutrition/recovery guidance, feedback-based revision, and saved-user management.

The screenshots correspond to the current FitBuddy interface and are stored in `docs-src/assets/` so that the editable Markdown documentation and generated PDF documentation use the same evidence set.

## Limitation
Fitness content is AI-generated general guidance and is not a substitute for medical advice, diagnosis, or professional fitness supervision.
