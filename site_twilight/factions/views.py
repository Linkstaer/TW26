from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from .models import (
    LEVEL_ORDER,
    Faction,
    FactionRank,
    CharacterFactionMembership,
    FactionApplication,
    FactionLog,
    AccessCard,
    FactionInvitation,
    FactionDivision,
    FactionType,
)
from announcements.models import Notification


DEFAULT_FACTION_TYPES = [
    {"key": "department", "display_name": "Departamento", "color": "#3498db"},
    {"key": "council", "display_name": "Consejo", "color": "#9b59b6"},
    {"key": "special_force", "display_name": "Fuerza Especial", "color": "#e74c3c"},
    {"key": "classified", "display_name": "Clasificada", "color": "#2c3e50"},
    {"key": "mtf", "display_name": "MTF", "color": "#aa2222"},
    {"key": "research", "display_name": "Research", "color": "#27ae60"},
    {"key": "security", "display_name": "Security", "color": "#f39c12"},
    {"key": "admin", "display_name": "Admin", "color": "#e91e63"},
    {"key": "ethics", "display_name": "Ethics", "color": "#00bcd4"},
    {"key": "other", "display_name": "Other", "color": "#95a5a6"},
]


@csrf_exempt
def faction_types_list(request):
    """Lista de tipos de facción (default + personalizados)"""
    if request.method == "GET":
        # Combinar tipos por defecto con tipos personalizados
        custom_types = FactionType.objects.filter(is_active=True)
        types_data = []

        # Agregar tipos por defecto
        for t in DEFAULT_FACTION_TYPES:
            types_data.append(
                {
                    "key": t["key"],
                    "display_name": t["display_name"],
                    "color": t["color"],
                    "is_default": True,
                }
            )

        # Agregar tipos personalizados
        for t in custom_types:
            types_data.append(
                {
                    "key": t.key,
                    "display_name": t.display_name,
                    "color": t.color,
                    "is_default": False,
                    "id": t.id,
                }
            )

        return JsonResponse({"types": types_data}, safe=False)

    elif request.method == "POST":
        if not request.user.is_authenticated or not request.user.is_superuser:
            return JsonResponse({"error": "Solo admins"}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

        key = data.get("key", "").lower().strip()
        display_name = data.get("display_name", "").strip()
        color = data.get("color", "#aa2222")

        if not key or not display_name:
            return JsonResponse(
                {"error": "Key y display_name son requeridos"}, status=400
            )

        # Verificar que no exista ya
        if any(t["key"] == key for t in DEFAULT_FACTION_TYPES):
            return JsonResponse(
                {"error": "Ya existe un tipo por defecto con esa key"}, status=400
            )

        if FactionType.objects.filter(key=key).exists():
            return JsonResponse({"error": "Ya existe un tipo con esa key"}, status=400)

        faction_type = FactionType.objects.create(
            key=key,
            display_name=display_name,
            color=color,
            description=data.get("description", ""),
        )

        return JsonResponse(
            {
                "id": faction_type.id,
                "key": faction_type.key,
                "display_name": faction_type.display_name,
                "color": faction_type.color,
                "is_default": False,
            }
        )

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def faction_list(request):
    """Lista de facciones públicas visibles para el usuario"""
    user = request.user

    # Solo facciones públicas
    factions = Faction.objects.filter(status=Faction.Status.ACTIVE, is_public=True)

    # Las fachadas deben ser indistinguibles para usuarios sin L5+ (spec §2.1):
    # solo quienes ven el nombre real ven también la marca de clasificada.
    can_see_classified = False
    if user.is_authenticated:
        if user.is_superuser:
            can_see_classified = True
        else:
            card = user.get_highest_access_card()
            can_see_classified = bool(card and card.level in ["L5", "L6"])

    visible_factions = []
    for faction in factions:
        visible_factions.append(
            {
                "id": faction.id,
                "name": faction.get_visible_name(user),
                "type": faction.faction_type,
                "is_classified": faction.is_classified and can_see_classified,
                "allow_applications": faction.allow_applications,
                "description": faction.description,
                "icon": faction.icon,
                "color": faction.color,
                "has_divisions": faction.divisions.exists(),
            }
        )

    return JsonResponse(visible_factions, safe=False)


def get_rank_bracket(level):
    """Clasifica el nivel de rango en bracket"""
    if level <= 25:
        return "low"
    elif level <= 50:
        return "mid"
    elif level <= 75:
        return "high"
    else:
        return "command"


def get_rank_bracket_display(bracket):
    """Retorna el nombre para mostrar del bracket"""
    displays = {
        "low": "Low Rank",
        "mid": "Mid Rank",
        "high": "High Rank",
        "command": "High Command",
    }
    return displays.get(bracket, "Unknown")


def my_factions(request):
    """Lista de facciones del usuario (miembro o líder)"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "No autenticado"}, status=401)

    from characters.models import Character

    # Facciones donde el usuario tiene personajes
    memberships = CharacterFactionMembership.objects.filter(
        character__owner=request.user, status=CharacterFactionMembership.Status.ACTIVE
    ).select_related("faction", "rank", "access_card")

    factions_data = []
    for m in memberships:
        faction = m.faction
        factions_data.append(
            {
                "faction_id": faction.id,
                "faction_name": faction.get_visible_name(request.user),
                "faction_type": faction.faction_type,
                "is_leader": request.user in faction.leaders.all(),
                "rank": m.rank.name if m.rank else "Miembro",
                "access_card": m.access_card.level if m.access_card else "L1",
                "allow_applications": faction.allow_applications,
                "is_public": faction.is_public,
            }
        )

    # Agregar facciones donde es líder aunque no tenga personajes
    led_factions = Faction.objects.filter(
        leaders=request.user, status=Faction.Status.ACTIVE
    ).exclude(id__in=[f["faction_id"] for f in factions_data])

    for faction in led_factions:
        factions_data.append(
            {
                "faction_id": faction.id,
                "faction_name": faction.display_name,
                "faction_type": faction.faction_type,
                "is_leader": True,
                "rank": "Líder",
                "access_card": None,
                "allow_applications": faction.allow_applications,
                "is_public": faction.is_public,
            }
        )

    return JsonResponse({"factions": factions_data}, safe=False)


@csrf_exempt
def faction_all(request):
    """Lista de todas las facciones (solo admin)"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "No autenticado"}, status=401)

    if not request.user.is_superuser:
        return JsonResponse({"error": "Solo admins"}, status=403)

    factions = Faction.objects.filter(status=Faction.Status.ACTIVE)

    factions_data = []
    for faction in factions:
        leaders = faction.leaders.all()
        leaders_data = [
            {"id": l.id, "roblox_id": l.roblox_id, "roblox_username": l.roblox_username}
            for l in leaders
        ]
        factions_data.append(
            {
                "id": faction.id,
                "name": faction.display_name,
                "real_name": faction.name,
                "type": faction.faction_type,
                "is_classified": faction.is_classified,
                "is_public": faction.is_public,
                "allow_applications": faction.allow_applications,
                "description": faction.description,
                "icon": faction.icon,
                "color": faction.color,
                "member_count": faction.memberships.filter(
                    status=CharacterFactionMembership.Status.ACTIVE
                ).count(),
                "leaders": leaders_data,
            }
        )

    return JsonResponse({"factions": factions_data}, safe=False)


@csrf_exempt
@login_required
def faction_create(request):
    """Crear una facción (solo admin)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not request.user.is_superuser:
        return JsonResponse({"error": "Solo admins"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    name = data.get("name")
    display_name = data.get("display_name")
    faction_type = data.get("type", "department")
    description = data.get("description", "")
    icon = data.get("icon", "")
    color = data.get("color", "#1a1a2e")
    is_public = data.get("is_public", True)
    allow_applications = data.get("allow_applications", True)
    is_classified = data.get("is_classified", False)
    facade_name = data.get("facade_name", "")
    leader_id = data.get("leader_id")

    if not name or not display_name:
        return JsonResponse({"error": "Nombre requerido"}, status=400)

    from django.contrib.auth import get_user_model
    from factions.models import FactionRank, AccessCard

    User = get_user_model()

    faction = Faction.objects.create(
        name=name,
        display_name=display_name,
        faction_type=faction_type,
        description=description,
        icon=icon,
        color=color,
        is_public=is_public,
        allow_applications=allow_applications,
        is_classified=is_classified,
        facade_name=facade_name,
    )

    # Crear rango temporal (nivel 0) - para nuevos miembros
    temporal_rank = FactionRank.objects.create(
        faction=faction,
        name="Temporal",
        level=0,
        can_manage_members=False,
        can_review_applications=False,
        can_assign_ranks=False,
    )

    # Crear rangos por defecto
    # Recluta - nivel más bajo (entrada)
    recluta_rank = FactionRank.objects.create(
        faction=faction,
        name="Recluta",
        level=1,
        can_manage_members=False,
        can_review_applications=False,
        can_assign_ranks=False,
    )

    # Líder - nivel más alto
    lider_rank = FactionRank.objects.create(
        faction=faction,
        name="Líder",
        level=100,
        can_manage_members=True,
        can_review_applications=True,
        can_assign_ranks=True,
    )

    # Asignar el rango temporal como rango por defecto
    faction.default_rank = temporal_rank
    faction.save()

    # Asignar líder si se proporciona
    if leader_id:
        try:
            leader = User.objects.get(id=leader_id)
            faction.leaders.add(leader)
        except User.DoesNotExist:
            pass

    # Notificar al líder si se asignó
    if leader_id:
        from announcements.models import Notification

        try:
            leader = User.objects.get(id=leader_id)
            Notification.objects.create(
                user=leader,
                notification_type=Notification.NotificationType.SYSTEM,
                title="Nueva facción asignada",
                message=f"Se te ha asignado como líder de la facción: {faction.display_name}",
                related_faction=faction,
            )
        except:
            pass

    return JsonResponse(
        {
            "success": True,
            "faction_id": faction.id,
            "message": "Facción creada correctamente con rangos por defecto",
        }
    )


@csrf_exempt
@login_required
def faction_update(request, faction_id):
    """Actualizar una facción (solo admin)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not request.user.is_superuser:
        return JsonResponse({"error": "Solo admins"}, status=403)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    faction.name = data.get("name", faction.name)
    faction.display_name = data.get("display_name", faction.display_name)
    faction.faction_type = data.get("faction_type", faction.faction_type)
    faction.description = data.get("description", faction.description)
    faction.color = data.get("color", faction.color)
    faction.is_public = data.get("is_public", faction.is_public)
    faction.allow_applications = data.get(
        "allow_applications", faction.allow_applications
    )
    faction.save()

    leader_id = data.get("leader_id")
    if leader_id is not None:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        faction.leaders.clear()
        if leader_id:
            try:
                leader = User.objects.get(id=leader_id)
                faction.leaders.add(leader)

                # Notificar al nuevo líder
                from announcements.models import Notification

                try:
                    Notification.objects.create(
                        user=leader,
                        notification_type=Notification.NotificationType.SYSTEM,
                        title="Facción actualizada",
                        message=f"Se te ha asignado como líder de la facción: {faction.display_name}",
                        related_faction=faction,
                    )
                except:
                    pass
            except User.DoesNotExist:
                pass

    return JsonResponse(
        {
            "success": True,
            "message": "Facción actualizada correctamente",
        }
    )


@csrf_exempt
def faction_detail(request, faction_id):
    """Detalles de una facción"""
    user = request.user

    try:
        faction = Faction.objects.get(id=faction_id, status=Faction.Status.ACTIVE)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Obtener rangos clasificados por bracket
    ranks = faction.ranks.all().order_by("level")
    ranks_by_bracket = {"low": [], "mid": [], "high": [], "command": []}
    for rank in ranks:
        bracket = get_rank_bracket(rank.level)
        ranks_by_bracket[bracket].append(
            {
                "id": rank.id,
                "name": rank.name,
                "level": rank.level,
                "bracket": bracket,
                "access_card": {
                    "id": rank.access_card.id,
                    "level": rank.access_card.level,
                    "display_name": rank.access_card.display_name,
                }
                if rank.access_card
                else None,
            }
        )

    # Obtener divisiones
    divisions = faction.divisions.all()
    divisions_data = []
    for div in divisions:
        div_ranks = div.ranks.all().order_by("level")
        divisions_data.append(
            {
                "id": div.id,
                "name": div.name,
                "description": div.description,
                "access_card": {
                    "id": div.access_card.id,
                    "level": div.access_card.level,
                    "display_name": div.access_card.display_name,
                }
                if div.access_card
                else None,
                "ranks": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "level": r.level,
                    }
                    for r in div_ranks
                ],
            }
        )

    data = {
        "id": faction.id,
        "name": faction.get_visible_name(user),
        "type": faction.faction_type,
        "is_classified": faction.is_classified,
        "description": faction.description,
        "icon": faction.icon,
        "color": faction.color,
        "allow_applications": faction.allow_applications,
        "ranks_by_bracket": ranks_by_bracket,
        "divisions": divisions_data,
    }

    # Si el usuario tiene acceso, mostrar líderes
    if user.is_authenticated:
        highest_card = user.get_highest_access_card()
        if highest_card and highest_card.level in ["L5", "L6"]:
            data["leaders"] = [
                {"id": l.id, "username": l.roblox_username}
                for l in faction.leaders.all()
            ]
            data["real_name"] = faction.name

    return JsonResponse(data)


