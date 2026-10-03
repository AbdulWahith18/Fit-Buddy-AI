# Scalability & Future Plan

{{HEADER:1 Mark}}

## Current System Limitations

| S.No | Limitation | Impact | Priority to Address |
|---|---|---|---|
| 1 | SQLite local database | Limited concurrent write scalability | High |
| 2 | Gemini generation is request-latency sensitive | End-to-end latency depends on external AI service | High |
| 3 | Local admin view has no authentication layer | Not suitable as a production admin console | High |
| 4 | Fitness profile is relatively small | Less personalization than a full health/fitness profile | Medium |

## Scalability Plan

| S.No | Scalability Aspect | Current State | Proposed Upgrade / Solution |
|---|---|---|---|
| 1 | User Load | Local FastAPI + SQLite | Multiple workers behind a reverse proxy |
| 2 | Data Storage | SQLite file | PostgreSQL with connection pooling |
| 3 | AI Requests | Synchronous generation | Async client/background jobs and queues |
| 4 | Security | API key in environment; local admin view | Authentication, authorization, rate limiting and secrets manager |
| 5 | Observability | Basic logging | Structured logs, metrics and tracing |

## Future Roadmap

| Phase | Planned Feature / Enhancement | Target Timeline | Expected Impact |
|---|---|---|---|
| Phase 2 | Exercise library, progress tracking and plan history versions | 1-2 months | Better continuity |
| Phase 3 | PostgreSQL, authentication and hosted deployment | 2-3 months | Multi-user production readiness |
| Phase 4 | Wearable integration, charts, reminders and nutrition tracking | 3-6 months | Broader fitness use cases |
