""" from ..decorators import require_staff_permission
from django.http import JsonResponse
from characters.models import Character

@require_staff_permission("supervise_actors_basic")
def api_supervise_actors_basic(request):
    actors = Character.objects.filter(is_actor=True)

    data = [{
        "id": a.id,
        "name": a.display_name,
        "scp_class": a.scp_class,
        "document": a.document,
    } for a in actors]

    return JsonResponse(data, safe=False)

@require_staff_permission("supervise_actors_full")
def api_supervise_actors_full(request):
    actors = Character.objects.filter(is_actor=True)

    return JsonResponse({
        "actors": [{
            "id": a.id,
            "name": a.display_name,
            "scp_class": a.scp_class,
            "document": a.document,
        } for a in actors],
    })
 """