# registro_habilidades.py
# Gestor de la base de datos de habilidades de la Fortaleza Cósmica.

import sqlite3
import datetime

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_PATH = "habilidades.db"

def inicializar_db():
    """
    Crea la base de datos y la tabla 'habilidades' si no existen.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habilidades (
                    url TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    fuente TEXT,
                    impacto INTEGER,
                    fecha_descubrimiento TEXT NOT NULL,
                    ultima_actualizacion TEXT NOT NULL
                )
            """)
            conn.commit()
            print(f"Base de datos '{DB_PATH}' inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")

def registrar_habilidad(url, nombre, fuente, impacto):
    """
    Registra una nueva habilidad o actualiza una existente en la base de datos.
    """
    ahora = datetime.datetime.now().isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Intenta insertar. Si la URL ya existe, la actualiza (ON CONFLICT).
            cursor.execute("""
                INSERT INTO habilidades (url, nombre, fuente, impacto, fecha_descubrimiento, ultima_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    impacto = excluded.impacto,
                    ultima_actualizacion = excluded.ultima_actualizacion;
            """, (url, nombre, fuente, impacto, ahora, ahora))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error al registrar la habilidad {url}: {e}")

if __name__ == "__main__":
    # Si se ejecuta directamente, solo inicializa la base de datos.
    inicializar_db()
