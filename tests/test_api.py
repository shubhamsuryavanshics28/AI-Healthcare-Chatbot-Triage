import os
import tempfile

# Keep tests isolated from the developer's local database.
_test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_test_db.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_test_db.name}"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_contains_disclaimer():
    response = client.get("/")
    assert response.status_code == 200
    assert "disclaimer" in response.json()


def test_triage_returns_safe_message_and_followups():
    response = client.post(
        "/api/triage",
        json={"symptoms": "mild headache"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] is not None
    assert data["urgency"] == "needs_review"
    assert data["follow_up_questions"]
    assert "cannot diagnose" in data["disclaimer"].lower()


def test_possible_emergency_phrase_gets_urgent_message():
    response = client.post(
        "/api/triage",
        json={"symptoms": "I have severe chest pain"},
    )
    assert response.status_code == 200
    assert response.json()["urgency"] == "urgent"
    assert "emergency" in response.json()["message"].lower()


def test_invalid_severity_rejected():
    response = client.post(
        "/api/triage",
        json={"symptoms": "headache", "severity": 11},
    )
    assert response.status_code == 422


def test_missing_session_is_404():
    response = client.get("/api/sessions/999999")
    assert response.status_code == 404
