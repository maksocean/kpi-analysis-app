# KPI Analysis App

Django-приложение для расчёта и визуализации ключевых показателей эффективности (KPI) в горнодобывающей отрасли.

## Содержание
- [О приложении](#о-приложении)
- [Архитектура системы](#архитектура-системы)
  - [Диаграмма C4](#диаграмма-c4)
  - [Диаграмма последовательности (процесс расчёта KPI)](#диаграмма-последовательности-процесс-расчёта-kpi)
- [Как запустить приложение](#как-запустить-приложение)
- [Стек технологий](#стек-технологий)

## О приложении

Приложение позволяет горному инженеру (аналитику) изменять входные параметры (объём добычи, время простоев, численность бригады, расход топлива) и мгновенно видеть пересчитанные KPI: коэффициент использования оборудования, производительность труда, удельный расход топлива, фактический темп добычи. Все расчёты выполняются на бэкенде, а графики обновляются без перезагрузки страницы.

## Архитектура системы

### Диаграмма C4
На диаграмме ниже показаны основные контейнеры приложения и их взаимодействие.

```mermaid
C4Container
title Container diagram for KPI Analysis App

Person(analyst, "Аналитик", "Специалист, ответственный за анализ и планирование производственных показателей")

System_Boundary(app, "KPI Analysis App") {
    Container(browser, "Браузер пользователя", "Веб-интерфейс (JavaScript, Chart.js)", "Отображает панель управления (слайдеры) и дашборд с графиками. Отправляет сценарные параметры на бэкенд и получает обновлённые KPI.")
    Container(backend, "Бэкенд-приложение", "Python/Django, DRF", "Принимает параметры через API, содержит ядро расчётов (MiningKPICalculator), управляет данными и формирует ответ для фронтенда.")
    ContainerDb(db, "База данных PostgreSQL", "PostgreSQL", "Хранит исторические данные, эталонные значения и сохраненные сценарии.")
}

Rel(analyst, browser, "Использует приложение")

BiRel(browser, backend, "Обмен сценарными параметрами и рассчитанными KPI (JSON/HTTPS)")
BiRel(backend, db, "Запрос/сохранение эталонных данных и сценариев (SQL)")
```

### Диаграмма последовательности (процесс расчёта KPI)

```mermaid
sequenceDiagram
    participant Browser
    participant DjangoView as Django View
    participant Serializer as KPICalculatorInputSerializer
    participant Calculator as MiningKPICalculator

    Note over Browser: Пользователь меняет поля и нажимает кнопку
    
    Browser->>DjangoView: POST /api/calculate/
    activate DjangoView

    DjangoView->>Serializer: is_valid()
    activate Serializer
    Serializer-->>DjangoView: validation result
    deactivate Serializer

    alt Данные валидны
        DjangoView->>Calculator: создать экземпляр
        activate Calculator
        DjangoView->>Calculator: calculate_all_kpis()
        activate Calculator
        Calculator-->>DjangoView: словарь KPI
        deactivate Calculator
        deactivate Calculator

        DjangoView-->>Browser: 200 OK (JSON)
    else Ошибка валидации
        DjangoView-->>Browser: 400 Bad Request

    end
    deactivate DjangoView

    Browser->>Chart: updateCharts(kpiData)
    activate Chart
    Chart-->>Browser: график обновлён
    deactivate Chart
```

## Как запустить приложение
**Требования**: Docker и Docker Compose (или Docker Desktop).

1. Склонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://gitverse.ru/ваш-логин/kpi-analysis-app.git
   cd kpi-analysis-app
   ```
2. Скопируйте `.env.example` в `.env` (при необходимости отредактируйте переменные).  

3. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
4. Откройте в браузере: http://localhost:8000/simulator/


>  **Примечание:** При первом запуске может потребоваться несколько минут на загрузку Docker-образов. После успешного запуска приложение будет доступно по указанному адресу.

## Стек технологий
- Python 3.13 / Django 4.x
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- Chart.js (фронтенд)