export { updateCharts, updateIndicators };
export { initChart };

let kpiChart = null;

function initChart() {
    const ctx = document.getElementById('kpiChart').getContext('2d');
    kpiChart = new Chart(ctx, {
        type: 'bar', // или 'radar' для другого представления
        data: {
            labels: ['Исп. оборудования', 'Произв. труда', 'Расход топлива', 'Темп добычи'],
            datasets: [{
                label: 'Значение KPI',
                data: [0, 0, 0, 0],
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function updateCharts(kpiData) {
    if (!kpiChart) initChart();

    const data = [
        kpiData.equipment_utilization_rate,
        kpiData.labor_productivity,
        kpiData.fuel_efficiency,
        kpiData.actual_production_rate
    ];

    kpiChart.data.datasets[0].data = data;
    kpiChart.update();
}

function updateIndicators(kpiData) {
    // Обновляем отдельные элементы, не трогая интерпретацию
    const equipmentEl = document.getElementById('equipment_value');
    if (equipmentEl) equipmentEl.innerText = kpiData.equipment_utilization_rate;

    const productivityEl = document.getElementById('productivity_value');
    if (productivityEl) productivityEl.innerText = kpiData.labor_productivity;

    const fuelEl = document.getElementById('fuel_value');
    if (fuelEl) fuelEl.innerText = kpiData.fuel_efficiency;

    const rateEl = document.getElementById('rate_value');
    if (rateEl) rateEl.innerText = kpiData.actual_production_rate;
}

// Инициализация при загрузке страницы
//document.addEventListener('DOMContentLoaded', initChart);