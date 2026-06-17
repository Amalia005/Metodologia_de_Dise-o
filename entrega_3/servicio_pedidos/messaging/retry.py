import time
import uuid
from datetime import datetime

# ==========================================
# MANEJO DE FALLOS — Reintentos + DLQ + Idempotencia
# ==========================================

# Dead Letter Queue: mensajes que agotaron reintentos
dead_letter_queue = []

# IDs de eventos ya procesados (idempotencia)
eventos_procesados = set()


def generar_event_id():
    """Genera un ID único para cada evento/mensaje."""
    return str(uuid.uuid4())


def ya_procesado(event_id):
    """Verifica si un evento ya fue procesado (idempotencia)."""
    return event_id in eventos_procesados


def marcar_procesado(event_id):
    """Marca un evento como procesado para evitar duplicados."""
    eventos_procesados.add(event_id)


def ejecutar_con_reintentos(funcion, mensaje, max_intentos=3, backoff_base=1):
    """Ejecuta una función con reintentos y backoff exponencial.

    - Reintenta hasta max_intentos veces.
    - Espera backoff_base * 2^(intento-1) segundos entre reintentos (1s, 2s, 4s).
    - Si agota reintentos, mueve el mensaje a la Dead Letter Queue.

    Args:
        funcion: función sin argumentos a ejecutar.
        mensaje: dict con los datos del mensaje (para registrar en DLQ).
        max_intentos: número máximo de intentos (default 3).
        backoff_base: segundos base para el backoff (default 1).

    Returns:
        El resultado de la función si tuvo éxito, None si falló.
    """
    ultimo_error = None
    for intento in range(1, max_intentos + 1):
        try:
            resultado = funcion()
            return resultado
        except Exception as e:
            ultimo_error = e
            print(f"  [RETRY] Intento {intento}/{max_intentos} fallido: {e}")
            if intento < max_intentos:
                espera = backoff_base * (2 ** (intento - 1))
                print(f"  [RETRY] Esperando {espera}s antes del siguiente intento...")
                time.sleep(espera)

    # Agotó reintentos → Dead Letter Queue
    entrada_dlq = {
        "mensaje": str(mensaje),
        "error": str(ultimo_error),
        "timestamp": datetime.now().isoformat(),
        "intentos_realizados": max_intentos
    }
    dead_letter_queue.append(entrada_dlq)
    print(f"  [DLQ] Mensaje movido a Dead Letter Queue: {entrada_dlq}")
    return None
