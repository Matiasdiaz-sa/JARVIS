const bmoScreen = document.querySelector('.bmo-screen');
const statusText = document.getElementById('status-text');

let currentState = 'esperando';

function updateState(newState) {
    if (currentState === newState) return;
    
    // Remove old state class
    bmoScreen.classList.remove(`state-${currentState}`);
    
    // Add new state class
    bmoScreen.classList.add(`state-${newState}`);
    
    // Update text
    statusText.innerText = newState;
    
    currentState = newState;
}

// Inicializar con estado base
bmoScreen.classList.add(`state-${currentState}`);
statusText.innerText = 'INICIANDO...';

// Polling local server for state updates
async function pollState() {
    try {
        const response = await fetch('/api/estado');
        if (response.ok) {
            const data = await response.json();
            updateState(data.estado);
        }
    } catch (error) {
        console.error('Error polling state:', error);
    }
}

// Poll every 150ms for snappy reactions
setInterval(pollState, 150);
