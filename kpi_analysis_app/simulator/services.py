class MiningKPICalculator:
    """
    Калькулятор ключевых показателей эффективности для горного участка.
    Все расчёты выполняются на основе модели ProductionData.
    """

    def __init__(self, production_data_instance):
        self.data = production_data_instance

    # 1. Коэффициент использования оборудования (Utilization Rate)
    def equipment_utilization_rate(self) -> float:
        """ (T_plan - T_down) / T_plan """
        if self.data.operating_time == 0:
            return 0.0
        return ((self.data.operating_time - self.data.downtime) / self.data.operating_time) * 100  # в процентах

    # 2. Производительность труда (Labor Productivity)
    def labor_productivity(self) -> float:
        """ Q / (N * (T_plan - T_down)) """
        effective_time = self.data.operating_time - self.data.downtime
        if effective_time == 0 or self.data.crew_size == 0:
            return 0.0
        return self.data.ore_volume / (self.data.crew_size * effective_time)  # тонн/чел*час

    # 3. Удельный расход топлива (Fuel Efficiency)
    def fuel_efficiency(self) -> float:
        """ F / Q """
        if self.data.ore_volume == 0:
            return 0.0
        return self.data.fuel_consumption / self.data.ore_volume  # литров/тонну

    # 4. Темп добычи (Ore Production Rate) - Фактический
    def actual_production_rate(self) -> float:
        """ Q / (T_plan - T_down) """
        effective_time = self.data.operating_time - self.data.downtime
        if effective_time == 0:
            return 0.0
        return self.data.ore_volume / effective_time  # тонн/час

    # Метод для получения всех KPI сразу (для API)
    def calculate_all_kpis(self) -> dict:
        return {
            'equipment_utilization_rate': round(self.equipment_utilization_rate(), 2),
            'labor_productivity': round(self.labor_productivity(), 2),
            'fuel_efficiency': round(self.fuel_efficiency(), 2),
            'actual_production_rate': round(self.actual_production_rate(), 2),
            # Дополнительные KPI можно добавить здесь
        }

def interpret_kpi(kpi_name: str, value: float) -> str:
    """Возвращает текстовую интерпретацию KPI для отображения на фронте."""
    if kpi_name == 'equipment_utilization_rate':
        if value < 60:
            return "Критически низкий КИО. Проверьте простои: организационные, ремонты."
        elif value < 85:
            return "КИО ниже целевого (85%). Есть резерв повышения за счёт сокращения простоев."
        else:
            return "КИО в норме (>85%). Хорошая организация работ."

    elif kpi_name == 'labor_productivity':
        if value < 2:
            return "Очень низкая производительность. Аутсорсинг или механизация?"
        elif value < 5:
            return "Средняя производительность. Можно улучшить за счёт бригадной работы."
        else:
            return "Высокая производительность. Эталонный показатель."

    elif kpi_name == 'fuel_efficiency':
        if value < 0.3:
            return "Отличная топливная эффективность (менее 0.3 л/т)."
        elif value < 0.8:
            return "Нормальный удельный расход топлива (0.3–0.8 л/т)."
        else:
            return "Высокий расход топлива (>0.8 л/т). Проверьте состояние техники, маршруты."

    elif kpi_name == 'actual_production_rate':
        if value < 30:
            return "Низкий темп добычи (<30 т/ч). Анализируйте буровзрывные работы, транспорт."
        elif value < 60:
            return "Средний темп добычи (30–60 т/ч)."
        else:
            return "Высокий темп добычи (>60 т/ч). Отличная интенсификация."

    else:
        return "Нет интерпретации для данного KPI."