"""
Eventos automáticos del feed (spec §5.1):
- Nuevos SCP
- Nuevos documentos
- Creación / disolución de facciones

Cada evento genera un EventLog y un anuncio automático filtrado por nivel.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Announcement, EventLog


def _auto_announce(title, content, min_level="L1", related_scp=None):
    Announcement.objects.create(
        title=title,
        content=content,
        announcement_type=Announcement.AnnouncementType.AUTOMATIC,
        min_access_level=min_level,
        related_scp=related_scp,
    )


@receiver(post_save, sender="scps.SCP")
def on_scp_created(sender, instance, created, **kwargs):
    if not created:
        return
    EventLog.objects.create(
        event_type=EventLog.EventType.SCP_CREATED,
        scp=instance,
        title=f"Nuevo archivo: {instance.scp_id}",
        description=f"Se ha registrado el archivo {instance.scp_id} - {instance.title}.",
        min_access_level="L1",
    )
    _auto_announce(
        f"Nuevo archivo SCP: {instance.scp_id}",
        f"El archivo {instance.scp_id} ({instance.title}) ha sido incorporado a la base de datos.",
        related_scp=instance,
    )


@receiver(post_save, sender="scps.Document")
def on_document_created(sender, instance, created, **kwargs):
    if not created:
        return
    EventLog.objects.create(
        event_type=EventLog.EventType.DOCUMENT_CREATED,
        document=instance,
        title=f"Nuevo documento: {instance.title}",
        description=f"Se ha publicado el documento «{instance.title}».",
        min_access_level=instance.min_access_level,
    )
    _auto_announce(
        f"Nuevo documento: {instance.title}",
        f"El documento «{instance.title}» está disponible en la sección Documentación.",
        min_level=instance.min_access_level,
    )


@receiver(pre_save, sender="factions.Faction")
def on_faction_status_change(sender, instance, **kwargs):
    """Detecta disolución de facciones comparando contra el estado previo."""
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    from factions.models import Faction

    if (
        previous.status != instance.status
        and instance.status == Faction.Status.DISSOLVED
    ):
        visible_name = instance.facade_name if instance.is_classified else instance.display_name
        EventLog.objects.create(
            event_type=EventLog.EventType.FACTION_DISSOLVED,
            faction=instance,
            title=f"Facción disuelta: {visible_name}",
            description=f"La facción {visible_name} ha sido disuelta.",
            min_access_level="L1",
        )
        _auto_announce(
            f"Facción disuelta: {visible_name}",
            f"La facción {visible_name} ha cesado sus operaciones.",
        )


@receiver(post_save, sender="factions.Faction")
def on_faction_created(sender, instance, created, **kwargs):
    if not created:
        return
    # Facciones clasificadas no se anuncian con su nombre real (spec §2.1)
    visible_name = instance.facade_name if instance.is_classified else instance.display_name
    EventLog.objects.create(
        event_type=EventLog.EventType.FACTION_CREATED,
        faction=instance,
        title=f"Nueva facción: {visible_name}",
        description=f"La facción {visible_name} ha sido establecida.",
        min_access_level="L1",
    )
    _auto_announce(
        f"Nueva facción: {visible_name}",
        f"La facción {visible_name} ha sido establecida en el sitio.",
    )


@receiver(post_save, sender="announcements.Notification")
def on_notification_created(sender, instance, created, **kwargs):
    """Empuja el contador de no leidas por SSE al usuario que la recibio."""
    if not created:
        return

    from django.db import transaction

    from core.events import emit_notification_count

    user_id = instance.user_id

    def push():
        # Las notificaciones se crean dentro de transacciones (factions/views.py):
        # contar antes del commit mandaria un numero que puede no existir nunca.
        unread = sender.objects.filter(user_id=user_id, is_read=False).count()
        emit_notification_count(user_id, unread)

    transaction.on_commit(push)
