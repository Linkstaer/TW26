import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from characters.models import Character

logger = logging.getLogger(__name__)

User = get_user_model()

@login_required
def api_get_user_by_roblox_id(request, roblox_id):
    """
    Perfil de usuario (spec §1.2).

    Devuelve Roblox ID y username, fecha de primer acceso, roles especiales,
    facciones activas de sus personajes (con fachadas) y el acceso derivado de
    la tarjeta más alta de todos sus personajes.

    Antes esta vista no pedía autenticación: exponía la base de usuarios,
    con roblox_id y flags de staff, a cualquier anónimo.
    """
    user = get_object_or_404(User, roblox_id=roblox_id)

    is_self = user.id == request.user.id
    is_moderator = request.user.is_superuser or request.user.has_permission(
        "access_moderation_dashboard"
    )

    # Roles especiales (Admin, High Command, O5...): los de staff salen del
    # StaffRole y los de RP de las tarjetas especiales de sus personajes.
    special_roles = []
    if user.is_superuser:
        special_roles.append({"kind": "staff", "name": "Administrador"})
    for role in user.staff_roles.all():
        special_roles.append(
            {
                "kind": "staff",
                "name": f"{role.get_scope_display()} · {role.get_level_display()}",
            }
        )

    highest_card = user.get_highest_access_card()
    # get_visible_factions aplica fachadas contra el usuario dueño; acá la
    # pregunta es qué puede ver QUIEN CONSULTA, así que se resuelve de nuevo.
    from factions.models import AccessCard, CharacterFactionMembership

    memberships = (
        CharacterFactionMembership.objects.filter(
            character__owner=user, status=CharacterFactionMembership.Status.ACTIVE
        )
        .select_related("faction", "rank", "access_card")
        .order_by("faction__display_name")
    )

    factions = []
    for membership in memberships:
        faction = membership.faction
        factions.append(
            {
                "id": faction.id,
                "name": faction.get_visible_name(request.user),
                "is_classified": faction.is_classified,
                "rank": membership.rank.name if membership.rank else None,
                "character": membership.character_id,
            }
        )
        card = membership.access_card
        if card and card.card_type != AccessCard.CardType.STANDARD:
            role_name = card.get_card_type_display()
            if not any(r["name"] == role_name for r in special_roles):
                special_roles.append({"kind": "rp", "name": role_name})

    data = {
        "roblox_username": user.roblox_username,
        "roblox_id": user.roblox_id,
        "id": user.id,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "is_booster": user.is_booster,
        "first_login": user.first_login.isoformat() if user.first_login else None,
        "last_login": user.last_login.isoformat() if user.last_login else None,
        # Acceso derivado de la tarjeta más alta de todos sus personajes (§1.2)
        "access_card": {
            "name": highest_card.display_name if highest_card else None,
            "level": highest_card.level if highest_card else "L1",
        },
        "special_roles": special_roles,
        "factions": factions,
    }

    # El estado de moderación no es información de perfil público.
    if is_self or is_moderator:
        data["warning_count"] = user.warning_count
        data["is_banned"] = user.is_banned

    return JsonResponse(data)

@login_required
def api_get_user_characters(request, roblox_id):
    """
    Personajes de un perfil. Pasa por el serializer de characters para no
    duplicar la matriz de visibilidad (spec §4.2): el perfil es público, así
    que la facción clasificada tiene que salir con su fachada y los datos
    reservados no pueden viajar a cualquiera.
    """
    from factions.models import CharacterFactionMembership
    from characters.views import (
        _serialize_character,
        _viewer_access,
        divisions_by_character,
    )

    try:
        user = get_object_or_404(User, roblox_id=roblox_id)
        characters = list(
            Character.objects.filter(owner=user)
            .select_related("owner", "scp_file")
            .order_by("-created_at")
        )

        membership_by_char = {
            m.character_id: m
            for m in CharacterFactionMembership.objects.filter(
                character__in=characters,
                status=CharacterFactionMembership.Status.ACTIVE,
            ).select_related("faction", "rank")
        }
        division_by_char = divisions_by_character([c.id for c in characters])

        access = _viewer_access(request.user)

        characters_data = []
        for char in characters:
            data = _serialize_character(
                char,
                request.user,
                access,
                membership=membership_by_char.get(char.id),
                division=division_by_char.get(char.id),
            )
            if data is not None:
                characters_data.append(data)

        return JsonResponse({"results": characters_data}, safe=False)
    except Exception:
        logger.exception("Error listando personajes de roblox_id=%s", roblox_id)
        return JsonResponse({"error": "Error interno"}, status=500)