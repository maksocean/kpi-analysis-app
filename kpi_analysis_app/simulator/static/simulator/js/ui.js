import { updateCharts } from './chartManager.js';

export function updateKPIDisplay(kpis) {
    document.getElementById('equipment_value').innerText = kpis.equipment_utilization_rate;
    document.getElementById('productivity_value').innerText = kpis.labor_productivity;
    document.getElementById('fuel_value').innerText = kpis.fuel_efficiency;
    document.getElementById('rate_value').innerText = kpis.actual_production_rate;
    updateCharts(kpis);
}

export function updateInterpretation(interpretation) {
    document.getElementById('interpret_equipment').innerText = interpretation.equipment_utilization_rate;
    document.getElementById('interpret_productivity').innerText = interpretation.labor_productivity;
    document.getElementById('interpret_fuel').innerText = interpretation.fuel_efficiency;
    document.getElementById('interpret_rate').innerText = interpretation.actual_production_rate;
}

export function populateScenarioSelect(select, scenarios) {
    select.innerHTML = '<option value="">-- Сценарий --</option>';
    scenarios.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = `${s.date} | Руда:${s.ore_volume}т | Время:${s.operating_time}ч`;
        select.appendChild(opt);
    });
}

export function showError(msg) { alert(msg); }