from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import StrEnum
from uuid import UUID, uuid4

class Intent(StrEnum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    ACCOUNT_ACCESS = "account_access"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    GENERAL = "general"

class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Team(StrEnum):
    BILLING = "billing_ops"
    PLATFORM = "platform_support"
    IDENTITY = "identity_access"
    PRODUCT = "product_specialists"
    GENERAL = "frontline_support"

@dataclass(slots=True)
class Ticket:
    subject: str
    body: str
    customer_email: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
