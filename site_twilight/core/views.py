from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import SiteState
from .api.auth.user import get_current_user_service
import json
import time
import threading
from queue import Queue

# Create your views here.


def api_get_ssu_status(request):
    return JsonResponse({"ssu_status": SiteState.get().ssu_status})


def api_get_current_user(request):
    data = get_current_user_service(request.user)
    return JsonResponse(data)


class EventEmitter:
    """Simple event emitter for SSE"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._clients = []
        return cls._instance

    def add_client(self, client):
        with self._lock:
            self._clients.append(client)

    def remove_client(self, client):
        with self._lock:
            if client in self._clients:
                self._clients.remove(client)

    def emit(self, event_type, data):
        with self._lock:
            clients = self._clients.copy()
        for client in clients:
            try:
                client.put_nowait({"type": event_type, "data": data})
            except:
                pass


# Global event emitter instance
event_emitter = EventEmitter()


def sse_events(request):
    """Server-Sent Events endpoint for real-time updates"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    from announcements.models import Notification

    # Create a queue for this client
    client_queue = Queue(maxsize=10)
    event_emitter.add_client(client_queue)

    def event_stream():
        try:
            # Send initial data
            yield f"event: connected\ndata: {json.dumps({'status': 'connected'})}\n\n"

            # Send initial notification count
            try:
                notification_count = Notification.objects.filter(
                    user=request.user, is_read=False
                ).count()
                yield f"event: notification_count\ndata: {json.dumps({'count': notification_count})}\n\n"
            except:
                pass

            # Send initial SSU status
            try:
                ssu_status = SiteState.get().ssu_status
                yield f"event: ssu_status\ndata: {json.dumps({'active': ssu_status})}\n\n"
            except:
                pass

            # Keep connection open and stream events
            while True:
                try:
                    event = client_queue.get(timeout=30)
                    yield f"event: {event['type']}\ndata: {json.dumps(event['data'])}\n\n"
                except:
                    # Send keepalive
                    yield f": keepalive\n\n"
        except GeneratorExit:
            pass
        finally:
            event_emitter.remove_client(client_queue)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


def emit_ssu_status_change(new_status):
    """Call this function when SSU status changes"""
    event_emitter.emit("ssu_status", {"active": new_status})


def emit_notification(user_id, count):
    """Call this function when a user receives a new notification"""
    event_emitter.emit("notification", {"count": count, "user_id": user_id})
