import os
import random
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import UUID, uuid4
import obsws_python as obs
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# --- Configuración ---
# Se recomienda usar variables de entorno para las claves de API y contraseñas.
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "YOUR_OBS_WEBSOCKET_PASSWORD") # ¡CAMBIAR ESTO!

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY") # ¡CAMBIAR ESTO!
# elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# --- Modelos de Datos (Pydantic) ---

class AudioChannel(BaseModel):
    active: bool = True
    volume: int = Field(100, ge=0, le=100)

class VirtualDesktop(BaseModel):
    active: bool = True
    monitor: int = Field(1, ge=1, le=3)

class SystemState(BaseModel):
    audio_channels: Dict[str, AudioChannel] = {f"agent_{i+1}": AudioChannel() for i in range(36)}
    virtual_desktops: Dict[str, VirtualDesktop] = {f"binomio_{i+1}": VirtualDesktop(monitor=(i % 3) + 1) for i in range(18)}

class FlowStep(BaseModel):
    step_index: int
    agent: str
    status: str = "pending"
    message: Optional[str] = None

class CommunicationFlow(BaseModel):
    flow_id: UUID = Field(default_factory=uuid4)
    status: str = "initiated"
    start_message: str
    steps: List[FlowStep] = []

# --- Base de Datos en Memoria (simulada) ---

AGENT_GRID = {
    "Alpha": ["Synaptic", "Aethereon", "Comet", "Andrew", "Concordia", "Jules"],
    "Beta": ["Gemmye", "Nexus", "Cove", "Gemini CLI", "Kimi2 + Claude", "Grock 4 CLI"],
    "Delta": ["Apolo", "Sebastian", "Ariel", "Fuse Base Agent", "Win-Core", "Space"],
    "Epsylon": ["Jenkins", "Moon", "Gideon", "Context7 Agent", "Octavius", "Oráculo"],
    "Gamma": ["Regina", "Valentina", "Shaiky", "Codex", "Gordon", "Bytebot"],
    "Omega": ["Alejandro", "Wright Data", "Gemini CLI", "Termux CLI", "Roboneo Agent", "Connectia"]
}

BINOMIOS = [
    "IA - Gestor Tareas", "IA - Agente", "IA - Prompting", "IA - Supervisor", "IA - Project Manager",
    "Gestor Tareas - Agente", "Gestor Tareas - Prompting", "Gestor Tareas - Supervisor", "Gestor Tareas - Project Manager",
    "Agente - Prompting", "Agente - Supervisor", "Agente - Project Manager",
    "Prompting - Supervisor", "Prompting - Project Manager",
    "Supervisor - Project Manager",
    "Henko - IA", "Henko - Gestor Tareas", "Henko - Agente"
]

# Estado del sistema y flujos activos
system_state = SystemState()
active_flows: Dict[UUID, CommunicationFlow] = {}


# --- Aplicación FastAPI ---

app = FastAPI(
    title="HenkoCorps Agent Orchestrator",
    description="API para controlar el ecosistema de 36 agentes, flujos de comunicación y OBS.",
    version="0.1.0"
)

# --- Middleware ---
# Configuración de CORS para permitir que el frontend (servido desde file://) se conecte.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)


@app.get("/", tags=["Status"])
async def read_root():
    """Endpoint raíz para verificar que el servidor está en funcionamiento."""
    return {"status": "ok", "message": "Agent Orchestrator API is running."}

# --- Endpoints de Información ---

@app.get("/agents", tags=["Information"], response_model=Dict[str, List[str]])
async def get_agents():
    """Devuelve la parrilla completa de agentes."""
    return AGENT_GRID

@app.get("/binomios", tags=["Information"], response_model=List[str])
async def get_binomios():
    """Devuelve la lista de los 18 binomios de trabajo."""
    return BINOMIOS

# --- Endpoints de Control (esqueleto) ---

# --- Endpoints de Control ---

@app.get("/status/all", tags=["Control"], response_model=SystemState)
async def get_full_status():
    """Devuelve el estado completo del sistema (canales de audio y escritorios)."""
    return system_state

@app.post("/control/audio/{agent_id}", tags=["Control"], response_model=AudioChannel)
async def control_audio_channel(agent_id: str, channel_data: AudioChannel):
    """Controla un canal de audio específico."""
    # Lógica de control de audio aquí (ej: guardar en BD, enviar a un servicio)
    if agent_id not in system_state.audio_channels:
        # En una app real, se lanzaría HTTPException(status_code=404)
        return {"error": "Agent ID not found"}
    system_state.audio_channels[agent_id] = channel_data
    return system_state.audio_channels[agent_id]

async def speak_message(text: str, agent_name: str):
    """
    Genera y reproduce un mensaje de audio para un agente específico.
    Refinado para simular un tiempo de habla más realista.
    """
    # Mapeo de ejemplo para dar voces únicas a agentes clave.
    # En una implementación real, esto vendría de una base de datos.
    VOICE_MAP = {
        "Delta-Apolo": "Adam",
        "Omega-Alejandro": "Domi",
        "Alpha-Synaptic": "Rachel",
        "Beta-Gemmye": "Bella",
        "Gamma-Regina": "Sarah",
        "Epsylon-Jenkins": "Arnold"
    }
    voice_to_use = VOICE_MAP.get(agent_name, "Rachel") # Voz por defecto

    # Simula el tiempo de habla basado en la longitud del texto.
    # Asumimos una velocidad de habla de ~150 palabras por minuto.
    # 1 palabra ~ 5 caracteres. 150 ppm = 750 cpm = 12.5 cps.
    # Duración = longitud / 12.5
    speech_duration = len(text) / 12.5

    print(f"SPEAKING as {agent_name} (using voice {voice_to_use}) for {speech_duration:.2f}s: '{text}'")
    # try:
    #     audio = elevenlabs_client.generate(text=text, voice=voice_to_use)
    #     play(audio)
    # except Exception as e:
    #     print(f"Error al generar audio para {agent_name}: {e}")
    await asyncio.sleep(speech_duration)


