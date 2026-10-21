const API_BASE = "https://ai-healthcare-chatbot-triage.onrender.com";
const form = document.getElementById("triage-form");
const messages = document.getElementById("messages");
const statusEl = document.getElementById("form-status");
const submitBtn = document.getElementById("submit-btn");

function addMessage(text, role = "bot", extraClass = "") {
  const el = document.createElement("div");
  el.className = `message ${role} ${extraClass}`.trim();
  el.textContent = text;
  messages.appendChild(el);
  messages.scrollTop = messages.scrollHeight;
  return el;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.textContent = "";
  const symptoms = document.getElementById("symptoms").value.trim();
  const ageRaw = document.getElementById("age").value;
  const duration = document.getElementById("duration").value.trim();
  const severityRaw = document.getElementById("severity").value;

  if (symptoms.length < 3) {
    statusEl.textContent = "Please describe the symptoms in a little more detail.";
    return;
  }

  const payload = { symptoms };
  if (ageRaw !== "") payload.age = Number(ageRaw);
  if (duration !== "") payload.duration = duration;
  if (severityRaw !== "") payload.severity = Number(severityRaw);

  addMessage(symptoms, "user");
  submitBtn.disabled = true;
  submitBtn.textContent = "Preparing response…";

  try {
    const response = await fetch(`${API_BASE}/api/triage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail ? JSON.stringify(data.detail) : "The request could not be processed.");
    }

    addMessage(`${data.message}\n\nPrototype urgency label: ${data.urgency}`, "bot", "result");
    if (data.follow_up_questions?.length) {
      addMessage("Follow-up questions:\n• " + data.follow_up_questions.join("\n• "), "bot");
    }
    addMessage(data.disclaimer, "bot");
    form.reset();
  } catch (error) {
    statusEl.textContent = `Could not reach the API. Make sure FastAPI is running at ${API_BASE}. Details: ${error.message}`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Get general guidance <span aria-hidden="true">→</span>';
  }
});
