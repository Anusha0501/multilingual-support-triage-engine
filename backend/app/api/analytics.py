from fastapi import APIRouter
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("/overview")
def overview() -> dict[str, int | float]:
    return {"open_tickets": 128, "sla_risk": 17, "automation_rate": 0.64, "languages": 12}
