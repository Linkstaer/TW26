from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from characters.models import Character

User = get_user_model()

def api_get_user_by_roblox_id(request, roblox_id):
    try:
        user = get_object_or_404(User, roblox_id=roblox_id)
        data = {
            "roblox_username": user.roblox_username,
            "roblox_id": user.roblox_id,
            "id": user.id,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "first_login": user.first_login.isoformat() if user.first_login else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)

@login_required
def api_get_user_characters(request, roblox_id):
    """
    Personajes de un perfil. Pasa por el serializer de characters para no
    duplicar la matriz de visibilidad (spec §4.2): el perfil es público, así
    que la facción clasificada tiene que salir con su fachada y los datos
    reservados no pueden viajar a cualquiera.
    """
    from factions.models import CharacterFactionMembership, FactionDivision
    from characters.views import _serialize_character, _viewer_access

    try:
        user = get_object_or_404(User, roblox_id=roblox_id)
        characters = list(
            Character.objects.filter(owner=user)
            .select_related("owner")
            .order_by("-created_at")
        )

        membership_by_char = {
            m.character_id: m
            for m in CharacterFactionMembership.objects.filter(
                character__in=characters,
                status=CharacterFactionMembership.Status.ACTIVE,
            ).select_related("faction", "rank")
        }
        division_by_char = {}
        for dm in FactionDivision.members.through.objects.filter(
            character_id__in=[c.id for c in characters]
        ):
            division = FactionDivision.objects.filter(id=dm.factiondivision_id).first()
            if division:
                division_by_char[dm.character_id] = division.name

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
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)