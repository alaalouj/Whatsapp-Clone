FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système nécessaires pour psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip
RUN pip install --upgrade pip

# Copier les dépendances et les installer
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY ./app /app/app

# Définir PYTHONPATH pour inclure /app
ENV PYTHONPATH=/app

# Exposer le port 8000
EXPOSE 8000

# Démarrer l'application avec le bon chemin de module
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
