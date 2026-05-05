const API_BASE = '/simulator/api';

export async function calculateKPIs(formData) {
    const response = await fetch(`${API_BASE}/calculate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || `HTTP ${response.status}`);
    }
    return response.json(); // { id, kpis, interpretation }
}

export async function exportScenariosToCSV() {
    // Простой редирект на CSV (или можно через blob, как у вас)
    window.location.href = `${API_BASE}/export-csv/`;
}

export async function fetchScenariosList() {
    const response = await fetch(`${API_BASE}/scenarios/`);
    return response.json();
}

export async function fetchScenarioById(id) {
    const response = await fetch(`${API_BASE}/scenarios/${id}/`);
    return response.json();
}