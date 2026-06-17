import queue
import threading
from messaging.retry import ejecutar_con_reintentos, generar_event_id, ya_procesado, marcar_procesado

# ==========================================
# COLA "asignación-repartidor"
# Cuando un pedido pasa a Validado, se publica
# un mensaje aquí. Un consumidor único (hilo daemon)
# lo procesa e invoca AsignacionService.
# Implementada con queue.Queue (FIFO, thread-safe,
# garantiza un solo consumidor por mensaje).
# ==========================================

cola_asignacion = queue.Queue()


def publicar(pedido_id):
    """Publica un mensaje de asignación en la cola.
    Genera un event_id único para idempotencia."""
    event_id = generar_event_id()
    mensaje = {"event_id": event_id, "pedido_id": pedido_id}
    cola_asignacion.put(mensaje)
    print(f"[COLA] Mensaje publicado en cola 'asignación-repartidor': {mensaje}")


def iniciar_consumidor(asignacion_service):
    """Inicia el hilo consumidor de la cola.
    Procesa mensajes uno a uno, invocando AsignacionService
    con reintentos y verificación de idempotencia.

    Args:
        asignacion_service: instancia de AsignacionService a invocar.

    Returns:
        El hilo daemon iniciado.
    """
    def consumidor():
        print("[COLA] Consumidor de 'asignación-repartidor' iniciado (hilo daemon)")
        while True:
            mensaje = cola_asignacion.get()
            event_id = mensaje["event_id"]
            pedido_id = mensaje["pedido_id"]

            # Verificar idempotencia
            if ya_procesado(event_id):
                print(f"[COLA] Evento {event_id} ya procesado, ignorando (idempotencia)")
                cola_asignacion.task_done()
                continue

            print(f"[COLA] Procesando asignación automática para pedido {pedido_id}...")

            def procesar():
                return asignacion_service.asignar_pedido(pedido_id)

            resultado = ejecutar_con_reintentos(procesar, mensaje)
            if resultado is not None:
                marcar_procesado(event_id)
                print(f"[COLA] Pedido {pedido_id} asignado exitosamente a repartidor {resultado.repartidor_id}")
            else:
                print(f"[COLA] Fallo definitivo en asignación de pedido {pedido_id} (ver DLQ)")

            cola_asignacion.task_done()

    hilo = threading.Thread(target=consumidor, daemon=True, name="consumidor-asignacion")
    hilo.start()
    return hilo
