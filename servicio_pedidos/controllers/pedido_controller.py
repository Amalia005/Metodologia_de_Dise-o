from flask import Blueprint, request, jsonify
from services.pedido_service import PedidoService
from services.asignacion_service import AsignacionService

pedido_bp = Blueprint('pedido_bp', __name__)
service = PedidoService()
asignacion_service = AsignacionService()


@pedido_bp.route('/pedidos', methods=['POST'])
def crear_pedido():
    """Crea un pedido nuevo (patrón Builder)."""
    try:
        datos = request.json
        pedido = service.crear_pedido(datos)
        return jsonify(pedido.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500


@pedido_bp.route('/pedidos/<pedido_id>', methods=['GET'])
def obtener_pedido(pedido_id):
    """Consulta el estado de un pedido (usa caché en memoria).
    La primera consulta viene de SQLite, las siguientes del caché.
    Se loguean tiempos de respuesta para demostrar la diferencia."""
    try:
        pedido_dict = service.obtener_pedido(pedido_id)
        return jsonify(pedido_dict), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500


@pedido_bp.route('/pedidos/<pedido_id>/estado', methods=['PUT'])
def actualizar_estado(pedido_id):
    """Cambia el estado del pedido (patrón State).
    - Si pasa a Validado: publica en cola 'asignación-repartidor'
    - Si pasa a Entregado: publica en tópico 'pedido-entregado'
    - Si pasa a Cancelado: no publica nada"""
    try:
        datos = request.json
        nuevo_estado = datos.get('estado')

        if not nuevo_estado:
            return jsonify({"error": "El campo 'estado' es obligatorio."}), 400

        pedido = service.cambiar_estado(pedido_id, nuevo_estado)
        return jsonify(pedido.to_dict()), 200

    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500


@pedido_bp.route('/pedidos/<pedido_id>/asignar', methods=['POST'])
def asignar_pedido(pedido_id):
    """Asignación MANUAL de repartidor (patrón Strategy).
    Vía alternativa al flujo automático por cola.
    Ambos caminos invocan el mismo AsignacionService."""
    try:
        datos = request.json or {}
        tipo_estrategia = datos.get('estrategia')
        pedido = asignacion_service.asignar_pedido(pedido_id, tipo_estrategia)
        return jsonify(pedido.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
