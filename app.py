from flask import Flask, jsonify
from controllers.pedido_controller import pedido_bp

app = Flask(__name__)

# Registrar los controladores (Blueprints)
app.register_blueprint(pedido_bp)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"mensaje": "API de Logística en línea"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)