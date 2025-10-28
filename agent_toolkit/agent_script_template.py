import requests
import time
import sys
import os

# --- Configuración ---
API_BASE_URL = "http://127.0.0.1:8000"
POLL_INTERVAL = 5  # Segundos entre cada búsqueda de trabajo

def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_my_task(agent_name: str):
    """Busca en el backend una tarea asignada a este agente."""
    try:
        response = requests.get(f"{API_BASE_URL}/flows/active")
        response.raise_for_status()
        active_flows = response.json()

        for flow in active_flows:
            for step in flow['steps']:
                if step['agent'] == agent_name and step['status'] == 'in_progress':
                    return flow, step
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] No se pudo conectar con el servidor: {e}")
        return None, None

def complete_my_task(flow_id: str, step_index: int, message: str):
    """Envía el resultado de la tarea al backend."""
    try:
        payload = {
            "flow_id": flow_id,
            "step_index": step_index,
            "message": message
        }
        response = requests.post(f"{API_BASE_URL}/flow/step/complete", json=payload)
        response.raise_for_status()
        print("\n[INFO] Tarea completada y enviada con éxito.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] No se pudo completar la tarea: {e}")
        return None

def main(agent_name: str):
    """Bucle principal del agente."""
    clear_screen()
    print("=====================================================")
    print(f"  Terminal del Agente: {agent_name}")
    print("=====================================================")
    print(f"Buscando tareas cada {POLL_INTERVAL} segundos...")

    while True:
        try:
            flow, task = find_my_task(agent_name)

            if task:
                clear_screen()
                print("=====================================================")
                print(f"  NUEVA TAREA PARA: {agent_name}")
                print("=====================================================")
                print(f"\n[Flujo ID]: {flow['flow_id']}")
                print(f"[Paso {task['step_index']}]: Tarea recibida.")
                print("\n------------------- MENSAJE RECIBIDO --------------------")
                print(f"  {task['message']}")
                print("-------------------------------------------------------")

                response_message = input("\n> Introduce tu respuesta y presiona Enter: ")

                complete_my_task(flow['flow_id'], task['step_index'], response_message)

                print("\nVolviendo al modo de espera...")
                time.sleep(POLL_INTERVAL)

            else:
                # Imprimir un punto en la misma línea para mostrar que está funcionando
                print(".", end='', flush=True)
                time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n\nCerrando terminal del agente. ¡Adiós!")
            break
        except Exception as e:
            print(f"\n[ERROR INESPERADO] {e}")
            time.sleep(POLL_INTERVAL * 2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python agent_script_template.py <nombre_del_agente>")
        print("Ejemplo: python agent_script_template.py Delta-Apolo")
        sys.exit(1)

    agent_name_arg = sys.argv[1]
    main(agent_name_arg)