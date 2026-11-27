from typing import Literal
from pydantic import BaseModel, Field

class solicitudIn(BaseModel):
    cliente: str = Field(min_length=2, max_length=100)
    mensaje: str = Field(min_length=5, max_length=2000)
    canal: Literal["web", "correo", "whatsapp"]

class ClasificacionOut(BaseModel):
   cliente: str
   categoria: str
   prioridad: str
   requiere_atencion: bool
   metodo: str