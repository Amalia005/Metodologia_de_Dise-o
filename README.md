# API de Logística de Última Milla — Entregable 3

Evolución arquitectónica del sistema de logística: de un monolito Flask a **3 procesos independientes** con persistencia real, comunicación asíncrona simulada, caché y API Gateway.

## Arquitectura

```
                    ┌─────────────────────┐
                    │    API Gateway       │
                    │    (puerto 8000)     │
                    └────┬───────────┬────┘
                         │           │
            /pedidos/*   │           │  /incidencias/*
                         │           │
                ┌────────▼──┐   ┌───▼──────────┐
                │  Servicio  │   │   Servicio    │
                │  Pedidos   │   │  Incidencias  │
                │ (pto 5000) │   │  (pto 5001)   │
                │            │──▶│               │
                │  SQLite    │ HTTP│  MongoDB     │
                │  Caché     │callback(mongomock)│
                │  Cola      │   │               │
                └────────────┘   └───────────────┘
```

## Requisitos Previos

- Python 3.8+
- pip

## Instalación

```bash
cd entrega_3
pip install -r requirements.txt
```

## Ejecución (3 terminales)

**Orden recomendado:** Incidencias → Pedidos → Gateway

### Terminal 1 — Servicio Incidencias (puerto 5001)
```bash
cd entrega_3/servicio_incidencias
python app.py
```

### Terminal 2 — Servicio Pedidos (puerto 5000)
```bash
cd entrega_3/servicio_pedidos
python app.py
```

### Terminal 3 — API Gateway (puerto 8000)
```bash
cd entrega_3/api_gateway
python gateway.py
```

> **Nota:** El Servicio Incidencias debe estar corriendo antes que el Servicio Pedidos para que las notificaciones HTTP del tópico "pedido-entregado" funcionen correctamente.

## Endpoints

### Vía API Gateway (puerto 8000)

| Método | Ruta | Descripción | Servicio |
|--------|------|-------------|----------|
| POST | `/pedidos` | Crear pedido (Builder) | Pedidos |
| GET | `/pedidos/<id>` | Consultar pedido (Caché) | Pedidos |
| PUT | `/pedidos/<id>/estado` | Cambiar estado (State) | Pedidos |
| POST | `/pedidos/<id>/asignar` | Asignar repartidor manual (Strategy) | Pedidos |
| POST | `/incidencias` | Registrar incidencia | Incidencias |
| GET | `/incidencias` | Listar incidencias | Incidencias |

### Endpoints internos (acceso directo, no vía Gateway)

| Método | Ruta | Puerto | Descripción |
|--------|------|--------|-------------|
| GET | `/internal/dlq` | 5000 | Ver Dead Letter Queue |
| POST | `/internal/evento-entregado` | 5001 | Callback HTTP del tópico |
| GET | `/internal/pedidos-entregados` | 5001 | Ver pedidos habilitados |

## Decisiones Tecnológicas — Dónde se evidencia cada una

### 1. División en microservicios
- **Servicio Pedidos:** `entrega_3/servicio_pedidos/app.py` (puerto 5000)
- **Servicio Incidencias:** `entrega_3/servicio_incidencias/app.py` (puerto 5001)
- **API Gateway:** `entrega_3/api_gateway/gateway.py` (puerto 8000)

### 2. API Gateway (routing por path)
- **Archivo:** `entrega_3/api_gateway/gateway.py`
- **Función:** `proxy()` — redirige `/pedidos/*` al puerto 5000 y `/incidencias/*` al puerto 5001

### 3. Persistencia SQLite (Servicio Pedidos)
- **Archivo:** `entrega_3/servicio_pedidos/repositories/pedido_repository.py`
- Usa `sqlite3` con archivo `pedidos.db`
- Tabla `pedidos` con `INSERT OR REPLACE` (upsert)
- Misma interfaz `guardar()` / `buscar_por_id()` que el repositorio original en memoria

### 4. Persistencia MongoDB — mongomock (Servicio Incidencias)
- **Archivo:** `entrega_3/servicio_incidencias/repositories/incidencia_repository.py`
- Usa `mongomock.MongoClient()` (simula MongoDB en memoria)
- **Esquema flexible:** `entrega_3/servicio_incidencias/models/incidencia.py` — campo `datos_extra` para campos opcionales según tipo (`foto_url`, `direccion_corregida`)

### 5. Cola "asignación-repartidor" (comunicación asíncrona)
- **Publicador:** `entrega_3/servicio_pedidos/services/pedido_service.py` → `cambiar_estado()` publica cuando el estado es "Validado"
- **Cola:** `entrega_3/servicio_pedidos/messaging/cola_asignacion.py` — `queue.Queue` de Python
- **Consumidor:** hilo daemon iniciado en `app.py`, invoca `AsignacionService`

