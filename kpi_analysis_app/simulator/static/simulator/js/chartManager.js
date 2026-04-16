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
    const container = document.getElementById('kpiIndicators');
    container.innerHTML = `
        <p><strong>Коэффициент использования оборудования:</strong> ${kpiData.equipment_utilization_rate} %</p>
        <p><strong>Производительность труда:</strong> ${kpiData.labor_productivity} т/чел*час</p>
        <p><strong>Удельный расход топлива:</strong> ${kpiData.fuel_efficiency} л/т</p>
        <p><strong>Фактический темп добычи:</strong> ${kpiData.actual_production_rate} т/час</p>
    `;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', initChart);