@csrf_exempt
def faction_members(request, faction_id):
    """Lista de miembros activos de una facción"""
    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    memberships = CharacterFactionMembership.objects.filter(
        faction=faction, status=CharacterFactionMembership.Status.ACTIVE
    ).select_related("character", "rank", "access_card")

    members = []
    member_owner_ids = set()
    current_user = request.user if request.user.is_authenticated else None

    for m in memberships:
        member_owner_ids.add(m.character.owner_id)
        # Aplicar fachada según nivel de acceso
        character_name = m.character.codename
        if faction.is_classified:
            if current_user:
                highest_card = current_user.get_highest_access_card()
                if not (highest_card and highest_card.level in ["L5", "L6"]):
                    character_name = f"[CLASIFICADO]"

        members.append(
            {
                "id": m.id,
                "character_id": m.character.id,
                "character_name": character_name,
                "rank_id": m.rank.id if m.rank else None,
                "rank": m.rank.name if m.rank else "Miembro",
                "rank_level": m.rank.level if m.rank else 0,
                "access_card": m.access_card.name if m.access_card else None,
                "is_leader": current_user == m.character.owner
                if current_user
                else False,
                "joined_at": m.joined_at.isoformat() if m.joined_at else None,
            }
        )

    # Agregar líderes que no tienen membership activa.
    # (Antes comparaba user.id contra ids de personaje: nunca coincidía y
    # duplicaba al líder con una fila fantasma sin membresía editable.)
    for leader in faction.leaders.all():
        if leader.id not in member_owner_ids:
            # Buscar personaje del líder
            from characters.models import Character

            leader_character = Character.objects.filter(owner=leader).first()
            if leader_character:
                members.append(
                    {
                        "id": None,
                        "character_id": leader_character.id,
                        "character_name": leader_character.codename,
                        "rank_id": None,
                        "rank": "Líder",
                        "rank_level": 100,
                        "access_card": None,
                        "is_leader": True,
                        "joined_at": None,
                    }
                )

    return JsonResponse({"members": members}, safe=False)


