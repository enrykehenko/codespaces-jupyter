# Manual de Operaciones: Indexador Maestro de la Fortaleza Cósmica

## 1. Directiva Principal

Este documento detalla el procedimiento para configurar y operar el `parser_maestro.py`, el agente de software responsable de crear y mantener el **Índice Maestro Universal** de la Fortaleza Cósmica.

El índice es un archivo de texto plano (`indice_maestro.txt`) que contiene los metadatos y la ubicación (local o `webviewlink`) de cada archivo en el ecosistema de la Fortaleza, permitiendo la consulta y el acceso autónomo a la información por parte de otros agentes.

## 2. Requisitos Previos

- **Python 3.x**: El lenguaje en el que opera el agente.
- **rclone**: La herramienta universal para la sincronización y montaje de unidades en la nube. Debe estar instalado y configurado en el sistema.

## 3. Fase I: Configuración de la Capa de Acceso a Datos (`rclone`)

Antes de que el indexador pueda operar, debe tener acceso a las fuentes de datos remotas.

### 3.1. Configuración de "Remotes"

Para cada servicio en la nube (Google Drive, OneDrive, etc.), debe configurar un "remote" en `rclone`.

1.  Abra una terminal y ejecute:
    ```bash
    rclone config
    ```
2.  Siga el asistente interactivo para cada cuenta que desee indexar:
    -   Presione `n` para un nuevo remote.
    -   Asigne un nombre descriptivo (ej: `gdrive_personal`, `onedrive_trabajo`). **Importante:** Si el remote es de Google Drive, asegúrese de que su nombre esté listado en la variable `REMOTES_GDRIVE` del archivo `config.py` para que el script pueda obtener los `webviewlinks`.
    -   Seleccione el tipo de almacenamiento (`drive`, `onedrive`, etc.).
    -   Complete el proceso de autenticación en su navegador.

### 3.2. Montaje de los "Remotes"

Una vez configurados, los remotes deben ser montados como directorios locales para que el indexador pueda escanearlos.

1.  Cree los directorios que servirán como puntos de montaje:
    ```bash
    mkdir -p ~/gdrive ~/onedrive
    ```
2.  Monte cada remote. Se recomienda ejecutar el comando en segundo plano con `--daemon` (en Linux/macOS):
    ```bash
    rclone mount gdrive_personal: ~/gdrive --daemon
    rclone mount onedrive_trabajo: ~/onedrive --daemon
    ```

## 4. Fase II: Configuración del Indexador

1.  **Editar `config.py`**:
    -   Abra el archivo `config.py`.
    -   Modifique la lista `DIRECTORIOS_A_ESCANEAR` para incluir las rutas a las carpetas locales y a los puntos de montaje de `rclone` que acaba de crear.
    -   Asegúrese de que la lista `REMOTES_GDRIVE` contiene los nombres exactos de los remotes de Google Drive que configuró.

## 5. Fase III: Ejecución

1.  **Instalar dependencias (solo la primera vez)**:
    -   El script no tiene dependencias externas más allá de la librería estándar de Python.

2.  **Ejecutar el Indexador**:
    -   Navegue al directorio donde se encuentra `parser_maestro.py` y ejecute:
        ```bash
        python3 parser_maestro.py
        ```

-   **Primera Ejecución**: El script escaneará todos los archivos en los directorios especificados. Esto puede tardar dependiendo del volumen de datos.
-   **Ejecuciones Posteriores**: El script solo escaneará los archivos nuevos o modificados desde la última ejecución, siendo un proceso mucho más rápido.

## 6. Verificación de Resultados

Una vez finalizada la ejecución, se generarán (o actualizarán) dos archivos:

-   `indice_maestro.txt`: La base de datos de la Fortaleza. Cada línea representa un archivo con el formato: `[Nombre]|[FechaModificación]|[Tamaño]|[Link]`.
-   `index_state.json`: El archivo de memoria del indexador. Contiene un único valor (`ultimo_escaneo`) que le permite saber desde qué punto debe reanudar el trabajo en la siguiente ejecución.

El Índice Maestro está listo para ser consultado por el resto de los agentes. Misión cumplida.
