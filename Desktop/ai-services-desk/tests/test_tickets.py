from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ENTRADA = {
    "cliente": "Restaurante Sol", "mensaje": "No puedo ingresar pedidos",
    "canal": "web",
}

def crear() -> dict:
    respuesta = client.post("/solicitudes", json=ENTRADA)
    assert respuesta.status_code == 201
    return respuesta.json()

def test_registrar_con_clasificador_anterior() -> None:
    ticket = crear()
    assert ticket["id"].startswith("SD-")
    assert ticket["prioridad"] == "alta"
    assert ticket["estado"] == "nueva"

def test_consultar_registro() -> None:
    ticket = crear()
    respuesta = client.get(f"/solicitudes/{ticket['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["cliente"] == "Restaurante Sol"

def test_no_existe() -> None:
    assert client.get("/solicitudes/SD-999999").status_code == 404

def test_validacion_original() -> None:
    respuesta = client.post("/solicitudes", json={**ENTRADA, "mensaje": "hola"})
    assert respuesta.status_code == 422

def test_flujo_valido() -> None:
    ticket = crear()
    ruta = f"/solicitudes/{ticket['id']}/estado"
    paso1 = client.patch(ruta, json={"estado": "en_revision"})
    assert paso1.status_code == 200
    paso2 = client.patch(ruta, json={"estado": "resuelta"})
    assert paso2.status_code == 200
    assert paso2.json()["estado"] == "resuelta"

def test_no_saltar_a_resuelta() -> None:
    ticket = crear()
    respuesta = client.patch(f"/solicitudes/{ticket['id']}/estado", json={"estado": "resuelta"})
    assert respuesta.status_code == 409

def test_estado_desconocido() -> None:
    ticket = crear()
    respuesta = client.patch(f"/solicitudes/{ticket['id']}/estado", json={"estado": "eliminada"})
    assert respuesta.status_code == 422