@csrf_exempt
@login_required
def faction_apply(request, faction_id):
    """Solicitar ingreso a una facción"""
    print(f"DEBUG faction_apply: user={request.user.username}, faction_id={faction_id}")

    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id, status=Faction.Status.ACTIVE)
        print(f"DEBUG: Found faction: {faction.name}")
    except Faction.DoesNotExist:
        print(f"DEBUG: Faction {faction_id} not found")
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar si permite solicitudes públicas
    if not faction.allow_applications:
        print(f"DEBUG: Faction {faction.name} does not allow applications")
        return JsonResponse(
            {"error": "Esta facción no acepta solicitudes públicas"}, status=400
        )

    # Verificar si es pública o el usuario es admin/miembro
    if not faction.is_public:
        if not request.user.is_superuser:
            print(f"DEBUG: Faction {faction.name} is private and user is not superuser")
            return JsonResponse(
                {"error": "Esta facción es privada. Solo por invitación."}, status=403
            )

    try:
        data = json.loads(request.body)
        character_id = data.get("character_id")
        message = data.get("message", "")
        print(f"DEBUG: character_id={character_id}, message={message}")
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON decode error: {e}")
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    from characters.models import Character

    try:
        character = Character.objects.get(id=character_id, owner=request.user)
        print(f"DEBUG: Found character: {character.codename}")
    except Character.DoesNotExist:
        print(
            f"DEBUG: Character {character_id} not found for user {request.user.username}"
        )
        return JsonResponse({"error": "Personaje no encontrado"}, status=404)

    # Verificar si ya tiene membresía activa
    if CharacterFactionMembership.objects.filter(
        character=character, status=CharacterFactionMembership.Status.ACTIVE
    ).exists():
        return JsonResponse(
            {"error": "El personaje ya tiene una facción activa"}, status=400
        )

    # Verificar si ya hay solicitud pendiente
    if FactionApplication.objects.filter(
        character=character, status=FactionApplication.Status.PENDING
    ).exists():
        return JsonResponse({"error": "Ya existe una solicitud pendiente"}, status=400)

    # Crear solicitud
    application = FactionApplication.objects.create(
        character=character, faction=faction, message=message
    )

    # Notificar a líderes de la facción
    for leader in faction.leaders.all():
        Notification.objects.create(
            user=leader,
            notification_type=Notification.NotificationType.FACTION_APPLICATION,
            title="Nueva solicitud de ingreso",
            message=f"{character.codename} ha solicitado unirse a {faction.display_name}",
            related_faction=faction,
            related_application=application,
        )

    return JsonResponse(
        {
            "success": True,
            "application_id": application.id,
            "message": "Solicitud enviada correctamente",
        }
    )


