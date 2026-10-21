from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import TriageSession
from .schemas import TriageRequest, TriageResponse, SessionSummary
from .triage import DISCLAIMER, assess

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Healthcare Chatbot — Patient Assistance & Triage",
    description=(
        "Educational prototype for symptom intake and safe next-step messaging. "
        "It does not diagnose and is not clinically validated."
    ),
    version="0.1.0",
)

# For local student development only. Restrict origins before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Healthcare chatbot API is running",
        "disclaimer": DISCLAIMER,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "note": "Service health only; not a medical assessment."}


@app.post("/api/triage", response_model=TriageResponse, status_code=200)
def create_triage(payload: TriageRequest, db: Session = Depends(get_db)):
    result = assess(payload)
    record = TriageSession(
        symptoms=payload.symptoms,
        age=payload.age,
        duration=payload.duration,
        severity=payload.severity,
        urgency=result["urgency"],
        response=result["message"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return TriageResponse(
        session_id=record.id,
        urgency=result["urgency"],
        message=result["message"],
        follow_up_questions=result["follow_up_questions"],
        disclaimer=result["disclaimer"],
    )


@app.get("/api/sessions", response_model=list[SessionSummary])
def list_sessions(limit: int = 20, db: Session = Depends(get_db)):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    return db.query(TriageSession).order_by(TriageSession.id.desc()).limit(limit).all()


@app.get("/api/sessions/{session_id}", response_model=SessionSummary)
def get_session(session_id: int, db: Session = Depends(get_db)):
    record = db.get(TriageSession, session_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return record
