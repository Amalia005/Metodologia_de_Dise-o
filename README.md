# Sistema Logístico — Metodología de Diseño

Proyecto académico que implementa un sistema de gestión de pedidos y repartidores aplicando **patrones de diseño GOF** y **principios SOLID** en Python.

---

## Estructura del proyecto

```
├── main.py                  # Punto de entrada — simulación de 4 casos de uso
├── ventas/
│   ├── pedido.py            # Entidad Pedido + Patrón State
│   └── builder.py           # Patrón Builder para construcción de pedidos
├── operaciones/
│   ├── repartidor.py        # Entidad Repartidor
│   └── asignador.py         # Patrón Strategy para asignación de repartidores
└── soporte/
    ├── incidencia.py         # Entidad Incidencia con ciclo de vida propio
    └── facade.py             # Patrón Facade — punto de acceso unificado
```

---

## Patrones de diseño implementados

| Categoría | Patrón | Clase principal | Descripción |
|---|---|---|---|
| Creacional | **Builder** | `PedidoBuilder` | Construye pedidos complejos paso a paso con método chaining |
| Comportamiento | **State** | `EstadoPedido` | Gestiona el ciclo de vida del pedido (Creado → Validado → Asignado) |
| Comportamiento | **Strategy** | `EstrategiaAsignacion` | Permite intercambiar algoritmos de asignación de repartidores |
| Estructural | **Facade** | `LogisticaFacade` | Unifica el acceso a todos los subsistemas en un solo punto |

---

## Principios SOLID aplicados

- **SRP** — Cada clase tiene una única responsabilidad
- **OCP** — Se pueden agregar nuevas estrategias de asignación sin modificar `AsignadorService`
- **LSP** — Todos los estados de `EstadoPedido` son completamente intercambiables
- **DIP** — `AsignadorService` depende de la abstracción `EstrategiaAsignacion`, no de implementaciones concretas

---

## Casos de uso simulados

1. **Crear Pedidos** — Construcción de pedidos desde distintos canales (ecommerce, tienda física)
2. **Validar Pedidos** — Transición de estado de `Creado` a `Validado`
3. **Asignar Repartidores** — Asignación automática por menor carga de trabajo
4. **Gestionar Incidencias** — Registro y resolución de incidencias por pedido

---

## Cómo ejecutar

```bash
python main.py
```

> Requiere Python 3.8 o superior. No depende de librerías externas.