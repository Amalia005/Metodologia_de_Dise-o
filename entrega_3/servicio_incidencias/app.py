from flask import Flask, jsonify
from controllers.incidencia_controller import incidencia_bp

# ==========================================
# SERVICIO INCIDENCIAS — Entrypoint
# Puerto 5001
# Caso de uso: Registrar incidencia (Soporte)
# Suscriptor del tópico "pedido-entregado"
# ==========================================

app = Flask(__name__)

# Registrar el controlador de incidencias
app.register_blueprint(incidencia_bp)


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "servicio": "Servicio de Incidencias",
        "puerto": 5001,
        "estado": "en línea"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
