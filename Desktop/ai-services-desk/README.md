# AI Service Desk — continuación de Sesión 5

Proyecto original suministrado por el docente, extendido sin renombrar sus clases y rutas previas.

## Ejecutar en macOS / terminal integrada de VS Code
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Abrir http://127.0.0.1:8000/docs

## Verificar
```bash
python -m pytest -v
```

## Nuevas rutas
- `POST /solicitudes` (201): registrar solicitud usando el clasificador existente
- `GET /solicitudes/{identificador}` (200/404): consultar por ID
- `PATCH /solicitudes/{identificador}/estado` (200/404/409/422): actualizar estado

### Recorrido en Swagger
1. POST /solicitudes: cliente `Restaurante Sol`, mensaje `No puedo ingresar pedidos`, canal `web`.
2. Copiar el `id` retornado (ej. SD-0001).
3. GET /solicitudes/{id}: estado `nueva`.
4. PATCH estado `resuelta`: 409 (no puede saltarse un paso).
5. PATCH estado `en_revision`: 200.
6. PATCH estado `resuelta`: 200.
7. GET: estado `resuelta`.

### Límites declarados
- Repository **en memoria**: al reiniciar se pierden los datos; distintas réplicas no comparten registros.
- IDs secuenciales solamente didácticos: **no usar en producción**.
- Sin autenticación ni auditoría: ejercicio local, no sistema productivo.
- La transición del estado requiere control de concurrencia transaccional para escalar a producción.
- No hay LLM: se reutilizan las reglas de la Sesión 3. Próximo paso: reemplazar la implementación del clasificador a través de su interfaz.
