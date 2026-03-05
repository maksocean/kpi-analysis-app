from rest_framework import serializers
from .models import ProductionData

class ProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionData
        fields = '__all__'  # Или выберите конкретные поля для ввода

class KPICalculatorInputSerializer(serializers.Serializer):
    """Сериализатор для входных данных симулятора (можно не привязывать к модели)."""
    ore_volume = serializers.FloatField(min_value=0)
    operating_time = serializers.FloatField(min_value=0)
    downtime = serializers.FloatField(min_value=0)
    crew_size = serializers.IntegerField(min_value=1)
    fuel_consumption = serializers.FloatField(min_value=0)