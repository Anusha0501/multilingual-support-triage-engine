from functools import lru_cache
from app.infrastructure.repositories import InMemoryTicketRepository
from app.services.triage import TicketTriageService

@lru_cache
def get_repository() -> InMemoryTicketRepository:
    return InMemoryTicketRepository()

def get_triage_service() -> TicketTriageService:
    return TicketTriageService(get_repository())
