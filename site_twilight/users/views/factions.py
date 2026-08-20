""" from ..decorators import require_staff_permission
from django.http import JsonResponse
from factions.models import Faction

@require_staff_permission("moderate_factions_basic")
def api_faction_moderation_basic(request):
    factions = Faction.objects.filter(is_active=True)

    data = [{
        "id": f.id,
        "name": f.display_name,
        "type": f.type,
        "status": f.status,
    } for f in factions]

    return JsonResponse(data, safe=False)

@require_staff_permission("moderate_factions_full")
def api_faction_moderation_full(request):
    factions = Faction.objects.all()

    data = [{
        "id": f.id,
        "name": f.display_name,
        "real_name": f.name,
        "type": f.type,
        "status": f.status,
        "leaders": [l.id for l in f.leaders.all()],
    } for f in factions]

    return JsonResponse(data, safe=False)
 """