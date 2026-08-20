""" from ..decorators import require_staff_permission
from django.http import JsonResponse
from documents.models import Document

@require_staff_permission("edit_rp_files_basic")
def api_edit_rp_files_basic(request, doc_id):
    doc = Document.objects.get(id=doc_id)

    if doc.level > request.user.max_access_level:
        return JsonResponse({"error": "forbidden"}, status=403)

    return JsonResponse({
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "level": doc.level,
    })

@require_staff_permission("edit_rp_files_full")
def api_edit_rp_files_full(request, doc_id):
    doc = Document.objects.get(id=doc_id)

    return JsonResponse({
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "level": doc.level,
        "metadata": doc.metadata,
    })
 """