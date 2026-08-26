"""
Bus de eventos para el stream SSE (/api/events/).

El emisor original guardaba los clientes en una lista en memoria del proceso,
asi que un emit() en el worker A no llegaba jamas a los clientes conectados al
worker B: con --workers 2 el push funcionaba solo por casualidad. Aca cada
worker publica en un canal de Redis y todos reparten a sus propios clientes
locales, con lo que el evento llega a todo el mundo sin importar que worker lo
origino.

Sin REDIS_URL definida (desarrollo con un solo proceso) el bus cae a reparto en
memoria. No es un error: es el comportamiento anterior, que alcanza cuando hay
un unico worker.
"""

import json
import logging
import threading
import time
from queue import Empty, Full, Queue

from django.conf import settings

logger = logging.getLogger(__name__)

CHANNEL = "site_twilight:sse"

# Cuanto espera un cliente antes de mandar un comentario de keepalive. Tiene que
# quedar por debajo de cualquier timeout de proxy intermedio para que la
# conexion no se considere muerta.
KEEPALIVE_SECONDS = 30

# Un cliente que no consume no puede crecer sin limite ni frenar al resto: al
# llenarse la cola se descartan los eventos nuevos.
QUEUE_MAXSIZE = 50


class Subscriber:
    """Un cliente SSE conectado a este proceso."""

    __slots__ = ("queue", "user_id")

    def __init__(self, user_id):
        self.queue = Queue(maxsize=QUEUE_MAXSIZE)
        self.user_id = user_id


class EventBus:
    def __init__(self):
        self._subscribers = []
        self._lock = threading.Lock()
        self._redis = None
        self._redis_failed = False
        self._listener_started = False

    # -- API publica ------------------------------------------------------

    def subscribe(self, user_id):
        subscriber = Subscriber(user_id)
        with self._lock:
            self._subscribers.append(subscriber)
        self._ensure_listener()
        return subscriber

    def unsubscribe(self, subscriber):
        with self._lock:
            if subscriber in self._subscribers:
                self._subscribers.remove(subscriber)

    def publish(self, event_type, data, user_id=None):
        """Emite un evento. Con user_id, solo lo recibe ese usuario."""
        payload = {"type": event_type, "data": data, "user_id": user_id}
        client = self._connect()

        if client is None:
            self._dispatch(payload)
            return

        try:
            # Redis nos devuelve el mensaje por nuestra propia suscripcion, asi
            # que no hay que repartirlo local tambien o llegaria duplicado.
            client.publish(CHANNEL, json.dumps(payload))
        except Exception:
            logger.warning(
                "SSE: fallo el publish a Redis, se reparte solo local", exc_info=True
            )
            self._dispatch(payload)

    # -- interno ----------------------------------------------------------

    def _dispatch(self, payload):
        target = payload.get("user_id")
        with self._lock:
            subscribers = list(self._subscribers)

        for subscriber in subscribers:
            if target is not None and subscriber.user_id != target:
                continue
            try:
                subscriber.queue.put_nowait(payload)
            except Full:
                logger.warning(
                    "SSE: cola llena para el usuario %s, evento descartado",
                    subscriber.user_id,
                )

    def _connect(self):
        """Conexion perezosa para publicar. None si no hay Redis configurada."""
        if self._redis is not None:
            return self._redis
        if self._redis_failed or not getattr(settings, "REDIS_URL", None):
            return None

        try:
            import redis

            client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_keepalive=True,
                health_check_interval=30,
            )
            client.ping()
        except Exception:
            # Que Redis no este no puede tumbar el sitio: se degrada a reparto
            # local y se sigue sirviendo.
            logger.warning(
                "SSE: no se pudo conectar a Redis, eventos solo locales",
                exc_info=True,
            )
            self._redis_failed = True
            return None

        self._redis = client
        return self._redis

    def _ensure_listener(self):
        """Arranca el hilo que escucha el canal. Uno solo por proceso."""
        with self._lock:
            if self._listener_started:
                return
            if not getattr(settings, "REDIS_URL", None):
                return
            self._listener_started = True

        threading.Thread(
            target=self._listen, name="sse-redis-listener", daemon=True
        ).start()

    def _listen(self):
        import redis

        while True:
            try:
                client = redis.Redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    socket_keepalive=True,
                    health_check_interval=30,
                )
                pubsub = client.pubsub(ignore_subscribe_messages=True)
                pubsub.subscribe(CHANNEL)
                logger.info("SSE: escuchando %s", CHANNEL)

                for message in pubsub.listen():
                    if message.get("type") != "message":
                        continue
                    try:
                        self._dispatch(json.loads(message["data"]))
                    except (TypeError, ValueError):
                        logger.warning("SSE: mensaje ilegible en %s", CHANNEL)
            except Exception:
                logger.warning(
                    "SSE: listener de Redis caido, reintento en 5s", exc_info=True
                )
                time.sleep(5)


event_bus = EventBus()


def emit_ssu_status_change(new_status):
    """El SSU cambio de estado: lo ve todo el mundo."""
    event_bus.publish("ssu_status", {"active": new_status})


def emit_notification_count(user_id, count):
    """Contador de notificaciones sin leer, solo para el usuario afectado."""
    event_bus.publish("notification_count", {"count": count}, user_id=user_id)
