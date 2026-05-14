from flask import Blueprint, request, jsonify
from services.pedido_service import PedidoService
from services.asignacion_service import AsignacionService

pedido_bp = Blueprint('pedido_bp', __name__)
service = PedidoService()
asignacion_service = AsignacionService()


@pedido_bp.route('/pedidos', methods=['POST'])
def crear_pedido():
    try:
        datos = request.json
        pedido = service.crear_pedido(datos)
        return jsonify(pedido.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500


@pedido_bp.route('/pedidos/<pedido_id>/estado', methods=['PUT'])
def actualizar_estado(pedido_id):
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


@pedido_bp.route('/pedidos/<id>/asignar', methods=['POST'])
def asignar_pedido(id):
    try:
        datos = request.json or {}
        tipo_estrategia = datos.get('estrategia')
        pedido = asignacion_service.asignar_pedido(id, tipo_estrategia)
        return jsonify(pedido.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500