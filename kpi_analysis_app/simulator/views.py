from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import KPICalculatorInputSerializer
from .services import MiningKPICalculator
from .models import ProductionData

def dashboard_view(request):
    return render(request, 'simulator/dashboard.html')

class CalculateKPIView(APIView):
    """
    Эндпоинт для расчёта KPI на основе переданных параметров.
    Принимает POST-запрос с JSON.
    """
    def post(self, request):
        serializer = KPICalculatorInputSerializer(data=request.data)
        if serializer.is_valid():
            # 1. Создаём временный объект модели из валидированных данных
            calc_data = ProductionData(**serializer.validated_data)
            # 2. Передаём его в калькулятор
            calculator = MiningKPICalculator(calc_data)
            # 3. Получаем результат
            kpis = calculator.calculate_all_kpis()
            # 4. Можно сохранить сценарий в БД (опционально)
            # ProductionData.objects.create(**serializer.validated_data)
            return Response(kpis, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Дополнительно: View для работы с историей (получение, сохранение)