@csrf_exempt
def faction_ranks(request, faction_id):
    """Lista de rangos de una facción"""
    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    ranks = faction.ranks.all().order_by("-level")

    ranks_data = []
    for rank in ranks:
        ranks_data.append(
            {
                "id": rank.id,
                "name": rank.name,
                "level": rank.level,
                "can_manage_members": rank.can_manage_members,
                "can_review_applications": rank.can_review_applications,
                "can_assign_ranks": rank.can_assign_ranks,
                "access_card": {
                    "id": rank.access_card.id,
                    "level": rank.access_card.level,
                    "display_name": rank.access_card.display_name,
                }
                if rank.access_card
                else None,
            }
        )

    return JsonResponse({"ranks": ranks_data}, safe=False)


@login_required
@csrf_exempt
def my_applications(request):
    """Ver mis solicitudes de ingreso"""
    from characters.models import Character

    characters = Character.objects.filter(owner=request.user)
    applications = (
        FactionApplication.objects.filter(character__in=characters)
        .select_related("faction", "character")
        .order_by("-created_at")
    )

    apps_data = []
    for app in applications:
        apps_data.append(
            {
                "id": app.id,
                "character_name": app.character.codename,
                "faction_name": app.faction.get_visible_name(request.user),
                "status": app.status,
                "message": app.message,
                "reviewed_by": app.reviewed_by.roblox_username
                if app.reviewed_by
                else None,
                "review_notes": app.review_notes,
                "created_at": app.created_at.isoformat() if app.created_at else None,
                "reviewed_at": app.reviewed_at.isoformat() if app.reviewed_at else None,
            }
        )

    return JsonResponse({"applications": apps_data}, safe=False)


@csrf_exempt
@login_required
def cancel_application(request, app_id):
    """Cancelar una solicitud pendiente"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        application = FactionApplication.objects.get(
            id=app_id,
            character__owner=request.user,
            status=FactionApplication.Status.PENDING,
        )
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Solicitud no encontrada"}, status=404)

    application.status = FactionApplication.Status.REJECTED
    application.save()

    return JsonResponse({"success": True, "message": "Solicitud cancelada"})


@login_required
@csrf_exempt
def faction_dashboard(request, faction_id):
    """Dashboard de facción para líderes"""
    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar si es líder
    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes acceso"}, status=403)

    # Miembros activos
    memberships = CharacterFactionMembership.objects.filter(
        faction=faction, status=CharacterFactionMembership.Status.ACTIVE
    ).select_related("character", "rank", "access_card")

    members_data = []
    for m in memberships:
        members_data.append(
            {
                "id": m.id,
                "character_id": m.character.id,
                "character_name": m.character.codename,
                "rank": m.rank.name if m.rank else None,
                "rank_id": m.rank.id if m.rank else None,
                "access_card": m.access_card.level if m.access_card else "L1",
                "joined_at": m.joined_at.isoformat() if m.joined_at else None,
            }
        )

    # Solicitudes pendientes
    pending_apps = FactionApplication.objects.filter(
        faction=faction, status=FactionApplication.Status.PENDING
    ).select_related("character")

    applications_data = []
    for app in pending_apps:
        applications_data.append(
            {
                "id": app.id,
                "character_name": app.character.codename,
                "message": app.message,
                "created_at": app.created_at.isoformat() if app.created_at else None,
            }
        )

    # Rangos
    ranks = faction.ranks.all().order_by("-level")
    ranks_data = []
    for r in ranks:
        ranks_data.append(
            {
                "id": r.id,
                "name": r.name,
                "level": r.level,
                "access_card": r.access_card.level if r.access_card else None,
            }
        )

    return JsonResponse(
        {
            "faction": {
                "id": faction.id,
                "name": faction.display_name,
                "type": faction.faction_type,
            },
            "members": members_data,
            "pending_applications": applications_data,
            "ranks": ranks_data,
        }
    )


@login_required
@csrf_exempt
def faction_applications(request, faction_id):
    """Ver solicitudes pendientes de una facción"""
    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos
    can_review = False
    if request.user in faction.leaders.all():
        can_review = True
    if request.user.has_permission("moderate_factions_full"):
        can_review = True

    if not can_review and not request.user.is_superuser:
        return JsonResponse({"error": "No tienes acceso"}, status=403)

    applications = FactionApplication.objects.filter(
        faction=faction, status=FactionApplication.Status.PENDING
    ).select_related("character")

    apps_data = []
    for app in applications:
        apps_data.append(
            {
                "id": app.id,
                "character_id": app.character.id,
                "character_name": app.character.codename,
                "message": app.message,
                "created_at": app.created_at.isoformat() if app.created_at else None,
            }
        )

    return JsonResponse({"applications": apps_data}, safe=False)


@csrf_exempt
@login_required
def review_application(request, faction_id, app_id):
    """Aceptar o rechazar una solicitud"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos
    can_review = False
    if request.user in faction.leaders.all():
        can_review = True
    if request.user.has_permission("moderate_factions_full"):
        can_review = True

    if not can_review and not request.user.is_superuser:
        return JsonResponse({"error": "No tienes acceso"}, status=403)

    try:
        application = FactionApplication.objects.get(
            id=app_id, faction=faction, status=FactionApplication.Status.PENDING
        )
    except FactionApplication.DoesNotExist:
        return JsonResponse({"error": "Solicitud no encontrada"}, status=404)

    try:
        data = json.loads(request.body)
        action = data.get("action")  # 'accept' or 'reject'
        notes = data.get("notes", "")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if action == "accept":
        # Aceptar: crear membresía
        application.status = FactionApplication.Status.ACCEPTED
        application.reviewed_by = request.user
        application.review_notes = notes

        # Usar rango temporal si existe, sino el más bajo
        initial_rank = faction.default_rank
        if not initial_rank:
            initial_rank = faction.ranks.order_by("level").first()

        # Asignar tarjeta según rango
        access_card = (
            initial_rank.access_card if initial_rank else AccessCard.get_default_card()
        )

        # (character, faction) es unique_together: si el personaje ya estuvo
        # en la facción (p. ej. fue expulsado), hay que reactivar esa fila,
        # no crear una nueva — create() reventaba con IntegrityError.
        membership, _ = CharacterFactionMembership.objects.update_or_create(
            character=application.character,
            faction=faction,
            defaults={
                "rank": initial_rank,
                "access_card": access_card,
                "status": CharacterFactionMembership.Status.ACTIVE,
                "left_at": None,
            },
        )

        # Crear log
        FactionLog.objects.create(
            faction=faction,
            action_type=FactionLog.ActionType.APPLICATION_ACCEPTED,
            character=application.character,
            performed_by=request.user,
            details={"membership_id": membership.id, "notes": notes},
        )

        application.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Solicitud aceptada",
                "membership_id": membership.id,
            }
        )

    elif action == "reject":
        application.status = FactionApplication.Status.REJECTED
        application.reviewed_by = request.user
        application.review_notes = notes
        application.save()

        FactionLog.objects.create(
            faction=faction,
            action_type=FactionLog.ActionType.APPLICATION_REJECTED,
            character=application.character,
            performed_by=request.user,
            details={"notes": notes},
        )

        return JsonResponse({"success": True, "message": "Solicitud rechazada"})

    return JsonResponse({"error": "Acción inválida"}, status=400)


