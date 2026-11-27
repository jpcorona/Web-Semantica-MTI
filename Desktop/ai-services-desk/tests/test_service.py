import pytest
from app.schemas import solicitudIn
from app.service import Clasificadorreglas, normalizar

@pytest.mark.parametrize("mensaje", [
    "Mi sistema está CAÍDO",
    "El servicio está caido",
    "No puedo facturar",
    "Estamos SIN SERVICIO",
    "Es urgente resolverlo",
])

def test_mensaje_urgentes(mensaje: str) -> None:
    solicitud = solicitudIn(cliente="Empresa ABC", mensaje=mensaje, canal="web")
    resultado = Clasificadorreglas().clasificar(solicitud)
    assert resultado.prioridad == "alta"
    assert resultado.categoria == "incidente"

def test_consulta_normal() -> None:
    solicitud = solicitudIn(cliente="Empresa ABC", mensaje="Necesito consultar mi estado", canal="correo")
    resultado = Clasificadorreglas().clasificar(solicitud)
    assert resultado.prioridad == "normal"
    assert resultado.requiere_atencion is False

def test_normalizar_acentos() -> None:
    assert normalizar("CAÍDO") == "caido"