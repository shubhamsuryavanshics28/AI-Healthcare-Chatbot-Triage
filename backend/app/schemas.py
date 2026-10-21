from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TriageRequest(BaseModel):
    symptoms: str = Field(min_length=3, max_length=2000)
    age: int | None = Field(default=None, ge=0, le=120)
    duration: str | None = Field(default=None, max_length=120)
    severity: int | None = Field(default=None, ge=1, le=10)


class TriageResponse(BaseModel):
    session_id: int | None
    urgency: str
    message: str
    follow_up_questions: list[str]
    disclaimer: str


class SessionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    symptoms: str
    age: int | None
    duration: str | None
    severity: int | None
    urgency: str
    response: str
    created_at: datetime
