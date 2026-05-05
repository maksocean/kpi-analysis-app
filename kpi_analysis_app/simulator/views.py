from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import KPICalculatorInputSerializer, ProductionDataSerializer
from .services import MiningKPICalculator, interpret_kpi
from .models import ProductionData
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import csv

def dashboard_view(request):
    return render(request, 'simulator/dashboard.html')

@method_decorator(csrf_exempt, name='dispatch')
class CalculateKPIView(APIView):
    """
    Эндпоинт для расчёта KPI на основе переданных параметров.
    Принимает POST-запрос с JSON.
    """
    def post(self, request):
        serializer = KPICalculatorInputSerializer(data=request.data)
        if serializer.is_valid():
            # Создаём объект модели из валидированных данных
            production_data = ProductionData.objects.create(**serializer.validated_data)
            # Вызываем калькулятор
            calculator = MiningKPICalculator(production_data)
            kpis = calculator.calculate_all_kpis()
            # Добавляем интерпретацию для каждого KPI
            interpretation = {
                key: interpret_kpi(key, value)
                for key, value in kpis.items()
            }
            # Возвращаем результат + ID сценария (чтобы потом экспортировать)
            return Response({
                'id': production_data.id,
                'kpis': kpis,
                'interpretation': interpretation
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ListScenariosView(APIView):
    def get(self, request):
        scenarios = ProductionData.objects.all().order_by('-date', '-id')
        # Сериализуем через ваш ProductionDataSerializer
        serializer = ProductionDataSerializer(scenarios, many=True)
        return Response(serializer.data)
class ExportScenariosCSVView(APIView):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="kpi_scenarios.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Дата', 'Руда(т)', 'План.время(ч)', 'Простой(ч)',
                         'Численность', 'Топливо(л)', 'КИО(%)', 'Произв.(т/ч-чел)',
                         'Уд.расход(л/т)', 'Темп(т/ч)'])

        for scenario in ProductionData.objects.all().order_by('-date'):
            # Вычисляем KPI для каждого сохранённого сценария
            calc = MiningKPICalculator(scenario)
            kpis = calc.calculate_all_kpis()
            writer.writerow([
                scenario.id, scenario.date, scenario.ore_volume,
                scenario.operating_time, scenario.downtime, scenario.crew_size,
                scenario.fuel_consumption,
                kpis['equipment_utilization_rate'],
                kpis['labor_productivity'],
                kpis['fuel_efficiency'],
                kpis['actual_production_rate']
            ])
        return response

class ScenarioDetailView(APIView):
    def get(self, request, pk):
        try:
            scenario = ProductionData.objects.get(pk=pk)
        except ProductionData.DoesNotExist:
            return Response({'error': 'Сценарий не найден'}, status=404)
        data = {
            'id': scenario.id,
            'ore_volume': scenario.ore_volume,
            'operating_time': scenario.operating_time,
            'downtime': scenario.downtime,
            'crew_size': scenario.crew_size,
            'fuel_consumption': scenario.fuel_consumption,
        }
        return Response(data)