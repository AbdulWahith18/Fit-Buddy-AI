# Project Demo Planning

{{HEADER:1 Mark}}

| S.No | Demo Section | Description | Duration (mins) | Responsible Member |
|---|---|---|---:|---|
| 1 | Introduction & problem statement | Explain generic-plan problem and FitBuddy goal | 1 | Kamalesh T |
| 2 | Architecture & tech stack | FastAPI, Gemini, SQLite, validation and fallback design | 2 | Abdul Wahith M |
| 3 | Input validation & generation | Enter user data and generate the seven-day plan | 2 | Bilu Besto H |
| 4 | Feedback revision | Submit feedback and demonstrate updated plan | 2 | Abdul Wahith M |
| 5 | Database/admin view | Show saved user, plan, feedback and deletion flow | 1 | Prasannavelan K |
| 6 | Testing & API | Run tests and demonstrate `/docs` endpoints | 2 | Bharath Jeyakkumar S |
| 7 | Scalability, future plan, Q&A | Roadmap and questions | 2 | Whole team |

### Demo Flow Summary

| Step | Activity | Notes |
|---|---|---|
| 1 | Introduction | Use problem statements from Phase 1 |
| 2 | Solution overview | Show architecture and AI/persistence flow |
| 3 | Live feature demonstration | Generate plan, show tip, submit feedback, reopen result |
| 4 | API/testing | Open `/docs` and explain mock-AI test strategy |
| 5 | Q&A | Be ready to explain model fallback and database design |

### Pre-demo checklist
- `.env` contains a working `GOOGLE_API_KEY` for live mode.
- `python scripts/list_models.py` has been used to verify available models.
- Start server with `uvicorn app.main:app --reload`.
- If no key is available, set `FITBUDDY_MOCK_AI=true` and explain the demo mode.


## Demonstration Details

| Field | Details |
|---|---|
| Demo Date | {{demo_date}} |
| Demo Location | {{demo_location}} |
| Demo Platform | {{demo_platform}} |
| Demo Video URL | {{demo_video_url}} |
| Faculty Mentor / Guide | {{mentor}} |
| Team Leader | {{team_leader}} |
