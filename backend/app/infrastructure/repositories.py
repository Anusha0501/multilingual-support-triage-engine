from app.domain.models import Ticket

class InMemoryTicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}

    def create(self, ticket: Ticket) -> Ticket:
        self._tickets[str(ticket.id)] = ticket
        return ticket

    def list(self) -> list[Ticket]:
        return list(self._tickets.values())

    def get(self, ticket_id: str) -> Ticket | None:
        return self._tickets.get(ticket_id)
