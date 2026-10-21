from .schemas import TriageRequest

DISCLAIMER = (
    "This educational tool cannot diagnose conditions or replace professional medical care. "
    "Its keyword rules are incomplete and may be wrong."
)

# A deliberately conservative demo list, not a validated clinical decision rule.
# This list must not be represented as comprehensive.
EMERGENCY_PHRASES = [
    "can't breathe", "cannot breathe", "difficulty breathing",
    "severe chest pain", "chest pain", "unconscious",
    "not waking up", "face drooping", "sudden weakness",
    "heavy bleeding", "severe allergic reaction", "suicidal"
]


def assess(request: TriageRequest) -> dict:
    text = request.symptoms.lower()
    follow_up = []

    # Do not assume absence of these keywords means the person is safe.
    if any(phrase in text for phrase in EMERGENCY_PHRASES):
        urgency = "urgent"
        message = (
            "Your description includes a phrase that may indicate an emergency. "
            "Seek emergency medical help now or contact your local emergency number. "
            "Do not rely on this chatbot to assess an emergency."
        )
    else:
        urgency = "needs_review"
        message = (
            "This prototype cannot determine the cause or reliably judge how serious symptoms are. "
            "Consider contacting a qualified healthcare professional, especially if symptoms are "
            "new, worsening, persistent, or worrying."
        )

    if request.age is None:
        follow_up.append("What is the patient's age?")
    if not request.duration:
        follow_up.append("How long have the symptoms been present?")
    if request.severity is None:
        follow_up.append("On a scale of 1 to 10, how severe do the symptoms feel?")

    if not follow_up:
        follow_up.append("Have the symptoms changed or worsened, or are there other symptoms?")

    return {
        "urgency": urgency,
        "message": message,
        "follow_up_questions": follow_up,
        "disclaimer": DISCLAIMER,
    }
