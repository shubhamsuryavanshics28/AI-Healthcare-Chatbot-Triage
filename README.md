# AI-Based Healthcare Chatbot for Patient Assistance and Triage

A student project starter for a web-based chatbot that collects symptom descriptions, asks basic follow-up questions, and returns a **non-diagnostic, rule-based urgency suggestion** with safe next steps.

> **Safety notice:** This educational prototype is not a medical device and does not diagnose, treat, or replace a clinician. The triage rules are deliberately simple and incomplete. Do not use this project for real clinical decisions or emergencies. In an emergency, contact local emergency services.

## Technology stack
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Backend:** Python, FastAPI, Pydantic
- **Database:** SQLite with SQLAlchemy 2.x
- **Testing:** pytest, FastAPI TestClient
- **API exploration:** automatic Swagger UI at `/docs`
- **Optional future AI integration:** can be added later behind a reviewed service; this starter does not send health information to an external AI service.

## Features
- Responsive chat-like interface
- API endpoint to assess a symptom description
- Rule-based urgent-warning phrase checks
- Follow-up prompts for missing information
- Stores conversations/triage summaries locally in SQLite (prototype only)
- View recent sessions and health disclaimer
- Input validation and basic error responses
- Unit tests for API behavior

## Project layout
```text
AI_Healthcare_Chatbot_Triage/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── triage.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   └── test_api.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── API_EXAMPLES.md
├── .gitignore
└── README.md
```

## Run locally on Fedora/Linux

### 1. Prerequisites
Install Python 3.10+ (Python 3.11+ recommended). From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 2. Start the API
Run from the project root:

```bash
uvicorn app.main:app --app-dir backend --reload
```

API: http://127.0.0.1:8000  
Interactive API docs: http://127.0.0.1:8000/docs

### 3. Open the frontend
With the API running, open `frontend/index.html` in your browser. If browser restrictions interfere, serve it locally in a second terminal:

```bash
python -m http.server 5500 --directory frontend
```

Then open http://127.0.0.1:5500.

### 4. Run tests
From the project root with the virtual environment active:

```bash
pytest
```

## API endpoints
- `GET /` — service status and safety notice
- `GET /health` — health check (not a medical assessment)
- `POST /api/triage` — assess symptom text using prototype rules
- `GET /api/sessions` — list recent saved sessions
- `GET /api/sessions/{session_id}` — fetch one saved session

## Example request
```bash
curl -X POST http://127.0.0.1:8000/api/triage \
  -H 'Content-Type: application/json' \
  -d '{"symptoms":"I have a mild headache","age":20,"duration":"since this morning","severity":3}'
```

## Important limitations and next steps
1. The symptom rules are not clinically validated, and keyword matching can miss or misread symptoms.
2. This project does not provide a diagnosis, medication recommendation, or treatment plan.
3. Before any real-world or human-subject testing, consult a qualified clinician, your supervisor, and your institution's ethics/privacy process.
4. Add authentication, authorization, retention/deletion controls, HTTPS, rate limiting, and security review before deployment.
5. Replace demo triage rules only with a clinically reviewed protocol and documented validation.
6. Keep secrets and real patient information out of source control and demo data.

## Team project work split (group of 4)
- Member 1: UI/UX and frontend integration
- Member 2: FastAPI endpoints, schemas, validation
- Member 3: database models, persistence, tests
- Member 4: literature review, safe triage requirements, evaluation and documentation

Adjust the split based on your supervisor's instructions.
