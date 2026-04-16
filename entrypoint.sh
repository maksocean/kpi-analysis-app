#!/bin/sh
python /app/kpi_analysis_app/manage.py migrate
python /app/kpi_analysis_app/manage.py runserver 0.0.0.0:8000