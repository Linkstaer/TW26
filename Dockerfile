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

# Create emergency admin
WORKDIR /app/site_twilight
RUN python manage.py ensure_admin

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE $PORT
CMD python manage.py migrate --noinput && \
    gunicorn site_twilight.wsgi:application --bind 0.0.0.0:$PORT