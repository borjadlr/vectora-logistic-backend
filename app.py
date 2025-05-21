from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()
    tabla = data.get("tabla", "")

    prompt = f"""
Eres un asistente logístico. Te paso una tabla con columnas como ORIGEN, DESTINO, CLIENTE, COLOR y FECHA.
Devuélveme un JSON estructurado con los campos:
- origen
- destino
- chofer (deducido del color)
- color_hex
- grupo (si pertenece a trayecto concatenado)
- orden (dentro del grupo)

Tabla:
{tabla}
"""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        contenido = respuesta.choices[0].message.content
        rutas = json.loads(contenido)

    except Exception as e:
        rutas = {
            "error": "La respuesta no era JSON válido o hubo un error de conexión.",
            "detalle": str(e),
            "bruto": locals().get("contenido", "")
        }

    return jsonify(rutas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
