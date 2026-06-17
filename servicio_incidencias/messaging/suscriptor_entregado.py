# ==========================================
# SUSCRIPTOR — Tópico "pedido-entregado"
# Registra qué pedidos están habilitados para
# recibir incidencias (solo los entregados).
# Incluye idempotencia por event_id.
# ==========================================

# Set de pedidos que ya fueron marcados como entregados
pedidos_entregados = set()

# Set de event_ids ya procesados (idempotencia)
eventos_procesados = set()


def procesar_evento(event_id, pedido_id):
    """Procesa un evento de pedido entregado.

    Verifica idempotencia: si el event_id ya fue procesado, ignora.
    Si es nuevo, agrega el pedido_id al set de pedidos habilitados.

    Returns:
        True si el evento fue procesado, False si era duplicado.
    """
    if event_id in eventos_procesados:
        print(f"  [IDEMPOTENCIA] Evento {event_id} ya fue procesado, ignorando duplicado")
        return False

    pedidos_entregados.add(pedido_id)
    eventos_procesados.add(event_id)
    print(f"  [SUSCRIPTOR] Pedido {pedido_id} marcado como entregado y habilitado para incidencias")
    return True


def esta_habilitado(pedido_id):
    """Verifica si un pedido está habilitado para recibir incidencias
    (es decir, si ya recibió el evento 'pedido-entregado')."""
    return pedido_id in pedidos_entregados
