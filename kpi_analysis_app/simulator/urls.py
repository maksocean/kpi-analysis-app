from django.urls import path
from . import views

urlpatterns = [
    # Главная html-страница с симулятором
    path('', views.dashboard_view, name='dashboard'),

    #path('simulator/', views.dashboard_view),

    # API эндпоинты (их вызывают тесты)
    path('api/calculate/', views.CalculateKPIView.as_view(), name='calculate_kpi'),
    path('api/scenarios/', views.ListScenariosView.as_view(), name='scenarios'),
    path('api/export-csv/', views.ExportScenariosCSVView.as_view(), name='export_csv'),
    path('api/scenarios/<int:pk>/', views.ScenarioDetailView.as_view(), name='scenario_detail'),
    path('api/calculate-preview/', views.CalculatePreviewView.as_view(), name='calculate_preview'),
]