@csrf_exempt
@login_required
def manage_member(request, faction_id, member_id):
    """Gestionar miembro (ascender, degradar, expulsar)"""
    if request.method not in ["POST", "DELETE"]:
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos
    can_manage = False
    if request.user in faction.leaders.all():
        can_manage = True
    if request.user.has_permission("moderate_factions_full"):
        can_manage = True

    if not can_manage and not request.user.is_superuser:
        return JsonResponse({"error": "No tienes acceso"}, status=403)

    try:
        membership = CharacterFactionMembership.objects.get(
            id=member_id, faction=faction
        )
    except CharacterFactionMembership.DoesNotExist:
        return JsonResponse({"error": "Miembro no encontrado"}, status=404)

    if request.method == "DELETE":
        # Expulsar miembro
        membership.status = CharacterFactionMembership.Status.INACTIVE
        membership.left_at = timezone.now()
        membership.save()

        FactionLog.objects.create(
            faction=faction,
            action_type=FactionLog.ActionType.MEMBER_EXPELLED,
            character=membership.character,
            performed_by=request.user,
            details={},
        )

        return JsonResponse({"success": True, "message": "Miembro expulsado"})

    # POST: cambiar rango
    try:
        data = json.loads(request.body)
        rank_id = data.get("rank_id")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if rank_id:
        try:
            new_rank = FactionRank.objects.get(id=rank_id, faction=faction)
            membership.rank = new_rank
            membership.access_card = new_rank.access_card
            membership.save()

            FactionLog.objects.create(
                faction=faction,
                action_type=FactionLog.ActionType.RANK_CHANGED,
                character=membership.character,
                performed_by=request.user,
                details={"old_rank": membership.rank.name, "new_rank": new_rank.name},
            )

            return JsonResponse(
                {"success": True, "message": f"Rango cambiado a {new_rank.name}"}
            )
        except FactionRank.DoesNotExist:
            return JsonResponse({"error": "Rango no encontrado"}, status=404)

    return JsonResponse({"error": "Datos inválidos"}, status=400)


@csrf_exempt
def access_cards_list(request):
    """Lista de tarjetas de acceso"""
    cards = AccessCard.objects.all()
    max_level = _max_assignable_card_level(request.user)

    cards_data = []
    for card in cards:
        cards_data.append(
            {
                "id": card.id,
                "name": card.name,
                "description": card.description,
                "is_classified": card.is_classified,
                "level": card.level,
                "card_type": card.card_type,
                "display_name": card.display_name,
                # Si quien pregunta puede otorgar esta tarjeta (ver
                # _max_assignable_card_level). El backend revalida igual.
                "assignable": card.level_number <= max_level,
            }
        )

    return JsonResponse({"cards": cards_data}, safe=False)


