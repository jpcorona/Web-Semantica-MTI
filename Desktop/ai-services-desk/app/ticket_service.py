"""Reglas del proceso de solicitudes, independientes de HTTP."""
from app.schemas import solicitudIn
from app.service import Clasificador
from app.repository import RepositorioEnMemoria
from app.ticket_schemas import Estado, SolicitudRegistrada

TRANSICIONES: dict[str, set[str]] = {
    "nueva": {"en_revision"},
    "en_revision": {"resuelta"},
    "resuelta": set(),
}

class TransicionInvalida(Exception):
    pass

class GestorSolicitudes:
    def __init__(self, repositorio: RepositorioEnMemoria, clasificador: Clasificador):
        self.repositorio = repositorio
        self.clasificador = clasificador

    def registrar(self, entrada: solicitudIn) -> SolicitudRegistrada:
        clasificacion = self.clasificador.clasificar(entrada)
        registro = SolicitudRegistrada(
            id="pendiente", cliente=entrada.cliente, mensaje=entrada.mensaje,
            canal=entrada.canal, categoria=clasificacion.categoria,
            prioridad=clasificacion.prioridad,
            requiere_atencion=clasificacion.requiere_atencion,
            estado="nueva",
        )
        return self.repositorio.guardar(registro)

    def consultar(self, identificador: str) -> SolicitudRegistrada | None:
        return self.repositorio.buscar(identificador)

    def cambiar_estado(self, identificador: str, nuevo: Estado) -> SolicitudRegistrada | None:
        actual = self.repositorio.buscar(identificador)
        if actual is None:
            return None
        if nuevo not in TRANSICIONES[actual.estado]:
            raise TransicionInvalida(f"No se permite pasar de {actual.estado} a {nuevo}")
        return self.repositorio.actualizar_estado(identificador, nuevo)
