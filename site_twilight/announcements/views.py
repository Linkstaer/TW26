from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import Announcement, AnnouncementView, EventLog


def announcement_list(request):
    """Lista de anuncios visibles para el usuario"""
    user = request.user

    announcements = Announcement.objects.filter(is_published=True).select_related(
        "author", "faction"
    )

    announcements_data = []
    for ann in announcements:
        if ann.can_user_view(user):
            announcements_data.append(
                {
                    "id": ann.id,
                    "title": ann.title,
                    "announcement_type": ann.announcement_type,
                    "min_access_level": ann.min_access_level,
                    "author": ann.author.roblox_username if ann.author else None,
                    "is_pinned": ann.is_pinned,
                    "views": ann.views,
                    "created_at": ann.created_at.isoformat()
                    if ann.created_at
                    else None,
                }
            )

    return JsonResponse({"announcements": announcements_data}, safe=False)


def announcement_detail(request, announcement_id):
    """Detalles de un anuncio"""
    user = request.user

    try:
        ann = Announcement.objects.get(id=announcement_id, is_published=True)
    except Announcement.DoesNotExist:
        return JsonResponse({"error": "Anuncio no encontrado"}, status=404)

    if not ann.can_user_view(user):
        return JsonResponse({"error": "Acceso denegado"}, status=403)

    return JsonResponse(
        {
            "id": ann.id,
            "title": ann.title,
            "content": ann.content,
            "announcement_type": ann.announcement_type,
            "min_access_level": ann.min_access_level,
            "author": ann.author.roblox_username if ann.author else None,
            "is_pinned": ann.is_pinned,
            "views": ann.views,
            "created_at": ann.created_at.isoformat() if ann.created_at else None,
            "updated_at": ann.updated_at.isoformat() if ann.updated_at else None,
        }
    )


@login_required
def view_announcement(request, announcement_id):
    """Registrar que el usuario vio el anuncio"""
    try:
        ann = Announcement.objects.get(id=announcement_id, is_published=True)
    except Announcement.DoesNotExist:
        return JsonResponse({"error": "Anuncio no encontrado"}, status=404)

    if not ann.can_user_view(request.user):
        return JsonResponse({"error": "Acceso denegado"}, status=403)

    # Registrar vista
    view, created = AnnouncementView.objects.get_or_create(
        announcement=ann, user=request.user
    )

    if created or view:
        ann.views += 1
        ann.save(update_fields=["views"])

    return JsonResponse({"success": True})


def event_list(request):
    """Lista de eventos del sistema"""
    user = request.user

    events = EventLog.objects.all()[:50]

    events_data = []
    for event in events:
        # Verificar nivel de acceso
        level_priority = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6}
        user_level = (
            max([level_priority.get(l, 0) for l in user.get_accessible_levels()])
            if user.is_authenticated
            else 1
        )
        required_level = level_priority.get(event.min_access_level, 1)

        if user_level < required_level:
            continue

        events_data.append(
            {
                "id": event.id,
                "event_type": event.event_type,
                "title": event.title,
                "description": event.description,
                "min_access_level": event.min_access_level,
                "created_at": event.created_at.isoformat()
                if event.created_at
                else None,
            }
        )

    return JsonResponse({"events": events_data}, safe=False)
