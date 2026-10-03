# Solution Architecture

{{HEADER:4 Marks}}

![Solution Architecture Diagram](assets/solution_architecture_diagram.png)

## Architectural components

| Component | Responsibility |
|---|---|
| `main.py` | Creates FastAPI app, mounts static files and initializes database |
| `routes.py` | HTML routes, shared logic and JSON API |
| `schemas.py` | Input/output validation contracts |
| `database.py` | SQLAlchemy models and persistence helpers |
| `gemini_client.py` | Shared AI client, retries, fallbacks and errors |
| Generator modules | Workout, nutrition and revised-plan generation |
| Templates/CSS | Current presentation layer |
