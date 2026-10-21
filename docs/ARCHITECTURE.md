# Architecture and methodology

## High-level flow
1. A user enters a symptom description and optional age, duration, and self-reported severity.
2. The browser sends a JSON `POST /api/triage` request to the FastAPI backend.
3. Pydantic validates field types and limits.
4. A small, explicitly non-clinical keyword rule function creates cautious guidance and follow-up prompts.
5. SQLAlchemy stores the submitted symptom text and response in SQLite.
6. The API returns a JSON response for the frontend to display.

## Component responsibilities
- `frontend/index.html`: accessible structure and form.
- `frontend/styles.css`: responsive visual design.
- `frontend/app.js`: sends HTTP requests and renders responses.
- `schemas.py`: request/response data contracts.
- `triage.py`: demo-only rules, separated so a reviewed policy can replace them.
- `models.py`: database table definition.
- `database.py`: engine, session factory, dependency.
- `main.py`: routes, dependency injection, app initialization.

## Safety and privacy boundaries
- The prototype does not diagnose, prescribe medicine, or claim to be clinically validated.
- Keyword matching is incomplete and must not be relied on to rule out emergencies.
- The starter stores symptom text in a local database. Use synthetic data only for demos.
- No authentication or user identity is included; do not expose this service publicly.
- Before any real-world use, require qualified clinical review, institutional approval, privacy assessment, threat modeling, and validation.
