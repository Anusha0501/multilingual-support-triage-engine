from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_triage_ticket_detects_spanish_billing():
    response = client.post("/api/v1/tickets/triage", json={"subject":"Factura incorrecta", "body":"Hola, necesito ayuda con una factura duplicada. Gracias.", "customer_email":"ana@example.com"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["language"]["label"] == "es"
    assert payload["intent"]["label"] == "billing"
    assert payload["assigned_team"] == "billing_ops"
