import os



def modo_mantenimiento() -> bool:
    """
    Lee la configuración del entorno en cada solicitud.
    """
    valor =  os.getenv("MODO_MANTENIMIENTO", "False")
    return valor.casefold() in {"true", "1","yes"}