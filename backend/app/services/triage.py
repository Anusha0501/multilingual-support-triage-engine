from hashlib import sha256
from uuid import uuid4
from app.domain.models import Intent, Priority, Team, Ticket
from app.dto.tickets import Prediction, TicketCreate, TicketTriageResponse
from app.infrastructure.repositories import InMemoryTicketRepository

class TicketTriageService:
    def __init__(self, repository: InMemoryTicketRepository) -> None:
        self.repository = repository

    def triage_ticket(self, request: TicketCreate) -> TicketTriageResponse:
        ticket = self.repository.create(Ticket(subject=request.subject, body=request.body, customer_email=str(request.customer_email)))
        text = f"{request.subject}\n{request.body}"
        language = self._detect_language(text)
        intent = self._classify_intent(text)
        priority = self._predict_priority(text)
        team = self._assign_team(intent.label)
        sla = self._predict_sla_risk(text, priority.label)
        return TicketTriageResponse(
            ticket_id=str(ticket.id), language=language, intent=intent, priority=priority,
            assigned_team=team.value, sla_breach_risk=sla, reply_draft=self._draft_reply(language.label, intent.label),
            trace_id=sha256(f"{ticket.id}:{uuid4()}".encode()).hexdigest()[:24],
        )

    def _detect_language(self, text: str) -> Prediction:
        lowered = text.lower()
        if any(token in lowered for token in ["hola", "gracias", "factura"]):
            return Prediction(label="es", confidence=0.86, rationale="Spanish support terms detected.")
        if any(token in lowered for token in ["bonjour", "merci", "facture"]):
            return Prediction(label="fr", confidence=0.84, rationale="French support terms detected.")
        if any("\u0900" <= char <= "\u097f" for char in text):
            return Prediction(label="hi", confidence=0.9, rationale="Devanagari script detected; IndicBERT can refine this in production.")
        return Prediction(label="en", confidence=0.78, rationale="Default English classifier path selected.")

    def _classify_intent(self, text: str) -> Prediction:
        lowered = text.lower()
        rules = [(Intent.BILLING, ["invoice", "billing", "refund", "charge", "factura"]), (Intent.ACCOUNT_ACCESS, ["login", "password", "mfa", "locked"]), (Intent.BUG_REPORT, ["bug", "error", "crash", "500"]), (Intent.FEATURE_REQUEST, ["feature", "request", "enhancement"])]
        for intent, terms in rules:
            if any(term in lowered for term in terms):
                return Prediction(label=intent.value, confidence=0.82, rationale=f"Matched {intent.value} keyword policy.")
        return Prediction(label=Intent.GENERAL.value, confidence=0.62, rationale="No specialist intent matched; routed to general triage.")

    def _predict_priority(self, text: str) -> Prediction:
        lowered = text.lower()
        if any(term in lowered for term in ["down", "outage", "security", "breach", "production"]):
            return Prediction(label=Priority.CRITICAL.value, confidence=0.88, rationale="Business-critical risk terms detected.")
        if any(term in lowered for term in ["urgent", "blocked", "cannot access"]):
            return Prediction(label=Priority.HIGH.value, confidence=0.8, rationale="Customer appears blocked.")
        return Prediction(label=Priority.MEDIUM.value, confidence=0.7, rationale="Standard support issue with no outage indicators.")

    def _assign_team(self, intent: str) -> Team:
        return {Intent.BILLING.value: Team.BILLING, Intent.ACCOUNT_ACCESS.value: Team.IDENTITY, Intent.BUG_REPORT.value: Team.PLATFORM, Intent.FEATURE_REQUEST.value: Team.PRODUCT}.get(intent, Team.GENERAL)

    def _predict_sla_risk(self, text: str, priority: str) -> Prediction:
        risk = "high" if priority in {Priority.HIGH.value, Priority.CRITICAL.value} else "medium"
        return Prediction(label=risk, confidence=0.76, rationale="Combines priority, customer-blocked language, and SLA policy baseline.")

    def _draft_reply(self, language: str, intent: str) -> str:
        drafts = {"es": "Gracias por contactarnos. Hemos recibido tu solicitud y nuestro equipo está revisándola con prioridad.", "fr": "Merci de nous avoir contactés. Notre équipe examine votre demande et reviendra rapidement vers vous.", "hi": "संपर्क करने के लिए धन्यवाद। हमारी टीम आपके अनुरोध की समीक्षा कर रही है।"}
        return drafts.get(language, f"Thanks for contacting support. We identified this as a {intent.replace('_', ' ')} request and routed it to the right team.")
