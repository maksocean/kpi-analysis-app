from django.test import TestCase
from rest_framework.test import APIClient
from .models import ProductionData
from .services import MiningKPICalculator


class KPICalculatorTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            'ore_volume': 1000,
            'operating_time': 24,
            'downtime': 2,
            'crew_size': 15,
            'fuel_consumption': 500
        }

    def test_kpi_calculation(self):
        response = self.client.post('/simulator/api/calculate/', self.valid_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['kpis']['equipment_utilization_rate'], 91.67)
        self.assertEqual(response.data['kpis']['labor_productivity'], 3.03)

    def test_invalid_downtime(self):
        invalid = self.valid_data.copy()
        invalid['downtime'] = 25  # больше operating_time
        response = self.client.post('/simulator/api/calculate/', invalid, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Время простоя не может быть больше', str(response.data))

    def test_save_to_db(self):
        response = self.client.post('/simulator/api/calculate/', self.valid_data, format='json')
        self.assertEqual(ProductionData.objects.count(), 1)
        saved = ProductionData.objects.first()
        self.assertEqual(saved.ore_volume, 1000)

    def test_export_csv(self):
        # Сначала сохраняем хотя бы один сценарий
        ProductionData.objects.create(**self.valid_data)
        response = self.client.get('/simulator/api/export-csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')