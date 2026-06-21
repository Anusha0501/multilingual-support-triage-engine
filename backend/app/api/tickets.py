from fastapi import APIRouter, Depends
from app.api.deps import get_triage_service
from app.dto.tickets import TicketCreate, TicketTriageResponse
from app.services.triage import TicketTriageService

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/triage", response_model=TicketTriageResponse)
def triage_ticket(payload: TicketCreate, service: TicketTriageService = Depends(get_triage_service)) -> TicketTriageResponse:
    return service.triage_ticket(payload)

@router.get("")
def list_tickets(service: TicketTriageService = Depends(get_triage_service)) -> list[dict[str, str]]:
    return [{"id": str(ticket.id), "subject": ticket.subject, "customer_email": ticket.customer_email} for ticket in service.repository.list()]
