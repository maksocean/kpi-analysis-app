import { calculateKPIs, exportScenariosToCSV, fetchScenariosList, fetchScenarioById } from './apiClient.js';
import { updateKPIDisplay, updateInterpretation, populateScenarioSelect, showError } from './ui.js';
import { initChart, updateCharts, updateIndicators } from './chartManager.js';

document.addEventListener('DOMContentLoaded', async () => {
    initChart();

    const form = {
        ore_volume: document.getElementById('ore_volume'),
        operating_time: document.getElementById('operating_time'),
        downtime: document.getElementById('downtime'),
        crew_size: document.getElementById('crew_size'),
        fuel_consumption: document.getElementById('fuel_consumption')
    };
    const calcBtn = document.getElementById('calculateBtn');
    const exportBtn = document.getElementById('exportCsvBtn');
    const loadBtn = document.getElementById('loadScenarioBtn');
    const select = document.getElementById('scenarioSelect');

    calcBtn?.addEventListener('click', async () => {
        const data = {
            ore_volume: parseFloat(form.ore_volume.value),
            operating_time: parseFloat(form.operating_time.value),
            downtime: parseFloat(form.downtime.value),
            crew_size: parseInt(form.crew_size.value),
            fuel_consumption: parseFloat(form.fuel_consumption.value)
        };
        try {
            const res = await calculateKPIs(data);
            updateKPIDisplay(res.kpis);
            if (res.interpretation) updateInterpretation(res.interpretation);

            // === ДОБАВИТЬ ЭТОТ БЛОК ===
            // После успешного расчёта обновляем выпадающий список сценариев
            const updatedScenarios = await fetchScenariosList();
            populateScenarioSelect(select, updatedScenarios);
            // ===========================

        } catch (err) {
            showError(err.message);
        }
    });

    exportBtn?.addEventListener('click', exportScenariosToCSV);

    if (loadBtn && select) {
        try {
            const scenarios = await fetchScenariosList();
            populateScenarioSelect(select, scenarios);
        } catch (err) { console.error(err); }

        loadBtn.addEventListener('click', async () => {
            if (!select.value) return;
            try {
                const scenario = await fetchScenarioById(select.value);
                form.ore_volume.value = scenario.ore_volume;
                form.operating_time.value = scenario.operating_time;
                form.downtime.value = scenario.downtime;
                form.crew_size.value = scenario.crew_size;
                form.fuel_consumption.value = scenario.fuel_consumption;
                calcBtn.click();
            } catch (err) {
                showError('Не удалось загрузить сценарий');
            }
        });
    }
});