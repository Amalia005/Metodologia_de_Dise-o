from flask import Flask, jsonify
from controllers.pedido_controller import pedido_bp
from services.asignacion_service import AsignacionService
from messaging.cola_asignacion import iniciar_consumidor
from messaging.retry import dead_letter_queue

# ==========================================
# SERVICIO PEDIDOS — Entrypoint
# Puerto 5000
# Casos de uso: Crear pedido, Cambiar estado,
# Asignar repartidor (manual y automático)
# ==========================================

app = Flask(__name__)

# Registrar el controlador de pedidos
app.register_blueprint(pedido_bp)


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "servicio": "Servicio de Pedidos",
        "puerto": 5000,
        "estado": "en línea"
    }), 200


@app.route('/internal/dlq', methods=['GET'])
def ver_dead_letter_queue():
    """Endpoint de diagnóstico: muestra los mensajes en la Dead Letter Queue."""
    return jsonify({
        "dead_letter_queue": dead_letter_queue,
        "total": len(dead_letter_queue)
    }), 200


if __name__ == '__main__':
    # Iniciar el consumidor de la cola "asignación-repartidor" (hilo daemon)
    asignacion_service = AsignacionService()
    iniciar_consumidor(asignacion_service)

    # use_reloader=False para evitar que el hilo consumidor se duplique
    app.run(debug=True, port=5000, use_reloader=False)
