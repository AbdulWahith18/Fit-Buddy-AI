# Code-Layout, Readability and Reusability

{{HEADER:2 Marks}}

## Repository Layout

![FitBuddy Project Code Layout](assets/code_layout_diagram.png)

## Readability
- Responsibilities are separated into configuration, schemas, database, routes and AI modules.
- Shared plan-generation logic is used by both HTML and JSON API routes.
- Validation errors are converted into field-oriented messages.
- Environment configuration avoids hard-coded credentials.

## Reusability
- `gemini_client.py` centralizes model creation, retries and fallbacks.
- Generator modules can be replaced without rewriting route handling.
- JSON API endpoints allow a future independent frontend.
- Mock AI makes the application testable without external AI calls.
