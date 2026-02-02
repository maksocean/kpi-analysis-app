# Базовый образ Python
FROM python:3.13

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app/kpi_analysis_appп

# Копируем файл зависимостей внутрь образа
COPY requirements.txt .

# Устанавливаем Python-зависимости приложения
RUN pip install --no-cache-dir -r requirements.txt

# Делаем логи Python мгновенными
ENV PYTHONUNBUFFERED=1

# Копируем весь проект (исходники приложения)
COPY . .

# Открываем порт (если веб-приложение)
EXPOSE 8000

# Создаём непривилегированного пользователя и переключаемся на него
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Запуск команды для миграции базы данных и старта сервера разработки
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]