# Performance Testing

{{HEADER:3 Marks}}

## Test Approach

The supplied application is a synchronous local FastAPI application with AI generation as the expected latency-dominant operation. Performance testing should therefore distinguish application overhead from external Gemini latency.

| Scenario | Test Setup | Measurement |
|---|---|---|
| 1 user | Local FastAPI + mock AI | Request latency and status |
| 10 users | Concurrent requests | Error rate and response time |
| 25 users | Concurrent requests | Error rate and response time |
| Live Gemini | Real API key | End-to-end latency including model call |

## Evidence Status

The package includes the evidence-folder convention used by the reference repository. The text evidence files are retained for the team's executed load-test outputs. Any performance values should be updated from the actual run results before final external submission if a fresh load test is performed.

## Optimization opportunities
- Use an async Gemini client or background queue for long AI requests.
- Cache non-personalized nutrition requests when appropriate.
- Move SQLite to PostgreSQL for concurrent production workloads.
- Add rate limiting and observability before public deployment.

## Step 5: Screenshots / Evidence

The following screenshot is visual evidence from the implemented FitBuddy application and complements the automated/text-based test evidence in `6.Project Testing/evidence/`.

![Generated workout plan evidence](assets/05_generated_workout_plan.jpeg)

**Figure 1 — FitBuddy Generated Workout Plan Evidence.** The screenshot shows the completed seven-day plan returned by the application, including the user's goal and intensity and the day-wise workout content. It demonstrates that the end-to-end generation workflow reaches a rendered result page suitable for user review.
