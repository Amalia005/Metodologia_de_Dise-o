import threading
import requests
from messaging.retry import ejecutar_con_reintentos, generar_event_id

# ==========================================
# TÓPICO "pedido-entregado"
# Cuando un pedido pasa a Entregado, se publica
# un evento a este tópico. El Servicio Incidencias
# está suscrito vía HTTP callback.
# La publicación se hace en un hilo separado para
# no bloquear la respuesta al cliente.
# ==========================================

# URLs de los suscriptores del tópico
SUSCRIPTORES = [
    "http://127.0.0.1:5001/internal/evento-entregado"
]


def publicar(pedido_id):
    """Publica un evento 'pedido-entregado' a todos los suscriptores.
    La notificación se envía en un hilo separado (fire-and-forget)
    para no bloquear la respuesta HTTP al cliente."""
    event_id = generar_event_id()
    evento = {"event_id": event_id, "pedido_id": pedido_id}

    def _notificar():
        for url in SUSCRIPTORES:
            def enviar(url_destino=url):
                print(f"  [TOPICO] Enviando evento a {url_destino}: {evento}")
                response = requests.post(url_destino, json=evento, timeout=5)
                response.raise_for_status()
                print(f"  [TOPICO] Suscriptor {url_destino} respondió: {response.status_code}")
                return response

            ejecutar_con_reintentos(enviar, evento)

    hilo = threading.Thread(target=_notificar, daemon=True, name="topico-entregado")
    hilo.start()
    print(f"[TOPICO] Evento 'pedido-entregado' publicado (async): {evento}")
