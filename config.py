# config.py
# Archivo de configuración para el indexador parser_maestro.py

# Lista de directorios a escanear.
# Añade aquí las rutas a tus carpetas locales y a los puntos de montaje de rclone.
# Ejemplo:
# DIRECTORIOS_A_ESCANEAR = [
#     "/workspaces/henkocorps_jupyter/hilos maestros",  # Carpeta local
#     "/home/ubuntu/gdrive",                         # Montaje de Google Drive
#     "/home/ubuntu/onedrive",                       # Montaje de OneDrive
# ]
DIRECTORIOS_A_ESCANEAR = [
    "/workspaces/henkocorps_jupyter" # Por defecto, escanea el workspace actual
]

# Nombre del archivo de salida para el índice.
ARCHIVO_INDICE_SALIDA = "indice_maestro.txt"

# Nombres de los remotes de rclone que corresponden a Google Drive.
# El script usará 'rclone link' para estos para obtener el webviewlink.
REMOTES_GDRIVE = ["gdrive"] # Añade aquí los nombres de tus remotes de gdrive

# Archivo para guardar el estado de la última indexación (timestamp).
ARCHIVO_ESTADO = "index_state.json"
