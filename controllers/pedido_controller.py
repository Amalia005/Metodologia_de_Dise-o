from flask import Blueprint, request, jsonify
from services.pedido_service import PedidoService

# Usamos Blueprint para organizar las rutas en Flask
pedido_bp = Blueprint('pedido_bp', __name__)
service = PedidoService()

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