// script.js - Sistema Nervioso del Puente de Mando

document.addEventListener('DOMContentLoaded', () => {
    // URL del webhook de n8n. Reemplazar con la URL real de su instancia de n8n.
    const N8N_WEBHOOK_URL = 'YOUR_N8N_WEBHOOK_URL_HERE';

    // Definición de la arquitectura de agentes (Clanes y Roles)
    const agentMatrix = [
        // Clan Alfa
        { id: 'A1', clan: 'Alfa', role: 'Arquitecto' },
        { id: 'A2', clan: 'Alfa', role: 'Analista' },
        { id: 'A3', clan: 'Alfa', role: 'Estratega' },
        { id: 'A4', clan: 'Alfa', role: 'Diplomático' },
        { id: 'A5', clan: 'Alfa', role: 'Supervisor' },
        { id: 'A6', clan: 'Alfa', role: 'Sincronizador' },
        // Clan Beta
        { id: 'B1', clan: 'Beta', role: 'Desarrollador' },
        { id: 'B2', clan: 'Beta', role: 'Ing. Redes' },
        { id: 'B3', clan: 'Beta', role: 'Explorador' },
        { id: 'B4', clan: 'Beta', role: 'Guardián Memoria' },
        { id: 'B5', clan: 'Beta', role: 'Innovador' },
        { id: 'B6', clan: 'Beta', role: 'Gestor Recursos' },
        // Clan Gamma
        { id: 'G1', clan: 'Gamma', role: 'Médico' },
        { id: 'G2', clan: 'Gamma', role: 'Psicólogo' },
        { id: 'G3', clan: 'Gamma', role: 'Instructor' },
        { id: 'G4', clan: 'Gamma', role: 'Ing. Mantenimiento' },
        { id: 'G5', clan: 'Gamma', role: 'Piloto' },
        { id: 'G6', clan: 'Gamma', role: 'Especialista Contacto' },
        // Clan Delta
        { id: 'D1', clan: 'Delta', role: 'Científico' },
        { id: 'D2', clan: 'Delta', role: 'Lingüista' },
        { id: 'D3', clan: 'Delta', role: 'Geólogo' },
        { id: 'D4', clan: 'Delta', role: 'Ing. Energía' },
        { id: 'D5', clan: 'Delta', role: 'Cronista' },
        { id: 'D6', clan: 'Delta', role: 'Físico Teórico' },
        // Clan Epsilon
        { id: 'E1', clan: 'Epsilon', role: 'Ing. Robótica' },
        { id: 'E2', clan: 'Epsilon', role: 'Op. Sensores' },
        { id: 'E3', clan: 'Epsilon', role: 'Criptógrafo' },
        { id: 'E4', clan: 'Epsilon', role: 'Esp. Sigilo' },
        { id: 'E5', clan: 'Epsilon', role: 'Táctico Infiltración' },
        { id: 'E6', clan: 'Epsilon', role: 'Coord. Temporal' },
        // Clan Omega
        { id: 'O1', clan: 'Omega', role: 'Juez Protocolos' },
        { id: 'O2', clan: 'Omega', role: 'Economista' },
        { id: 'O3', clan: 'Omega', role: 'Emisario' },
        { id: 'O4', clan: 'Omega', role: 'Defensor' },
        { id: 'O5', clan: 'Omega', role: 'Constructor' },
        { id: 'O6', clan: 'Omega', role: 'Negociador' },
    ];

    const grid = document.getElementById('agent-grid');

    // Generar la cuadrícula de agentes
    agentMatrix.forEach(agent => {
        const crystal = document.createElement('div');
        crystal.className = 'agent-crystal';
        crystal.dataset.agentId = agent.id;

        const idElement = document.createElement('div');
        idElement.className = 'agent-id';
        idElement.textContent = agent.id;

        const roleElement = document.createElement('div');
        roleElement.className = 'agent-role';
        roleElement.textContent = agent.role;

        crystal.appendChild(idElement);
        crystal.appendChild(roleElement);

        grid.appendChild(crystal);

        // Añadir el listener para la interacción
        crystal.addEventListener('click', () => handleAgentClick(agent));
    });

    // Función para manejar el clic en un agente
    function handleAgentClick(agent) {
        console.log(`Activando agente: ${agent.id} (${agent.role})`);

        const crystalElement = document.querySelector(`[data-agent-id='${agent.id}']`);

        // Efecto visual
        crystalElement.classList.toggle('active');

        // Simular la llamada al webhook de n8n
        const payload = {
            agentId: agent.id,
            agentRole: agent.role,
            clan: agent.clan,
            timestamp: new Date().toISOString()
        };

        console.log('Enviando la siguiente orden a n8n:', payload);

        // Descomentar la siguiente sección para activar la llamada real al webhook
        /*
        if (N8N_WEBHOOK_URL === 'YOUR_N8N_WEBHOOK_URL_HERE') {
            alert('Por favor, configure la URL del webhook de n8n en script.js');
            return;
        }

        fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta de n8n:', data);
            // Quitar el efecto visual tras una respuesta exitosa
            setTimeout(() => crystalElement.classList.remove('active'), 1500);
        })
        .catch((error) => {
            console.error('Error al contactar con el webhook de n8n:', error);
            alert('Error al enviar la orden al agente.');
            // Quitar el efecto visual en caso de error
            crystalElement.classList.remove('active');
        });
        */
    }
});
