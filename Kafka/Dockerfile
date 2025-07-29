# Imagen base mínima con Python 3.10
FROM python:3.10-slim

# Establecer variables de entorno para evitar problemas con buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo primero los requirements para aprovechar cache
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY ./app .

# Exponer puertos (si decides usar networking externo con Kafka o ES)
EXPOSE 9092
EXPOSE 9200

# Comando por defecto (puede ser modificado al construir o ejecutar)
CMD ["python", "main.py"]
