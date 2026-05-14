from flask import Blueprint, request, jsonify
from services.incidencia_service import IncidenciaService

incidencia_bp = Blueprint('incidencia_bp', __name__)
service = IncidenciaService()


@incidencia_bp.route('/incidencias', methods=['POST'])
def registrar_incidencia():
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
