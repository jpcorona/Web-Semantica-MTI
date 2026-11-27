import logging
from time import perf_counter
from fastapi import FastAPI, Depends, HTTPException
from app.config import modo_mantenimiento
from app.schemas import solicitudIn, ClasificacionOut
from app.service import Clasificador, clasificar_solicitud, obtener_clasificador



logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


app=FastAPI(title="AI Service Desk", description="este es un ejemplo.", version="1.0.0")

@app.get("/health")
def health()-> dict[str, str]:
    return {"status": "ok"}

@app.post("/clasificar", response_model=ClasificacionOut)
def clasificar(solicitud: solicitudIn, clasificador: Clasificador = Depends(obtener_clasificador)) -> ClasificacionOut:
    if modo_mantenimiento():
        raise HTTPException(status_code=503, detail="El servicio está en mantenimiento")
    inicio = perf_counter()
    resultado = clasificador.clasificar(solicitud)
    duracion_ms = (perf_counter() - inicio) * 1000
    logger.info("canal=%s prioridad=%s duracion_ms=%.2f", solicitud.canal, resultado.prioridad, duracion_ms)
    return resultado

# SESIÓN 5: ampliación sin modificar /health ni /clasificar.
from app.repository import repositorio
from app.ticket_schemas import CambioEstadoIn, SolicitudRegistrada
from app.ticket_service import GestorSolicitudes, TransicionInvalida

@app.post("/solicitudes", response_model=SolicitudRegistrada, status_code=201)
def registrar_solicitud(
    entrada: solicitudIn,
    clasificador: Clasificador = Depends(obtener_clasificador),
) -> SolicitudRegistrada:
    if modo_mantenimiento():
        raise HTTPException(status_code=503, detail="El servicio está en mantenimiento")
    gestor = GestorSolicitudes(repositorio, clasificador)
    registrada = gestor.registrar(entrada)
    logger.info("solicitud_id=%s prioridad=%s", registrada.id, registrada.prioridad)
    return registrada

@app.get("/solicitudes/{identificador}", response_model=SolicitudRegistrada)
def consultar_solicitud(identificador: str) -> SolicitudRegistrada:
    gestor = GestorSolicitudes(repositorio, obtener_clasificador())
    resultado = gestor.consultar(identificador)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return resultado

@app.patch("/solicitudes/{identificador}/estado", response_model=SolicitudRegistrada)
def actualizar_estado(identificador: str, cambio: CambioEstadoIn) -> SolicitudRegistrada:
    gestor = GestorSolicitudes(repositorio, obtener_clasificador())
    try:
        resultado = gestor.cambiar_estado(identificador, cambio.estado)
    except TransicionInvalida as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    if resultado is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return resultado
