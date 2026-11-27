import unicodedata
from typing import Protocol
from app.schemas import solicitudIn, ClasificacionOut

PALABRAS_URGENTES = ["caído", "caido", "no puedo", "sin servicio", "urgente"]

def normalizar(texto: str) -> str:
    """Minúsculas y sin marcas de acentos para comparar expresiones"""
    texto= unicodedata.normalize("NFKD", texto.casefold())
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))

class Clasificador(Protocol):
    def clasificar(self, solicitud: solicitudIn) -> ClasificacionOut: ...

class Clasificadorreglas:
    def clasificar(self, solicitud: solicitudIn) -> ClasificacionOut:
        mensaje = normalizar(solicitud.mensaje)
        es_urgente = any(palabra in mensaje for palabra in PALABRAS_URGENTES)
        return ClasificacionOut(
            cliente=solicitud.cliente,
            categoria="incidente" if es_urgente else "consulta",
            prioridad="alta" if es_urgente else "normal",
            requiere_atencion=es_urgente,
            metodo="reglas_deterministas",
        )

def obtener_clasificador() -> Clasificador:
    """Punto de entensión para un clasificador LLM en próximos cursos."""
    return Clasificadorreglas()


def clasificar_solicitud(solicitud: solicitudIn) -> ClasificacionOut:
    return Clasificadorreglas().clasificar(solicitud)
