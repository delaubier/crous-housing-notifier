FROM python:3.12-slim

# Empêche la mise en cache de stdout/stderr par Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DATA_DIR=/app/data

WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application
COPY crous_api.py notifier.py bot.py ./

# Répertoire de données persistantes
RUN mkdir -p /app/data

CMD ["python", "bot.py"]
