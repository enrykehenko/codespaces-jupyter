# parser_maestro.py
# Agente: A2 Aethereon (Especialista en Datos y Automatización)
# Misión: Generar el Índice Maestro de la Fortaleza Cósmica.

import os
import subprocess
import datetime
import json
import config

def obtener_link(ruta_completa):
    """
    Obtiene el 'webviewlink' para archivos en remotes de Google Drive a través de rclone,
    o la ruta absoluta para archivos locales.
    """
    for remote in config.REMOTES_GDRIVE:
        partes = ruta_completa.split(os.sep)
        try:
            idx = partes.index(remote)
            punto_montaje = os.sep.join(partes[:idx + 1])
            ruta_relativa = os.path.relpath(ruta_completa, punto_montaje)

            comando = ["rclone", "link", f"{remote}:{ruta_relativa}"]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
            return resultado.stdout.strip()
        except (ValueError, subprocess.CalledProcessError):
            continue

    return os.path.abspath(ruta_completa)

def cargar_estado():
    """Carga el timestamp de la última ejecución."""
    if not os.path.exists(config.ARCHIVO_ESTADO):
        return 0
    try:
        with open(config.ARCHIVO_ESTADO, "r") as f:
            return json.load(f).get("ultimo_escaneo", 0)
    except (json.JSONDecodeError, IOError):
        return 0

def guardar_estado(timestamp):
    """Guarda el timestamp de la ejecución actual."""
    try:
        with open(config.ARCHIVO_ESTADO, "w") as f:
            json.dump({"ultimo_escaneo": timestamp}, f)
    except IOError as e:
        print(f"Advertencia: No se pudo guardar el estado: {e}")

def cargar_indice_existente():
    """Carga el índice existente en un diccionario para una actualización eficiente."""
    indice = {}
    if not os.path.exists(config.ARCHIVO_INDICE_SALIDA):
        return indice
    try:
        with open(config.ARCHIVO_INDICE_SALIDA, "r", encoding="utf-8") as f:
            for linea in f:
                try:
                    _, _, _, link = linea.strip().split("|", 3)
                    indice[link] = linea.strip()
                except ValueError:
                    continue
        return indice
    except IOError:
        return {}

def generar_indice():
    """
    Escanea los directorios y actualiza el índice maestro de forma incremental.
    """
    print("Iniciando actualización incremental del Índice Maestro...")

    ultimo_escaneo = cargar_estado()
    ahora = datetime.datetime.now().timestamp()
    indice_actual = cargar_indice_existente()
    archivos_procesados = 0

    for directorio in config.DIRECTORIOS_A_ESCANEAR:
        print(f"Escaneando: {directorio}...")
        for raiz, _, archivos in os.walk(directorio):
            for nombre_archivo in archivos:
                try:
                    ruta_completa = os.path.join(raiz, nombre_archivo)
                    stats = os.stat(ruta_completa)

                    if stats.st_mtime > ultimo_escaneo:
                        archivos_procesados += 1
                        fecha_mod = datetime.datetime.fromtimestamp(stats.st_mtime).isoformat()
                        tamaño_mb = stats.st_size / (1024 * 1024)
                        link = obtener_link(ruta_completa)
                        linea = f"{nombre_archivo}|{fecha_mod}|{tamaño_mb:.4f}MB|{link}"
                        indice_actual[link] = linea

                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"Error procesando {ruta_completa}: {e}")

    if archivos_procesados > 0:
        print(f"Escaneo completo. {archivos_procesados} archivos nuevos/modificados procesados.")
        try:
            entradas_ordenadas = sorted(indice_actual.values(), key=lambda x: x.split('|')[1], reverse=True)
            with open(config.ARCHIVO_INDICE_SALIDA, "w", encoding="utf-8") as f:
                f.write("\n".join(entradas_ordenadas))
            print(f"Índice Maestro actualizado en: {config.ARCHIVO_INDICE_SALIDA}")
            guardar_estado(ahora)
            print("Estado de la indexación actualizado.")
        except Exception as e:
            print(f"Error al escribir el índice: {e}")
    else:
        print("No se encontraron archivos nuevos o modificados. El índice está al día.")

if __name__ == "__main__":
    generar_indice()
