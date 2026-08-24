FROM node:20-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app

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

EXPOSE $PORT
# migrate + ensure_admin corren en runtime: en build no hay base de datos
CMD python manage.py migrate --noinput && (python manage.py ensure_admin || echo '[warn] ensure_admin fallo, continuando') && echo "[boot] iniciando gunicorn en 0.0.0.0:${PORT:-8000}" && gunicorn site_twilight.wsgi:application --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile - --log-level info
