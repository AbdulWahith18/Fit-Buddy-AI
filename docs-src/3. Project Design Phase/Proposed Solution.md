# Proposed Solution

{{HEADER:3 Marks}}

## Solution Overview

FitBuddy is a web application that combines structured user validation, Google Gemini generation, persistence and feedback-based revision.

### Core flow
1. User enters profile and fitness preferences.
2. Pydantic validates and normalizes the input.
3. Gemini generates a seven-day workout plan.
4. A separate Gemini Flash pathway generates a nutrition/recovery tip.
5. User and plan data are persisted in SQLite.
6. User can submit feedback.
7. The latest plan becomes the context for a revised plan.
8. The original plan remains stored.

### Reliability behavior
- Configurable model names and fallback lists.
- Retry handling for transient AI errors.
- Static nutrition-tip fallback.
- Mock-AI mode for automated testing and demonstrations.

### Future UI independence
The current Jinja2 presentation is not tightly coupled to the core business logic. A future React or other frontend can consume the JSON API while retaining the same generation and persistence behavior.