@login_required
@csrf_exempt
def create_access_card(request):
    """Crear una nueva tarjeta de acceso (solo admin)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not request.user.is_superuser:
        return JsonResponse({"error": "Solo administradores"}, status=403)

    try:
        data = json.loads(request.body)
        name = data.get("name")
        if not name:
            return JsonResponse({"error": "El nombre es requerido"}, status=400)

        level = data.get("level", AccessCard.Level.L1)
        card_type = data.get("card_type", AccessCard.CardType.STANDARD)
        if level not in AccessCard.Level.values:
            return JsonResponse({"error": "Nivel inválido"}, status=400)
        if card_type not in AccessCard.CardType.values:
            return JsonResponse({"error": "Tipo de tarjeta inválido"}, status=400)

        card = AccessCard.objects.create(
            name=name,
            description=data.get("description", ""),
            is_classified=data.get("is_classified", False),
            level=level,
            card_type=card_type,
        )

        return JsonResponse(
            {"success": True, "card_id": card.id, "message": "Tarjeta creada"}
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)


@csrf_exempt
def access_card_detail(request, card_id):
    """Detalles de una tarjeta específica"""
    try:
        card = AccessCard.objects.get(id=card_id)
    except AccessCard.DoesNotExist:
        return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)

    return JsonResponse(
        {
            "id": card.id,
            "name": card.name,
            "description": card.description,
            "is_classified": card.is_classified,
            "level": card.level,
            "card_type": card.card_type,
            "display_name": card.display_name,
        }
    )


# === INVITATIONS ===
@login_required
@csrf_exempt
def invite_member(request, faction_id):
    """Invitar a un usuario a una facción (el usuario elegirá su personaje al aceptar)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos (líder o admin)
    can_invite = False
    if request.user in faction.leaders.all():
        can_invite = True
    if request.user.is_superuser:
        can_invite = True

    if not can_invite:
        return JsonResponse({"error": "No tienes permisos"}, status=403)

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        message = data.get("message", "")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if not user_id:
        return JsonResponse({"error": "user_id es requerido"}, status=400)

    from users.models import User

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    # Verificar si ya tiene invitación pendiente para esta facción
    if FactionInvitation.objects.filter(
        user=user, faction=faction, status=FactionInvitation.Status.PENDING
    ).exists():
        return JsonResponse(
            {"error": "Ya existe una invitación pendiente para este usuario"},
            status=400,
        )

    # Crear invitación (sin personaje, el usuario elegirá al aceptar)
    invitation = FactionInvitation.objects.create(
        faction=faction,
        user=user,
        invited_by=request.user,
        message=message,
    )

    # Notificar al usuario
    Notification.objects.create(
        user=user,
        notification_type=Notification.NotificationType.FACTION_INVITATION,
        title="Invitación de facción",
        message=f"Has sido invitad@ a unirte a {faction.display_name}",
        related_faction=faction,
        related_invitation=invitation,
    )

    return JsonResponse(
        {
            "success": True,
            "invitation_id": invitation.id,
            "message": "Invitación enviada",
        }
    )


@login_required
@csrf_exempt
def my_invitations(request):
    """Ver mis invitaciones"""
    from characters.models import Character

    characters = Character.objects.filter(owner=request.user)
    invitations = (
        FactionInvitation.objects.filter(character__in=characters)
        .select_related("faction", "character", "invited_by")
        .order_by("-created_at")
    )

    invitations_data = []
    for inv in invitations:
        invitations_data.append(
            {
                "id": inv.id,
                "faction_name": inv.faction.get_visible_name(request.user),
                "character_name": inv.character.codename,
                "status": inv.status,
                "message": inv.message,
                "invited_by": inv.invited_by.roblox_username
                if inv.invited_by
                else None,
                "created_at": inv.created_at.isoformat() if inv.created_at else None,
            }
        )

    return JsonResponse({"invitations": invitations_data}, safe=False)


@login_required
@csrf_exempt
def faction_invitations(request, faction_id):
    """Ver invitaciones enviadas por una facción"""
    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos
    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    invitations = (
        FactionInvitation.objects.filter(faction=faction)
        .select_related("faction", "invited_by", "user")
        .order_by("-created_at")
    )

    invitations_data = []
    for inv in invitations:
        user_name = None
        if inv.user:
            user_name = inv.user.roblox_username
        elif inv.character:
            user_name = inv.character.codename

        invitations_data.append(
            {
                "id": inv.id,
                "user_id": inv.user.id if inv.user else None,
                "user_name": user_name,
                "status": inv.status,
                "message": inv.message,
                "invited_by": inv.invited_by.roblox_username
                if inv.invited_by
                else None,
                "created_at": inv.created_at.isoformat() if inv.created_at else None,
            }
        )

    return JsonResponse({"invitations": invitations_data}, safe=False)


@login_required
@csrf_exempt
def cancel_invitation(request, invitation_id):
    """Cancelar una invitación enviada"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        invitation = FactionInvitation.objects.get(id=invitation_id)
    except FactionInvitation.DoesNotExist:
        return JsonResponse({"error": "Invitación no encontrada"}, status=404)

    # Verificar permisos (líder de la facción o admin)
    if request.user not in invitation.faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    invitation.status = FactionInvitation.Status.DECLINED
    invitation.save()

    return JsonResponse({"success": True})


@login_required
@csrf_exempt
def respond_invitation(request, invitation_id):
    """Aceptar o rechazar invitación"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    # Las invitaciones nuevas se emiten al usuario y sin personaje (ver
    # invite_user_to_faction); `character` solo sobrevive en las viejas.
    try:
        invitation = FactionInvitation.objects.get(
            Q(user=request.user) | Q(character__owner=request.user),
            id=invitation_id,
            status=FactionInvitation.Status.PENDING,
        )
    except FactionInvitation.DoesNotExist:
        return JsonResponse({"error": "Invitación no encontrada"}, status=404)

    try:
        data = json.loads(request.body)
        action = data.get("action")  # 'accept' or 'decline'
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if action == "accept":
        from characters.models import Character

        # La invitación no trae personaje: el usuario elige cuál se une.
        character = invitation.character
        if character is None:
            character_id = data.get("character_id")
            if not character_id:
                return JsonResponse(
                    {"error": "Elegí con qué personaje unirte"}, status=400
                )
            try:
                character = Character.objects.get(id=character_id, owner=request.user)
            except Character.DoesNotExist:
                return JsonResponse({"error": "Personaje no encontrado"}, status=404)

        # Verificar si ya tiene membresía activa
        if CharacterFactionMembership.objects.filter(
            character=character,
            status=CharacterFactionMembership.Status.ACTIVE,
        ).exists():
            return JsonResponse(
                {"error": "El personaje ya tiene una facción activa"}, status=400
            )

        invitation.character = character
        invitation.accept()

        # Notificar al líder
        Notification.objects.create(
            user=invitation.invited_by,
            notification_type=Notification.NotificationType.SYSTEM,
            title="Invitación aceptada",
            message=f"{character.codename} ha aceptado la invitación a {invitation.faction.display_name}",
            related_faction=invitation.faction,
        )

        return JsonResponse({"success": True, "message": "Te has unido a la facción"})

    elif action == "decline":
        invitation.decline()
        return JsonResponse({"success": True, "message": "Invitación rechazada"})

    return JsonResponse({"error": "Acción inválida"}, status=400)


