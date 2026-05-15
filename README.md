# API de Logística - Entregable 2

Servicio web en Flask para logística de última milla. Arquitectura en capas con patrones GoF.

## Estructura

```
controllers/   → Capa de Presentación (HTTP + JSON)
services/      → Capa de Aplicación (lógica de casos de uso)
models/        → Capa de Dominio (entidades y reglas de negocio)
repositories/  → Capa de Infraestructura (persistencia en memoria)
```

## Endpoints

| Método | Ruta | Descripción | Patrón |
|--------|------|-------------|--------|
| POST | `/pedidos` | Crear pedido | Builder |
| PUT | `/pedidos/<id>/estado` | Cambiar estado | State |
| POST | `/pedidos/<id>/asignar` | Asignar repartidor | Strategy |
| POST | `/incidencias` | Registrar incidencia | Facade |

## Ejecución

```bash
pip install -r requirements.txt
python app.py
```

El servidor corre en `http://127.0.0.1:5000`