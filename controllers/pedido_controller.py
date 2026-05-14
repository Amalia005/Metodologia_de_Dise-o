from flask import Blueprint, request, jsonify
from services.pedido_service import PedidoService
from services.asignacion_service import AsignacionService

# Usamos Blueprint para organizar las rutas en Flask
pedido_bp = Blueprint('pedido_bp', __name__)
service = PedidoService()
asignacion_service = AsignacionService()

@pedido_bp.route('/pedidos', methods=['POST'])
def crear_pedido():
    try:
        datos = request.json
        nuevo_pedido = service.crear_pedido(datos)
        # Devuelve código 201 (Created)
        return jsonify(nuevo_pedido), 201
    except ValueError as e:
        # Si falta un dato, devuelve código 400 (Bad Request) con el error
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@pedido_bp.route('/pedidos/<id>/asignar', methods=['POST'])
def asignar_pedido(id):
    try:
        datos = request.json or {}
        tipo_estrategia = datos.get('estrategia')
        pedido_asignado = asignacion_service.asignar_pedido(id, tipo_estrategia)
        return jsonify(pedido_asignado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500