# === NOTIFICATIONS ===
@login_required
@csrf_exempt
def notifications_list(request):
    """Lista de notificaciones del usuario"""
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:50]

    notifications_data = []
    for notif in notifications:
        notifications_data.append(
            {
                "id": notif.id,
                "type": notif.notification_type,
                "title": notif.title,
                "message": notif.message,
                "is_read": notif.is_read,
                # Para poder navegar al panel correspondiente desde la notificación
                "faction_id": notif.related_faction_id,
                # El id de la notificación NO es el de la invitación: el modal
                # de respuesta necesita este.
                "invitation_id": notif.related_invitation_id,
                "created_at": notif.created_at.isoformat()
                if notif.created_at
                else None,
            }
        )

    return JsonResponse({"notifications": notifications_data}, safe=False)


@login_required
@csrf_exempt
def notifications_unread_count(request):
    """Cantidad de notificaciones no leídas"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()

    return JsonResponse({"unread_count": count})


@login_required
@csrf_exempt
def mark_notification_read(request, notification_id):
    """Marcar notificación como leída"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
    except Notification.DoesNotExist:
        return JsonResponse({"error": "Notificación no encontrada"}, status=404)

    notification.mark_as_read()
    return JsonResponse({"success": True})


@login_required
@csrf_exempt
def mark_all_notifications_read(request):
    """Marcar todas las notificaciones como leídas"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

    from django.utils import timezone

    Notification.objects.filter(user=request.user, is_read=False).update(
        read_at=timezone.now()
    )

    return JsonResponse({"success": True})


def _max_assignable_card_level(user) -> int:
    """
    Nivel máximo de tarjeta que un usuario puede asignar a un rango.
    Un líder no puede otorgar más acceso del que él mismo tiene; los admins
    no tienen tope. Devuelve 0 si el usuario no tiene tarjeta alguna.
    """
    if getattr(user, "is_superuser", False):
        return LEVEL_ORDER["L6"]
    if not getattr(user, "is_authenticated", False):
        return 0
    card = user.get_highest_access_card()
    return card.level_number if card else 0


# === ADMIN: Crear/Editar Rangos de Facción ===
@login_required
@csrf_exempt
def create_faction_rank(request, faction_id):
    """Crear un rango para una facción"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos (líder o admin)
    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    try:
        data = json.loads(request.body)
        name = data.get("name")
        access_card_id = data.get("access_card_id")
        can_manage_members = data.get("can_manage_members", False)
        can_review_applications = data.get("can_review_applications", False)
        can_assign_ranks = data.get("can_assign_ranks", False)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if not name:
        return JsonResponse({"error": "El nombre es requerido"}, status=400)

    if FactionRank.objects.filter(faction=faction, name=name).exists():
        return JsonResponse({"error": "Ya existe un rango con ese nombre"}, status=400)

    # Tarjeta: mismo tope que al editar (ver update_faction_rank). Se
    # identifica por id, no por nivel: varias tarjetas comparten nivel
    # (L6 es O5, RAISA, Administración y Beta-1 a la vez).
    access_card_obj = None
    if access_card_id:
        try:
            access_card_obj = AccessCard.objects.get(id=access_card_id)
        except AccessCard.DoesNotExist:
            return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)
        if access_card_obj.level_number > _max_assignable_card_level(request.user):
            return JsonResponse(
                {"error": "No podés asignar una tarjeta superior a la tuya"},
                status=403,
            )

    # Nivel jerárquico: define el bracket (1-25 bajo, 26-50 medio,
    # 51-75 alto, 76-100 alto mando). Se respeta el enviado; si no
    # viene, se deriva de la tarjeta.
    try:
        level = int(data.get("level") or 0)
    except (TypeError, ValueError):
        level = 0
    if not 1 <= level <= 100:
        level = access_card_obj.level_number if access_card_obj else 1

    # Crear rango
    rank = FactionRank.objects.create(
        faction=faction,
        name=name,
        level=level,
        access_card=access_card_obj,
        can_manage_members=can_manage_members,
        can_review_applications=can_review_applications,
        can_assign_ranks=can_assign_ranks,
    )

    return JsonResponse(
        {"success": True, "rank_id": rank.id, "message": "Rango creado"}
    )


