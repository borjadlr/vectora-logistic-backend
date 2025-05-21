from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

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

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    contenido = respuesta.choices[0].message["content"]
    try:
        rutas = json.loads(contenido)
    except Exception:
        rutas = {"error": "La respuesta no era JSON válido", "bruto": contenido}

    return jsonify(rutas)
