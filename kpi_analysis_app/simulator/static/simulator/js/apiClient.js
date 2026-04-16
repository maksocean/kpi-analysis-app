const API_URL = '/simulator/api/calculate/';

async function calculateKPIs() {
    const formData = {
        ore_volume: parseFloat(document.getElementById('ore_volume').value),
        operating_time: parseFloat(document.getElementById('operating_time').value),
        downtime: parseFloat(document.getElementById('downtime').value),
        crew_size: parseInt(document.getElementById('crew_size').value),
        fuel_consumption: parseFloat(document.getElementById('fuel_consumption').value)
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Не забудьте реализовать получение CSRF-токена
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const kpiData = await response.json();
        updateCharts(kpiData); // Функция из chartManager.js
        updateIndicators(kpiData);

    } catch (error) {
        console.error('Ошибка при расчёте KPI:', error);
        alert('Произошла ошибка при расчёте. Проверьте консоль.');
    }
}

// Базовая функция для получения CSRF-токена (упрощённо)
function getCsrfToken() {
    return document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || '';
}