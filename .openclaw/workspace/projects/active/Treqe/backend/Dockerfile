FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear estructura de directorios
RUN mkdir -p /app/src /app/logs /app/tests

# Copiar código fuente
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY alembic.ini /app/
COPY .env.example /app/.env

# Crear usuario no-root
RUN useradd -m -u 1000 treqe && chown -R treqe:treqe /app
USER treqe

# Variables de entorno por defecto
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Puerto de la aplicación
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]