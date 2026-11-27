"""Contratos nuevos: no cambiamos los modelos de la Sesión 3."""
from typing import Literal
from pydantic import BaseModel, Field

Estado = Literal["nueva", "en_revision", "resuelta"]

class CambioEstadoIn(BaseModel):
    estado: Estado

class SolicitudRegistrada(BaseModel):
    id: str
    cliente: str
    mensaje: str
    canal: str
    categoria: str
    prioridad: str
    requiere_atencion: bool
    estado: Estado = "nueva"
