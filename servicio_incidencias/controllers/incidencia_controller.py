from flask import Blueprint, request, jsonify
from services.incidencia_service import IncidenciaService
from messaging.suscriptor_entregado import procesar_evento, pedidos_entregados

incidencia_bp = Blueprint('incidencia_bp', __name__)
service = IncidenciaService()


@incidencia_bp.route('/incidencias', methods=['POST'])
def registrar_incidencia():
    """Registra una incidencia para un pedido entregado.
    Rechaza la operación si el pedido no ha sido marcado como entregado
    (es decir, no se recibió el evento del tópico 'pedido-entregado')."""
    try:
        datos = request.json
        incidencia = service.registrar_incidencia(datos)
        return jsonify(incidencia.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500


@incidencia_bp.route('/incidencias', methods=['GET'])
def listar_incidencias():
    """Lista todas las incidencias registradas (útil para demos)."""
    try:
        incidencias = service.listar_incidencias()
        return jsonify(incidencias), 200
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500


@incidencia_bp.route('/internal/evento-entregado', methods=['POST'])
def recibir_evento_entregado():
    """Endpoint interno: recibe notificaciones del Servicio Pedidos
    cuando un pedido pasa a estado 'Entregado'.
    Agrega el pedido_id al set de pedidos habilitados.
    Verifica idempotencia por event_id."""
    try:
        datos = request.json
        event_id = datos.get('event_id')
        pedido_id = datos.get('pedido_id')

        if not event_id or not pedido_id:
            return jsonify({"error": "Los campos 'event_id' y 'pedido_id' son obligatorios"}), 400

        fue_nuevo = procesar_evento(event_id, pedido_id)

        if fue_nuevo:
            return jsonify({
                "mensaje": f"Pedido {pedido_id} habilitado para recibir incidencias",
                "event_id": event_id
            }), 200
        else:
            return jsonify({
                "mensaje": "Evento ya procesado anteriormente (idempotencia)",
                "event_id": event_id
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@incidencia_bp.route('/internal/pedidos-entregados', methods=['GET'])
def ver_pedidos_entregados():
    """Endpoint de diagnóstico: muestra los pedidos habilitados para incidencias."""
    return jsonify({
        "pedidos_entregados": list(pedidos_entregados),
        "total": len(pedidos_entregados)
    }), 200
