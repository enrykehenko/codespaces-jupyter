# escriba.py
# Agente Escriba de la Fortaleza Cósmica (Prototipo Antihorario)
# Misión: Registrar las interacciones y el contexto estructural de la web.

import sqlite3
import datetime
import json
import os

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Asegura que la ruta a la DB sea relativa al script, no al directorio de trabajo.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "interacciones.db")

def inicializar_db():
    """
    Crea la base de datos 'interacciones.db' y su tabla si no existen.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # La tabla almacenará la memoria episódica de los agentes.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    url TEXT NOT NULL,
                    transcripcion TEXT NOT NULL,
                    mapa_estructural TEXT, -- Almacenará un JSON con selectores CSS/XPath
                    agente_horario TEXT,   -- El agente que realiza la acción/conversación
                    agente_antihorario TEXT -- El agente que registra (este)
                )
            """)
            conn.commit()
            print(f"Base de datos de interacciones '{DB_PATH}' inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos de interacciones: {e}")

def registrar_interaccion(url, transcripcion, mapa_estructural, agente_horario, agente_antihorario="Escriba"):
    """
    Guarda un registro completo de una interacción en la base de datos.
    """
    ahora = datetime.datetime.now().isoformat()
    mapa_json = json.dumps(mapa_estructural) if mapa_estructural else None

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO interacciones (timestamp, url, transcripcion, mapa_estructural, agente_horario, agente_antihorario)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ahora, url, transcripcion, mapa_json, agente_horario, agente_antihorario))
            conn.commit()
            print(f"Interacción en {url} registrada por {agente_antihorario}.")
    except sqlite3.Error as e:
        print(f"Error al registrar la interacción: {e}")

if __name__ == "__main__":
    # Si se ejecuta directamente, inicializa la base de datos
    # y registra una interacción de ejemplo para verificación.
    inicializar_db()

    ejemplo_mapa = {
        "zona_pregunta": "#prompt-textarea",
        "boton_enviar": "button[data-testid='send-button']",
        "zona_respuesta": ".markdown.prose"
    }

    registrar_interaccion(
        url="https://chat.openai.com/chat",
        transcripcion="Pregunta: ¿Cuál es la misión? Respuesta: Construir la Fortaleza.",
        mapa_estructural=ejemplo_mapa,
        agente_horario="Comandante_CX"
    )
