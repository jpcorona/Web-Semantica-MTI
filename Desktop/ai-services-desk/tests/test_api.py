from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_incidente_urgente()-> None:
        respuesta = client.post("/clasificar",
        json={"cliente": "Juan", "mensaje": "Mi sistema esta caido y no puedo facturar", "canal": "web"})
        assert respuesta.status_code == 200
        assert respuesta.json()["prioridad"] == "alta"
        assert respuesta.json()["requiere_atencion"] is True

def test_rechaza_mensaje_corto() -> None:
        respuesta = client.post("/clasificar",
        json={"cliente": "Empresa ABC", "mensaje": "Hola", "canal": "web"})
        assert respuesta.status_code == 422