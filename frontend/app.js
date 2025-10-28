document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:8000'; // Asumiendo que el backend corre en el puerto 8000

    // --- Selectores de Elementos del DOM ---
    const apiStatusIndicator = document.getElementById('api-status');
    const desktopControlsContainer = document.getElementById('desktop-controls');
    const audioControlsContainer = document.getElementById('audio-controls');
    const startFlowBtn = document.getElementById('start-flow-btn');
    const startMessageInput = document.getElementById('start-message-input');
    const activeFlowsList = document.getElementById('active-flows-list');

    // --- Funciones de Renderizado ---

    const renderDesktopControl = (binomioId, data) => {
        const card = document.createElement('div');
        card.className = 'control-card';
        card.innerHTML = `
            <h4>${binomioId.replace('_', ' ')}</h4>
            <label>
                <input type="checkbox" class="desktop-active" data-id="${binomioId}" ${data.active ? 'checked' : ''}>
                Activo
            </label>
            <label>
                Monitor:
                <select class="desktop-monitor" data-id="${binomioId}">
                    <option value="1" ${data.monitor === 1 ? 'selected' : ''}>1</option>
                    <option value="2" ${data.monitor === 2 ? 'selected' : ''}>2</option>
                    <option value="3" ${data.monitor === 3 ? 'selected' : ''}>3</option>
                </select>
            </label>
        `;
        desktopControlsContainer.appendChild(card);
    };

    const renderAudioControl = (agentId, data) => {
        const card = document.createElement('div');
        card.className = 'control-card';
        card.innerHTML = `
            <h4>${agentId.replace('_', ' ')}</h4>
            <label>
                <input type="checkbox" class="audio-active" data-id="${agentId}" ${data.active ? 'checked' : ''}>
                Activo
            </label>
            <label>
                Volumen:
                <input type="range" class="audio-volume" data-id="${agentId}" min="0" max="100" value="${data.volume}">
                <span class="volume-display">${data.volume}</span>
            </label>
        `;
        audioControlsContainer.appendChild(card);
    };

    const addFlowToList = (flow) => {
        const listItem = document.createElement('li');
        listItem.id = `flow-${flow.flow_id}`;
        listItem.innerHTML = `
            <strong>ID:</strong> ${flow.flow_id.substring(0, 8)}... | <strong>Estado:</strong> ${flow.status}
            <br>
            <em>${flow.start_message}</em>
        `;
        activeFlowsList.prepend(listItem);
    };


    // --- Lógica de la API ---

    const checkApiStatus = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/`);
            if (response.ok) {
                apiStatusIndicator.textContent = 'API Online';
                apiStatusIndicator.className = 'status-indicator-green';
                return true;
            }
        } catch (error) {
            console.error('API connection failed:', error);
        }
        apiStatusIndicator.textContent = 'API Offline';
        apiStatusIndicator.className = 'status-indicator-red';
        return false;
    };

    const loadInitialState = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/status/all`);
            const state = await response.json();

            desktopControlsContainer.innerHTML = '';
            for (const [id, data] of Object.entries(state.virtual_desktops)) {
                renderDesktopControl(id, data);
            }

            audioControlsContainer.innerHTML = '';
            for (const [id, data] of Object.entries(state.audio_channels)) {
                renderAudioControl(id, data);
            }
        } catch (error) {
            console.error('Failed to load initial state:', error);
        }
    };

    const startFlow = async () => {
        const message = startMessageInput.value;
        if (!message) {
            alert('Por favor, escribe un mensaje para iniciar el flujo.');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/flow/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ start_message: message }),
            });
            const flow = await response.json();
            if (response.ok) {
                addFlowToList(flow);
                startMessageInput.value = '';
            } else {
                alert(`Error al iniciar el flujo: ${flow.detail || 'Error desconocido'}`);
            }
        } catch (error) {
            console.error('Failed to start flow:', error);
        }
    };

    // --- Inicialización y Event Listeners ---

    const updateBackend = async (endpoint, data) => {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                console.error(`Error updating backend at ${endpoint}:`, await response.json());
            }
        } catch (error) {
            console.error(`Failed to send update to ${endpoint}:`, error);
        }
    };

    // --- Inicialización y Event Listeners ---

    const init = async () => {
        if (await checkApiStatus()) {
            await loadInitialState();
        }
        // Comprobar el estado de la API periódicamente
        setInterval(checkApiStatus, 10000);

        startFlowBtn.addEventListener('click', startFlow);

        // Listeners para los controles (delegación de eventos)
        desktopControlsContainer.addEventListener('change', (e) => {
            const target = e.target;
            const id = target.dataset.id;
            if (!id) return;

            const card = target.closest('.control-card');
            const active = card.querySelector('.desktop-active').checked;
            const monitor = parseInt(card.querySelector('.desktop-monitor').value, 10);

            updateBackend(`/control/desktop/${id}`, { active, monitor });
        });

        audioControlsContainer.addEventListener('change', (e) => {
            const target = e.target;
            const id = target.dataset.id;
            if (!id) return;

            const card = target.closest('.control-card');
            const active = card.querySelector('.audio-active').checked;
            const volume = parseInt(card.querySelector('.audio-volume').value, 10);
            card.querySelector('.volume-display').textContent = volume;

            updateBackend(`/control/audio/${id}`, { active, volume });
        });
    };

    init();
});