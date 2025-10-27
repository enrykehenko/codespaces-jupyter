# vigia.py
# Agente Vigía de la Fortaleza Cósmica
# Misión: Descubrir y evaluar nuevas herramientas de IA.

import requests
from bs4 import BeautifulSoup
import re

# --- CONFIGURACIÓN DEL AGENTE ---
FUENTES_DE_INTELIGENCIA = {
    "Hacker News AI": "https://news.ycombinator.com/t/ai",
    "GitHub Trending Python": "https://github.com/trending/python?since=daily",
    "Papers with Code": "https://paperswithcode.com/latest"
}

# Regex para identificar repositorios de GitHub
GITHUB_REGEX = re.compile(r'https://github\.com/[\w\-]+/[\w\-]+')

def analizar_impacto(url_repo):
    """
    Estima el impacto de una herramienta.
    Versión inicial: Simula la puntuación.
    Versión futura: Se conectará a la API de GitHub para obtener estrellas, forks, etc.
    """
    # Simulación: Asigna una puntuación aleatoria de impacto.
    from random import randint
    return randint(1, 1000)

def escanear_fuente(nombre_fuente, url):
    """
    Escanea una única fuente de inteligencia y extrae herramientas de IA.
    """
    print(f"--- Escaneando fuente: {nombre_fuente} ({url}) ---")
    habilidades_encontradas = {}
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status() # Lanza un error si la petición falla

        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los enlaces que coincidan con el patrón de GitHub
        enlaces = soup.find_all('a', href=True)
        repositorios = set()

        for link in enlaces:
            match = GITHUB_REGEX.search(link['href'])
            if match:
                repositorios.add(match.group(0))

        print(f"Se encontraron {len(repositorios)} repositorios únicos.")

        for repo in repositorios:
            impacto = analizar_impacto(repo)
            habilidades_encontradas[repo] = {
                "nombre": repo.split('/')[-1],
                "fuente": nombre_fuente,
                "impacto": impacto
            }

    except requests.RequestException as e:
        print(f"Error al acceder a la fuente {nombre_fuente}: {e}")

    return habilidades_encontradas

def main():
    """
    Punto de entrada principal para el Agente Vigía.
    """
    print("Iniciando ciclo de vigilancia de la Fortaleza Cósmica...")
    arsenal_potencial = {}

    for nombre, url in FUENTES_DE_INTELIGENCIA.items():
        habilidades = escanear_fuente(nombre, url)
        arsenal_potencial.update(habilidades)

    print("\n--- Informe de Vigilancia Finalizado ---")
    if not arsenal_potencial:
        print("No se han descubierto nuevas habilidades en este ciclo.")
        return

    # Ordenar las herramientas por impacto descendente
    habilidades_ordenadas = sorted(
        arsenal_potencial.items(),
        key=lambda item: item[1]['impacto'],
        reverse=True
    )

    print(f"Se han identificado {len(habilidades_ordenadas)} habilidades potenciales.")

    # --- FASE 2: Registrar en la Armería Central ---
    import registro_habilidades
    registro_habilidades.inicializar_db() # Asegura que la DB y la tabla existan

    print("\nRegistrando habilidades en la armería...")
    for repo_url, datos in habilidades_ordenadas:
        registro_habilidades.registrar_habilidad(
            url=repo_url,
            nombre=datos['nombre'],
            fuente=datos['fuente'],
            impacto=datos['impacto']
        )

    print(f"Registro completado. {len(habilidades_ordenadas)} habilidades guardadas/actualizadas en '{registro_habilidades.DB_PATH}'.")

    # Mostrar el top 10 para confirmación
    print("\nTop 10 habilidades descubiertas:")
    for repo_url, datos in habilidades_ordenadas[:10]:
        print(f"  - [{datos['nombre']}] (Impacto: {datos['impacto']}) -> {repo_url}")


if __name__ == "__main__":
    main()
