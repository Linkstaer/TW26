import json
import logging
from queue import Empty

from django.db import connection
from django.http import JsonResponse, StreamingHttpResponse

from .events import KEEPALIVE_SECONDS, event_bus
from .models import SiteState
from .api.auth.user import get_current_user_service

logger = logging.getLogger(__name__)


def api_get_ssu_status(request):
    return JsonResponse({"ssu_status": SiteState.get().ssu_status})


def api_get_current_user(request):
    data = get_current_user_service(request.user)
    return JsonResponse(data)


def _frame(event_type, data):
    """Un evento con el formato de linea que exige text/event-stream."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


def sse_events(request):
    """Server-Sent Events endpoint for real-time updates"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    from announcements.models import Notification

    user_id = request.user.id
    subscriber = event_bus.subscribe(user_id)

    def event_stream():
        try:
            yield _frame("connected", {"status": "connected"})

            try:
                unread = Notification.objects.filter(
                    user_id=user_id, is_read=False
                ).count()
                yield _frame("notification_count", {"count": unread})
            except Exception:
                logger.warning(
                    "SSE: no se pudo leer el contador inicial", exc_info=True
                )

            try:
                yield _frame("ssu_status", {"active": SiteState.get().ssu_status})
            except Exception:
                logger.warning("SSE: no se pudo leer el estado SSU inicial", exc_info=True)

            # De aca en adelante el stream no toca la base. Si no soltamos la
            # conexion, cada cliente conectado se queda con una de Postgres
            # ocupada durante horas y se agota el pool del servidor.
            connection.close()

            while True:
                try:
                    event = subscriber.queue.get(timeout=KEEPALIVE_SECONDS)
                except Empty:
                    # Sin eventos: mandamos un comentario para que el proxy y el
                    # navegador no den la conexion por muerta.
                    yield ": keepalive\n\n"
                    continue

                yield _frame(event["type"], event["data"])
        finally:
            event_bus.unsubscribe(subscriber)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
