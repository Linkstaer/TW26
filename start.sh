#!/bin/sh
# Arranque del contenedor. Cada fase se loguea para que un fallo se vea en
# los Deploy Logs de Railway en vez de terminar en un 502 mudo.
set -u

cd /app/site_twilight

echo "[boot] 1/3 migrate"
python manage.py migrate --noinput || {
    echo "[boot] FATAL: migrate fallo, abortando"
    exit 1
}

# No debe poder bloquear el arranque: si tarda o falla, se sigue igual.
echo "[boot] 2/3 ensure_admin"
timeout 30 python manage.py ensure_admin
STATUS=$?
if [ $STATUS -eq 124 ]; then
    echo "[boot] WARN: ensure_admin excedio 30s, continuando sin el"
elif [ $STATUS -ne 0 ]; then
    echo "[boot] WARN: ensure_admin fallo (exit $STATUS), continuando"
fi

echo "[boot] 3/3 gunicorn en 0.0.0.0:${PORT:-8080}"
# worker-class gthread: /api/events/ es un stream SSE que dura horas. Un worker
# sync atiende una request por vez y el arbitro lo mata al superar --timeout, que
# es lo que provocaba un WORKER TIMEOUT cada 2 minutos. Con hilos, el latido del
# worker corre aparte y no depende de cuanto dure cada request.
exec gunicorn site_twilight.wsgi:application \
    --bind "0.0.0.0:${PORT:-8080}" \
    --worker-class gthread \
    --workers "${WEB_CONCURRENCY:-2}" \
    --threads "${WEB_THREADS:-25}" \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