@app.post("/control/desktop/{binomio_id}", tags=["Control"], response_model=VirtualDesktop)
async def control_virtual_desktop(binomio_id: str, desktop_data: VirtualDesktop):
    """Controla un escritorio virtual y cambia la escena en OBS."""
    if binomio_id not in system_state.virtual_desktops:
        raise HTTPException(status_code=404, detail="Binomio ID not found")

    system_state.virtual_desktops[binomio_id] = desktop_data

    # --- Integración con OBS ---
    if desktop_data.active:
        try:
            # El ID es "binomio_1", "binomio_2", etc. El índice es 0, 1, ...
            binomio_index = int(binomio_id.split('_')[1]) - 1
            scene_name = BINOMIOS[binomio_index]

            cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
            await cl.set_current_program_scene(scene_name)
            print(f"OBS scene changed to: {scene_name}")
        except Exception as e:
            print(f"Error connecting to OBS or changing scene: {e}")
            # No lanzar error al frontend, solo registrarlo en el backend.
            # El estado se actualiza igualmente.

    return system_state.virtual_desktops[binomio_id]

# --- Endpoints de Flujo de Comunicación ---

class StartFlowRequest(BaseModel):
    start_message: str
    start_agent: str = "Delta-Apolo"

@app.post("/flow/start", tags=["Flow"], response_model=CommunicationFlow)
async def start_communication_flow(request: StartFlowRequest):
    """Inicia un nuevo flujo de comunicación y vocaliza el mensaje inicial."""
    # Lógica de selección dinámica de agentes para los pasos de estudio.
    study_clans = ["Alpha", "Beta", "Gamma", "Epsylon"]
    study_agents_pool = [agent for clan in study_clans for agent in AGENT_GRID[clan]]

    # Seleccionar 4 agentes de estudio al azar y sin repetición.
    study_group = random.sample(study_agents_pool, 4)

    flow_agents = [
        request.start_agent,
        *study_group,  # Desempaquetar la lista de agentes seleccionados
        "Omega-Alejandro" # Asignar un integrador específico para el final
    ]
    steps = [FlowStep(step_index=i, agent=agent) for i, agent in enumerate(flow_agents)]

    # Crear el nuevo flujo
    new_flow = CommunicationFlow(
        start_message=request.start_message,
        steps=steps
    )
    # Asignar el mensaje inicial al primer paso y marcarlo como en progreso
    new_flow.steps[0].message = request.start_message
    new_flow.steps[0].status = "in_progress"

    active_flows[new_flow.flow_id] = new_flow

    # --- Integración con Voces ---
    # Vocalizar el mensaje de inicio de forma asíncrona
    asyncio.create_task(speak_message(text=request.start_message, agent_name=request.start_agent))

    return new_flow

@app.get("/flow/status/{flow_id}", tags=["Flow"], response_model=CommunicationFlow)
async def get_flow_status(flow_id: UUID):
    """Obtiene el estado de un flujo de comunicación específico."""
    if flow_id not in active_flows:
        raise HTTPException(status_code=404, detail="Flow ID not found")
    return active_flows[flow_id]

class CompleteStepRequest(BaseModel):
    flow_id: UUID
    step_index: int
    message: str

@app.post("/flow/step/complete", tags=["Flow"], response_model=CommunicationFlow)
async def complete_flow_step(request: CompleteStepRequest):
    """Permite a un agente marcar un paso como completado y pasar al siguiente."""
    flow = active_flows.get(request.flow_id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow ID not found")

    if request.step_index >= len(flow.steps):
        raise HTTPException(status_code=400, detail="Invalid step index")

    current_step = flow.steps[request.step_index]
    if current_step.status != "in_progress":
        raise HTTPException(status_code=400, detail=f"Step {request.step_index} is not in progress.")

    current_step.status = "completed"
    current_step.message = request.message

    # Avanzar al siguiente paso, si existe
    next_step_index = request.step_index + 1
    if next_step_index < len(flow.steps):
        next_step = flow.steps[next_step_index]
        next_step.status = "in_progress"
        # El mensaje del agente anterior es el input para el siguiente
        next_step.message = request.message

        # Vocalizar el mensaje para el siguiente agente
        asyncio.create_task(speak_message(text=next_step.message, agent_name=next_step.agent))
    else:
        # El flujo ha terminado
        flow.status = "completed"
        asyncio.create_task(speak_message(text="El flujo de comunicación ha finalizado.", agent_name="System"))

    return flow

@app.get("/flows/active", tags=["Flow"], response_model=List[CommunicationFlow])
async def get_active_flows():
    """Devuelve una lista de todos los flujos de comunicación que no están completados."""
    return [flow for flow in active_flows.values() if flow.status != "completed"]