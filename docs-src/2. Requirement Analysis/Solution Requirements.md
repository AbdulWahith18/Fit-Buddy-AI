# Solution Requirements

{{HEADER:4 Marks}}

## Step 1: Functional Requirements (FR)

| S.No | Requirement Category | Requirement Description | Priority |
|---|---|---|---|
| 1 | User Input | Accept username, user ID, age, weight, fitness goal and intensity | High |
| 2 | Validation | Enforce age, weight, string length, ID pattern and intensity constraints | High |
| 3 | AI Workout Generation | Generate a personalized seven-day workout plan using Gemini | High |
| 4 | Nutrition / Recovery | Generate a concise tip and use a fallback when the tip service fails | High |
| 5 | Persistence | Store users and plans using SQLAlchemy and SQLite | High |
| 6 | Feedback Revision | Revise the latest plan from natural-language feedback | High |
| 7 | Original Plan Preservation | Keep the original generated plan when a revised plan exists | High |
| 8 | Saved Result | Reopen a saved plan using user ID | Medium |
| 9 | Admin View | Display saved users/plans and support deletion | Medium |
| 10 | JSON API | Provide generation, feedback, nutrition and user retrieval endpoints | High |
| 11 | Health Endpoint | Provide `/health` for service status | Medium |
| 12 | Testability | Support mock-AI mode so automated tests do not require live Gemini calls | High |

## Step 2: Non-Functional Requirements

| Category | Requirement |
|---|---|
| Usability | Clear forms, results, feedback and error messages |
| Reliability | AI model fallbacks and friendly service errors |
| Maintainability | Separate configuration, validation, database, AI and routes |
| Testability | Mock AI and isolated SQLite test database |
| Portability | Python/FastAPI application suitable for local or container deployment |
| Security | API keys supplied through environment variables rather than source code |
