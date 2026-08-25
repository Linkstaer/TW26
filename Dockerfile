FROM node:20-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app

# Sin esto, la salida de Python queda bufferada y los logs de arranque
# no aparecen en Railway hasta que el proceso termina.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy frontend build
COPY --from=frontend /app/frontend/dist /app/frontend/dist

# Install Python dependencies
COPY site_twilight/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy application - copy everything including site_twilight folder
COPY . .

WORKDIR /app/site_twilight

# Collect static files (no requiere base de datos)
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

EXPOSE 8080

# El arranque vive en start.sh (ver logs de cada fase). railway.json ya no
# define startCommand: este CMD es la unica fuente de verdad.
CMD ["sh", "/app/start.sh"]
