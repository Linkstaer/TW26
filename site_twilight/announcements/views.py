from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import Announcement, AnnouncementView, EventLog, LoreSuggestion


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


def _user_can_publish_announcements(user) -> bool:
    """Publicadores autorizados (spec §5.1): Site Director, líderes de facción, admins."""
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    # Líderes de facción
    if user.led_factions.exists():
        return True
    card = user.get_highest_access_card()
    return bool(card and card.can_edit_any)


@login_required
def announcement_create(request):
    """Crear un anuncio In-RP / Off-RP (spec §5.1)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not _user_can_publish_announcements(request.user):
        return JsonResponse({"error": "Sin permisos para publicar anuncios"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return JsonResponse({"error": "Título y contenido requeridos"}, status=400)

    ann_type = data.get("announcement_type", Announcement.AnnouncementType.OFF_RP)
    if ann_type not in (
        Announcement.AnnouncementType.IN_RP,
        Announcement.AnnouncementType.OFF_RP,
        Announcement.AnnouncementType.CRITICAL,
    ):
        return JsonResponse({"error": "Tipo de anuncio inválido"}, status=400)

    # Solo admins pueden publicar críticos
    if ann_type == Announcement.AnnouncementType.CRITICAL and not (
        request.user.is_superuser or request.user.is_staff
    ):
        return JsonResponse({"error": "Solo administración publica eventos críticos"}, status=403)

    min_level = (data.get("min_access_level") or "L1").upper()
    if min_level not in ("L1", "L2", "L3", "L4", "L5", "L6"):
        return JsonResponse({"error": "Nivel inválido"}, status=400)

    faction = None
    faction_id = data.get("faction_id")
    if faction_id:
        from factions.models import Faction

        faction = Faction.objects.filter(id=faction_id).first()
        if faction is None:
            return JsonResponse({"error": "Facción no encontrada"}, status=404)
        # Un líder solo publica anuncios de sus propias facciones
        if not (
            request.user.is_superuser
            or request.user.is_staff
            or faction.leaders.filter(id=request.user.id).exists()
        ):
            return JsonResponse(
                {"error": "Solo los líderes publican anuncios de su facción"}, status=403
            )

    ann = Announcement.objects.create(
        title=title,
        content=content,
        announcement_type=ann_type,
        min_access_level=min_level,
        faction=faction,
        author=request.user,
        is_pinned=bool(data.get("is_pinned"))
        and (request.user.is_superuser or request.user.is_staff),
    )

    return JsonResponse({"success": True, "id": ann.id})


# ===== Sugerencias de Lore (Boosters) =====


@login_required
def lore_suggestion_create(request):
    """Los Boosters envían sugerencias de lore (spec, sección final)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not (request.user.is_booster or request.user.is_superuser):
        return JsonResponse(
            {"error": "Solo los Boosters pueden enviar sugerencias de lore"}, status=403
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return JsonResponse({"error": "Título y contenido requeridos"}, status=400)

    suggestion = LoreSuggestion.objects.create(
        author=request.user, title=title, content=content
    )

    return JsonResponse({"success": True, "id": suggestion.id})


@login_required
def lore_suggestion_list(request):
    """Mis sugerencias; el staff ve todas."""
    is_reviewer = request.user.is_superuser or request.user.is_staff

    suggestions = (
        LoreSuggestion.objects.select_related("author", "reviewed_by")
        if is_reviewer
        else LoreSuggestion.objects.filter(author=request.user).select_related(
            "author", "reviewed_by"
        )
    )

    return JsonResponse(
        {
            "is_reviewer": is_reviewer,
            "is_booster": request.user.is_booster or request.user.is_superuser,
            "suggestions": [
                {
                    "id": sg.id,
                    "title": sg.title,
                    "content": sg.content,
                    "status": sg.status,
                    "author": sg.author.roblox_username,
                    "review_notes": sg.review_notes,
                    "reviewed_by": sg.reviewed_by.roblox_username
                    if sg.reviewed_by
                    else None,
                    "created_at": sg.created_at.isoformat(),
                }
                for sg in suggestions[:100]
            ],
        }
    )


@login_required
def lore_suggestion_review(request, suggestion_id):
    """El staff aprueba o rechaza una sugerencia."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({"error": "Sin permisos"}, status=403)

    try:
        suggestion = LoreSuggestion.objects.get(id=suggestion_id)
    except LoreSuggestion.DoesNotExist:
        return JsonResponse({"error": "Sugerencia no encontrada"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    action = data.get("action")
    if action not in ("approve", "reject"):
        return JsonResponse({"error": "Acción inválida"}, status=400)

    suggestion.status = (
        LoreSuggestion.Status.APPROVED
        if action == "approve"
        else LoreSuggestion.Status.REJECTED
    )
    suggestion.reviewed_by = request.user
    suggestion.review_notes = data.get("notes", "")
    suggestion.reviewed_at = timezone.now()
    suggestion.save()

    return JsonResponse({"success": True, "status": suggestion.status})
