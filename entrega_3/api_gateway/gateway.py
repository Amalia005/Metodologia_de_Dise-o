from flask import Flask, request, jsonify
import requests as http_client

# ==========================================
# API GATEWAY — Proxy por path
# Puerto 8000
# Responsabilidad única: redirigir peticiones
# a los servicios correspondientes por prefijo de ruta.
# NO implementa autenticación, rate limiting,
# ni ninguna otra responsabilidad.
# ==========================================

app = Flask(__name__)

# Mapeo de prefijos de ruta a URLs de servicios
SERVICIOS = {
    "pedidos": "http://127.0.0.1:5000",
    "incidencias": "http://127.0.0.1:5001",
}


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "servicio": "API Gateway",
        "puerto": 8000,
        "estado": "en línea",
        "rutas": {
            "/pedidos/*": "Servicio Pedidos (puerto 5000)",
            "/incidencias/*": "Servicio Incidencias (puerto 5001)",
        }
    }), 200


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    """Redirige la petición al servicio correspondiente según el prefijo de ruta.
    Pasa método HTTP, headers, body y query params tal cual."""

    # Determinar el servicio destino por prefijo
    prefijo = path.split('/')[0]

    if prefijo not in SERVICIOS:
        return jsonify({
            "error": f"Ruta '/{path}' no reconocida. Rutas válidas: /pedidos/*, /incidencias/*"
        }), 404

    url_destino = f"{SERVICIOS[prefijo]}/{path}"

    try:
        # Reenviar la petición al servicio destino
        headers_filtrados = {
            key: value for key, value in request.headers
            if key.lower() not in ('host', 'content-length')
        }

        respuesta = http_client.request(
            method=request.method,
            url=url_destino,
            headers=headers_filtrados,
            json=request.get_json(silent=True),
            params=request.args,
            timeout=30
        )

        # Filtrar headers de respuesta problemáticos
        headers_respuesta = {
            key: value for key, value in respuesta.headers.items()
            if key.lower() not in ('transfer-encoding', 'content-encoding', 'content-length')
        }

        return (respuesta.content, respuesta.status_code, headers_respuesta)

    except http_client.exceptions.ConnectionError:
        return jsonify({
            "error": f"No se pudo conectar al servicio en {SERVICIOS[prefijo]}. "
                     f"Verifique que el servicio esté corriendo."
        }), 502
    except http_client.exceptions.Timeout:
        return jsonify({
            "error": f"Timeout al conectar con el servicio en {SERVICIOS[prefijo]}."
        }), 504
    except Exception as e:
        return jsonify({"error": f"Error en el gateway: {str(e)}"}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("API GATEWAY iniciado en puerto 8000")
    print("Rutas configuradas:")
    for prefijo, url in SERVICIOS.items():
        print(f"  /{prefijo}/* → {url}")
    print("=" * 50)
    app.run(debug=True, port=8000)
