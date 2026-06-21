from pydantic import BaseModel, EmailStr, Field

class TicketCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=180)
    body: str = Field(min_length=10, max_length=12000)
    customer_email: EmailStr
    product_area: str | None = None

class Prediction(BaseModel):
    label: str
    confidence: float
    rationale: str

class TicketTriageResponse(BaseModel):
    ticket_id: str
    language: Prediction
    intent: Prediction
    priority: Prediction
    assigned_team: str
    sla_breach_risk: Prediction
    reply_draft: str
    trace_id: str
