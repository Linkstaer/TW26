from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import SCP, SCPEditLog, Document, DocumentEditLog


def scp_list(request):
    """Lista de SCPs visibles para el usuario"""
    user = request.user

    scps = SCP.objects.filter(is_active=True, is_deleted=False)

    accessible_levels = (
        user.get_accessible_levels() if user.is_authenticated else ["L1"]
    )

    scps_data = []
    for scp in scps:
        scps_data.append(
            {
                "id": scp.id,
                "scp_id": scp.scp_id,
                "title": scp.title,
                "object_class": scp.object_class,
            }
        )

    return JsonResponse({"scps": scps_data}, safe=False)


def scp_detail(request, scp_id):
    """Detalles de un SCP con contenido según nivel de acceso"""
    user = request.user

    try:
        scp = SCP.objects.get(id=scp_id, is_active=True, is_deleted=False)
    except SCP.DoesNotExist:
        return JsonResponse({"error": "SCP no encontrado"}, status=404)

    return JsonResponse(scp.to_dict(user))


@login_required
def scp_edit(request, scp_id):
    """Editar un SCP"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        scp = SCP.objects.get(id=scp_id)
    except SCP.DoesNotExist:
        return JsonResponse({"error": "SCP no encontrado"}, status=404)

    # Verificar permisos
    can_edit, reason = scp.can_user_edit(request.user)
    if not can_edit:
        return JsonResponse({"error": reason}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    # Actualizar campos
    section = data.get("section")
    content = data.get("content")
    reason = data.get("reason", "")

    if not section or content is None:
        return JsonResponse({"error": "Sección y contenido requeridos"}, status=400)

    # Guardar contenido anterior
    old_content = getattr(scp, f"content_{section.lower()}", "")

    # Actualizar
    setattr(scp, f"content_{section.lower()}", content)
    scp.save()

    # Crear log de edición
    SCPEditLog.objects.create(
        scp=scp,
        edited_by=request.user,
        section=section,
        old_content=old_content,
        new_content=content,
        edit_reason=reason,
    )

    return JsonResponse({"success": True, "message": f"Sección {section} actualizada"})


def document_list(request):
    """Lista de documentos"""
    user = request.user

    documents = Document.objects.filter(is_published=True)

    docs_data = []
    for doc in documents:
        if doc.can_user_view(user):
            docs_data.append(
                {
                    "id": doc.id,
                    "title": doc.title,
                    "slug": doc.slug,
                    "doc_type": doc.doc_type,
                    "min_access_level": doc.min_access_level,
                    "author": doc.author.roblox_username if doc.author else None,
                    "created_at": doc.created_at.isoformat()
                    if doc.created_at
                    else None,
                }
            )

    return JsonResponse({"documents": docs_data}, safe=False)


def document_detail(request, slug):
    """Detalles de un documento"""
    user = request.user

    try:
        doc = Document.objects.get(slug=slug, is_published=True)
    except Document.DoesNotExist:
        return JsonResponse({"error": "Documento no encontrado"}, status=404)

    if not doc.can_user_view(user):
        return JsonResponse({"error": "Acceso denegado"}, status=403)

    return JsonResponse(
        {
            "id": doc.id,
            "title": doc.title,
            "slug": doc.slug,
            "doc_type": doc.doc_type,
            "content": doc.content,
            "min_access_level": doc.min_access_level,
            "author": doc.author.roblox_username if doc.author else None,
            "author_faction": doc.author_faction,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
        }
    )


@login_required
def document_edit(request, slug):
    """Editar un documento"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        doc = Document.objects.get(slug=slug)
    except Document.DoesNotExist:
        return JsonResponse({"error": "Documento no encontrado"}, status=404)

    # Verificar permisos de edición
    can_edit = False

    if request.user.is_superuser:
        can_edit = True
    else:
        highest_card = request.user.get_highest_access_card()
        if highest_card:
            if highest_card.can_edit_any:
                can_edit = True
            elif highest_card.can_edit_scd:
                # ScD puede editar procedimientos
                if doc.doc_type in [
                    Document.DocType.PROCEDURE,
                    Document.DocType.REGULATION,
                ]:
                    can_edit = True
            elif highest_card.can_edit_o5:
                can_edit = True

    if not can_edit:
        return JsonResponse({"error": "Sin permisos para editar"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    content = data.get("content")
    summary = data.get("summary", "")

    if not content:
        return JsonResponse({"error": "Contenido requerido"}, status=400)

    # Guardar versión anterior
    old_content = doc.content

    # Actualizar
    doc.content = content
    doc.save()

    # Crear log
    DocumentEditLog.objects.create(
        document=doc,
        edited_by=request.user,
        old_content=old_content,
        new_content=content,
        edit_summary=summary,
    )

    return JsonResponse({"success": True, "message": "Documento actualizado"})
