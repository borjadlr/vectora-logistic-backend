from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Contexto de ubicaciones
ubicaciones_contexto = """
Estas son ubicaciones relevantes del sistema logístico:

- 2T2: Carrer Miquel Torelló i Pagès, 7, 08750 Molins de Rei, Barcelona | Horario: 08:00 - 17:00 | Tipo: Base / Campa
- CAMPA VILANOVA: Vilanova Park, Carretera de l'Arboç, Km 2.5, 08800 Vilanova i la Geltrú | Horario: 08:00 - 20:00 | Tipo: Campa
- GRIMALDI MUELLE COSTA PTO BCN: Terminal Grimaldi, Muelle de Costa, s/n, 08039 Barcelona | Horario: 24h | Tipo: Terminal Portuaria
- TRADISA: Acceso Complejo SEAT, s/n, 08760 Martorell, Barcelona | Horario: 06:00 - 22:00 | Tipo: Centro Logístico
- SETRAMPARK: Ctra. N-152z Km. 16, 08130 Santa Perpètua de Mogoda, Barcelona | Horario: 07:00 - 19:00 | Tipo: Centro logístico
- ROVIRA MOTOR: Polígono Malloles, Calle Rupit, 1, 08500 Vic, Barcelona | Horario: 08:00 - 13:00 / 15:00 - 19:00 | Tipo: Concesionario
- AUTOS NIGORRA IBIZA: Av. Sant Joan de Labritja, s/n, 07800 Ibiza | Horario: 09:00 - 13:00 / 16:00 - 20:00 | Tipo: Concesionario
- TEAMS VILADOMAT: Carrer de Viladomat, 275, L'Eixample, 08029 Barcelona | Horario: 08:00 - 18:00 | Tipo: Centro logístico
- ROMACAR FLOTAS: Calle Pere IV, 425, 08020 Barcelona | Horario: 07:30 - 20:30 | Tipo: Flota Ford
- BADAL: Rambla de Badal, 81, 08014 Barcelona | Horario: 09:00 - 13:00 / 16:00 - 20:00 | Tipo: Concesionario Stellantis
"""

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()
    tabla = data.get("tabla", "")

    prompt = f"""
Eres un asistente logístico. A continuación tienes información de ubicaciones relevantes y después una tabla con movimientos logísticos.
Tu tarea es devolver un JSON con los campos:
- origen
- destino
- chofer (deducido del color si lo hubiera)
- color_hex
- grupo (si pertenece a un trayecto concatenado)
- orden (dentro del grupo)

{ubicaciones_contexto}

Tabla:
{tabla}
"""

    try:
        respuesta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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