@login_required
@csrf_exempt
def update_faction_rank(request, faction_id, rank_id):
    """Editar un rango: nombre, nivel (bracket), permisos y tarjeta."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
        rank = FactionRank.objects.get(id=rank_id, faction=faction)
    except (Faction.DoesNotExist, FactionRank.DoesNotExist):
        return JsonResponse({"error": "Rango no encontrado"}, status=404)

    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    name = (data.get("name") or rank.name).strip()
    if (
        name != rank.name
        and FactionRank.objects.filter(faction=faction, name=name).exists()
    ):
        return JsonResponse({"error": "Ya existe un rango con ese nombre"}, status=400)
    rank.name = name

    if "level" in data:
        try:
            level = int(data.get("level"))
        except (TypeError, ValueError):
            return JsonResponse({"error": "Nivel inválido"}, status=400)
        if not 1 <= level <= 100:
            return JsonResponse({"error": "El nivel debe estar entre 1 y 100"}, status=400)
        rank.level = level

    for flag in ("can_manage_members", "can_review_applications", "can_assign_ranks"):
        if flag in data:
            setattr(rank, flag, bool(data[flag]))

    # Tarjeta: un líder puede elegirla, pero nunca por encima de la suya
    # (el bracket 1-100 no determina el nivel de acceso: un rango medio puede
    # llevar L2, L4 o ninguna). Los admins no tienen tope.
    if "access_card_id" in data:
        max_level = _max_assignable_card_level(request.user)

        # Tampoco puede tocar un rango cuya tarjeta actual lo supera: si no
        # puede otorgar ese nivel, tampoco puede quitarlo.
        if rank.access_card and rank.access_card.level_number > max_level:
            return JsonResponse(
                {"error": "No podés modificar la tarjeta de un rango superior al tuyo"},
                status=403,
            )

        card_id = data.get("access_card_id")
        if card_id:
            try:
                card = AccessCard.objects.get(id=card_id)
            except AccessCard.DoesNotExist:
                return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)
            if card.level_number > max_level:
                return JsonResponse(
                    {"error": "No podés asignar una tarjeta superior a la tuya"},
                    status=403,
                )
            rank.access_card = card
        else:
            rank.access_card = None

    rank.save()
    return JsonResponse({"success": True, "message": "Rango actualizado"})


@login_required
@csrf_exempt
def delete_faction_rank(request, faction_id, rank_id):
    """Eliminar un rango sin miembros asignados."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
        rank = FactionRank.objects.get(id=rank_id, faction=faction)
    except (Faction.DoesNotExist, FactionRank.DoesNotExist):
        return JsonResponse({"error": "Rango no encontrado"}, status=404)

    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    in_use = CharacterFactionMembership.objects.filter(
        rank=rank, status=CharacterFactionMembership.Status.ACTIVE
    ).count()
    if in_use:
        return JsonResponse(
            {"error": f"No se puede eliminar: {in_use} miembro(s) tienen este rango. Reasígnalos primero."},
            status=400,
        )

    if faction.default_rank_id == rank.id:
        faction.default_rank = None
        faction.save(update_fields=["default_rank"])

    rank.delete()
    return JsonResponse({"success": True, "message": "Rango eliminado"})


@login_required
@csrf_exempt
def faction_divisions(request, faction_id):
    """Lista de divisiones de una facción"""
    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    divisions = faction.divisions.all()
    divisions_data = []
    for div in divisions:
        # Obtener miembros de la división
        members = div.members.all()
        members_data = []
        for m in members:
            members_data.append(
                {
                    "id": m.id,
                    "character_id": m.id,
                    "character_name": m.codename,
                }
            )

        divisions_data.append(
            {
                "id": div.id,
                "name": div.name,
                "description": div.description,
                "is_public": div.is_public,
                "access_card_id": div.access_card.id if div.access_card else None,
                "members": members_data,
            }
        )

    return JsonResponse({"divisions": divisions_data}, safe=False)


@login_required
@csrf_exempt
def create_division(request, faction_id):
    """Crear una división para una facción"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos (líder o admin)
    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    # Verificar máximo de 5 divisiones
    if faction.divisions.count() >= 5:
        return JsonResponse({"error": "Máximo de 5 divisiones permitidas"}, status=400)

    try:
        data = json.loads(request.body)
        name = data.get("name")
        description = data.get("description", "")
        is_public = data.get("is_public", True)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    if not name:
        return JsonResponse({"error": "El nombre es requerido"}, status=400)

    division = FactionDivision.objects.create(
        faction=faction,
        name=name,
        description=description,
        is_public=is_public,
    )

    return JsonResponse(
        {"success": True, "division_id": division.id, "message": "División creada"}
    )


@login_required
@csrf_exempt
def add_member_to_division(request, faction_id, division_id):
    """Agregar un miembro a una división"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        faction = Faction.objects.get(id=faction_id)
    except Faction.DoesNotExist:
        return JsonResponse({"error": "Facción no encontrada"}, status=404)

    # Verificar permisos (líder o admin)
    if request.user not in faction.leaders.all():
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permisos"}, status=403)

    try:
        division = FactionDivision.objects.get(id=division_id, faction=faction)
    except FactionDivision.DoesNotExist:
        return JsonResponse({"error": "División no encontrada"}, status=404)

    # Verificar máximo de 10 miembros
    if division.members.count() >= 10:
        return JsonResponse({"error": "Máximo de 10 miembros por división"}, status=400)

    try:
        data = json.loads(request.body)
        character_id = data.get("character_id")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    from characters.models import Character

    try:
        character = Character.objects.get(id=character_id, owner=request.user)
    except Character.DoesNotExist:
        return JsonResponse({"error": "Personaje no encontrado"}, status=404)

    # Agregar a la división
    division.members.add(character)

    return JsonResponse({"success": True, "message": "Miembro agregado a la división"})


# === ADMIN: Actualizar Tarjeta de Acceso ===
@login_required
@csrf_exempt
def update_access_card(request, card_id):
    """Actualizar una tarjeta de acceso (solo admin)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not request.user.is_superuser:
        return JsonResponse({"error": "Solo administradores"}, status=403)

    try:
        card = AccessCard.objects.get(id=card_id)
    except AccessCard.DoesNotExist:
        return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)

    try:
        data = json.loads(request.body)
        card.name = data.get("name", card.name)
        card.description = data.get("description", card.description)
        card.is_classified = data.get("is_classified", card.is_classified)

        level = data.get("level", card.level)
        card_type = data.get("card_type", card.card_type)
        if level not in AccessCard.Level.values:
            return JsonResponse({"error": "Nivel inválido"}, status=400)
        if card_type not in AccessCard.CardType.values:
            return JsonResponse({"error": "Tipo de tarjeta inválido"}, status=400)
        card.level = level
        card.card_type = card_type
        card.save()

        return JsonResponse({"success": True, "message": "Tarjeta actualizada"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)


from django.utils import timezone
