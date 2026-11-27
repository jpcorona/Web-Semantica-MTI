"""Almacén temporal para aprender el patrón Repository.
ADVERTENCIA: se pierde al reiniciar y no sirve para varias réplicas.
"""
from threading import Lock
from app.ticket_schemas import SolicitudRegistrada, Estado

class RepositorioEnMemoria:
    def __init__(self) -> None:
        self._datos: dict[str, SolicitudRegistrada] = {}
        self._contador = 0
        self._lock = Lock()

    def guardar(self, solicitud: SolicitudRegistrada) -> SolicitudRegistrada:
        with self._lock:
            self._contador += 1
            identificador = f"SD-{self._contador:04d}"
            guardada = solicitud.model_copy(update={"id": identificador})
            self._datos[identificador] = guardada
            return guardada.model_copy()

    def buscar(self, identificador: str) -> SolicitudRegistrada | None:
        with self._lock:
            item = self._datos.get(identificador)
            return item.model_copy() if item else None

    def actualizar_estado(self, identificador: str, estado: Estado) -> SolicitudRegistrada | None:
        with self._lock:
            actual = self._datos.get(identificador)
            if actual is None:
                return None
            actualizado = actual.model_copy(update={"estado": estado})
            self._datos[identificador] = actualizado
            return actualizado.model_copy()

repositorio = RepositorioEnMemoria()
