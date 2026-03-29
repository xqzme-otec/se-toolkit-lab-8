FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости напрямую
RUN pip install --no-cache-dir \
    fastapi>=0.100.0 \
    uvicorn>=0.23.0 \
    sqlmodel>=0.0.14 \
    asyncpg>=0.29.0 \
    pydantic-settings>=2.0.0 \
    opentelemetry-api>=1.20.0 \
    opentelemetry-sdk>=1.20.0 \
    opentelemetry-exporter-otlp>=1.20.0

# Копируем код
COPY backend/src /app/src

# Настраиваем PYTHONPATH для импортов
ENV PYTHONPATH=/app/src

# Запускаем приложение
CMD ["uvicorn", "lms_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