### 6. Tópico "pedido-entregado" (comunicación asíncrona)
- **Publicador:** `entrega_3/servicio_pedidos/messaging/topico_entregado.py` — HTTP POST al Servicio Incidencias
- **Suscriptor:** `entrega_3/servicio_incidencias/messaging/suscriptor_entregado.py` — set de pedidos habilitados
- **Endpoint callback:** `POST /internal/evento-entregado` en `entrega_3/servicio_incidencias/controllers/incidencia_controller.py`

### 7. Reintentos + DLQ + Idempotencia
- **Reintentos con backoff exponencial:** `entrega_3/servicio_pedidos/messaging/retry.py` → `ejecutar_con_reintentos()` (1s, 2s, 4s)
- **Dead Letter Queue:** lista en `retry.py`, visible en `GET /internal/dlq`
- **Idempotencia (Pedidos):** set `eventos_procesados` en `retry.py`, verificado por `cola_asignacion.py`
- **Idempotencia (Incidencias):** set `eventos_procesados` en `suscriptor_entregado.py`

### 8. Caché en memoria con invalidación por estado
- **Archivo:** `entrega_3/servicio_pedidos/cache/pedido_cache.py`
- **Uso:** `entrega_3/servicio_pedidos/services/pedido_service.py` → `obtener_pedido()` consulta caché antes de SQLite
- **Invalidación:** `cambiar_estado()` llama `pedido_cache.invalidar()` en cada transición
- **Demo:** los logs muestran `[CACHE HIT]` / `[CACHE MISS]` y tiempos en ms

### 9. Comunicación síncrona REST
- Toda la comunicación usa REST con JSON (igual que el Entregable 2)
- El Gateway reenvía peticiones HTTP completas (método, headers, body)

## Flujo de Demo en Postman

```
1. POST /pedidos                         → Crear pedido (estado: Creado)
2. PUT  /pedidos/<id>/estado             → {"estado": "Validado"}
   ↳ Se dispara asignación automática vía cola (ver logs terminal 2)
3. GET  /pedidos/<id>                    → Verificar estado: Asignado + repartidor_id
4. GET  /pedidos/<id>                    → Segunda vez: log muestra CACHE HIT
5. PUT  /pedidos/<id>/estado             → {"estado": "En Camino"}
6. PUT  /pedidos/<id>/estado             → {"estado": "Entregado"}
   ↳ Se envía evento HTTP al Servicio Incidencias (ver logs terminal 1)
7. POST /incidencias                     → {"pedido_id": "<id>", "tipo": "paquete_dañado",
                                            "descripcion": "...", "foto_url": "..."}
8. POST /incidencias (pedido NO entregado) → Error: "no está en estado Entregado"
9. GET  /incidencias                     → Listar todas las incidencias
```

> **Todas las peticiones del flujo de demo van al puerto 8000** (API Gateway), excepto los endpoints `/internal/*` que se acceden directamente a los puertos 5000/5001.

## Estructura del Entregable 3

```
entrega_3/
├── servicio_pedidos/                    ← Puerto 5000
│   ├── app.py
│   ├── controllers/
│   │   └── pedido_controller.py
│   ├── services/
│   │   ├── pedido_service.py
│   │   ├── asignacion_service.py
│   │   └── estrategia_asignacion.py
│   ├── models/
│   │   ├── pedido.py                    ← State + Builder (sin cambios)
│   │   └── repartidor.py               ← Sin cambios
│   ├── repositories/
│   │   ├── pedido_repository.py         ← SQLite
│   │   └── repartidor_repository.py     ← Memoria
│   ├── messaging/
│   │   ├── cola_asignacion.py           ← queue.Queue + hilo consumidor
│   │   ├── topico_entregado.py          ← HTTP callback
│   │   └── retry.py                     ← Reintentos + DLQ + Idempotencia
│   └── cache/
│       └── pedido_cache.py              ← Caché en memoria
│
├── servicio_incidencias/                ← Puerto 5001
│   ├── app.py
│   ├── controllers/
│   │   └── incidencia_controller.py
│   ├── services/
│   │   └── incidencia_service.py
│   ├── models/
│   │   └── incidencia.py                ← Con datos_extra para MongoDB
│   ├── repositories/
│   │   └── incidencia_repository.py     ← MongoDB (mongomock)
│   └── messaging/
│       └── suscriptor_entregado.py      ← Set de pedidos entregados
│
├── api_gateway/                         ← Puerto 8000
│   └── gateway.py                       ← Proxy por path
│
└── requirements.txt
```