# web_mapper.py
# Cartógrafo Digital de la Fortaleza Cósmica
# Misión: Analizar una URL y generar un mapa estructural para la navegación autónoma.

import requests
from bs4 import BeautifulSoup
import re

def generar_mapa_estructural(url):
    """
    Analiza el HTML de una URL y genera un mapa heurístico de las zonas de interacción.
    """
    print(f"Mapeando estructura de: {url}")
    mapa = {
        "zona_pregunta": None,
        "boton_enviar": None,
        "zona_respuesta": None,
        "gaps_detectados": [] # Para futura navegación
    }

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Heurística 1: Encontrar el área de texto principal para la pregunta.
        # Buscamos textareas, especialmente con IDs o nombres sugerentes.
        pregunta_input = soup.find('textarea', {'id': re.compile(r'prompt|input|query', re.I)})
        if not pregunta_input:
            pregunta_input = soup.find('textarea')
        if pregunta_input:
            mapa['zona_pregunta'] = f"textarea#{pregunta_input.get('id')}" if pregunta_input.get('id') else "textarea"

        # Heurística 2: Encontrar el botón de envío.
        # Buscamos botones con texto o data-testid sugerentes.
        boton_enviar = soup.find('button', {'data-testid': re.compile(r'send|submit', re.I)})
        if not boton_enviar:
            boton_enviar = soup.find('button', string=re.compile(r'Send|Submit|Enviar|>', re.I))
        if boton_enviar:
            mapa['boton_enviar'] = f"button[data-testid='{boton_enviar.get('data-testid')}']" if boton_enviar.get('data-testid') else "button"


        # Heurística 3: Encontrar la zona de respuesta.
        # Buscamos contenedores que suelen albergar conversaciones (roles, clases).
        zona_respuesta = soup.find('div', {'role': 'log'})
        if not zona_respuesta:
             zona_respuesta = soup.find('div', class_=re.compile(r'conversation|chat|response', re.I))
        if zona_respuesta:
            mapa['zona_respuesta'] = f"div[role='{zona_respuesta.get('role')}']" if zona_respuesta.get('role') else f"div.{'.'.join(zona_respuesta.get('class',[]))}"

        print("Mapeo completado.")
        return mapa

    except requests.RequestException as e:
        print(f"Error al acceder a la URL para mapeo: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado durante el mapeo: {e}")
        return None

if __name__ == "__main__":
    # URL de ejemplo para la prueba
    url_prueba = "https://www.google.com" # Usamos Google como ejemplo simple

    mapa_resultado = generar_mapa_estructural(url_prueba)

    if mapa_resultado:
        import json
        print("\n--- Mapa Estructural Generado ---")
        print(json.dumps(mapa_resultado, indent=2))

        # Ahora, integramos con el Escriba para registrar este hallazgo
        import escriba
        escriba.inicializar_db()
        escriba.registrar_interaccion(
            url=url_prueba,
            transcripcion="[SISTEMA] Mapeo estructural inicial completado.",
            mapa_estructural=mapa_resultado,
            agente_horario="WebMapper"
        )

# Necesitaremos importar 're' para las expresiones regulares en las heurísticas.
import re
