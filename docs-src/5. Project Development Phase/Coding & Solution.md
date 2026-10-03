# Coding & Solution

{{HEADER:4 Marks}}

## Milestone 1: Backend Foundation

- `app/main.py` creates the FastAPI application, mounts CSS/static content and initializes the database.
- `app/routes.py` contains the HTML routes and JSON API.
- `app/schemas.py` validates username, user ID, age, weight, goal, intensity and feedback.
- `app/database.py` persists users and plans using SQLAlchemy/SQLite.

## Milestone 2: AI Integration

- `gemini_client.py` provides shared Gemini client behavior.
- `gemini_generator.py` generates seven-day workout plans.
- `gemini_flash_generator.py` generates nutrition/recovery tips.
- `updated_plan.py` revises a plan from natural-language feedback.
- `mock_ai.py` supplies deterministic responses for testing/demo mode.

## Milestone 3: User Interface

The supplied application provides Jinja2 pages for input, results, feedback and the all-users/admin view.

## Milestone 4: API and Persistence

The API includes `/api/generate-workout`, `/api/submit-feedback`, `/api/nutrition-tip`, `/api/users`, `/api/users/{user_id}` and `/health`.

## Milestone 5: Testing and Reliability

The project includes pytest tests, isolated test database setup, mock AI, AI error handling, model fallback logic and a static fallback for nutrition tips.

## Team implementation areas

| Member | Main development contribution |
|---|---|
| Abdul Wahith M | FastAPI architecture, Gemini client integration and API flow |
| Kamalesh T | Templates, CSS and user-facing result/feedback/admin views |
| Bilu Besto H | Pydantic validation, feedback revision and failure handling |
| Bharath Jeyakkumar S | Automated tests and test verification |
| Prasannavelan K | SQLAlchemy persistence, user/plan management and setup/demo support |
