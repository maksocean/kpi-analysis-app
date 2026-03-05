from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), # Главная страница с симулятором
    path('api/calculate/', views.CalculateKPIView.as_view(), name='calculate_kpi'),
]