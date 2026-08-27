from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import SCP, SCPActorLog, SCPEditLog, Document, DocumentEditLog


def _log_actor_action(scp, user, action, description="", **details):
    """
    Registra la acción si quien la hizo es el Actor SCP del archivo (spec §3.4).
    Devuelve el log creado o None.
    """
    if not scp.is_actor(user):
        return None
    return SCPActorLog.objects.create(
        scp=scp,
        character=scp.actor_character,
        performed_by=user,
        action=action,
        description=description,
        details=details,
    )


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

    if section.upper() not in ("L1", "L2", "L3", "L4", "L5", "L6"):
        return JsonResponse({"error": "Sección inválida"}, status=400)

    # Verificar permisos por sección (O5 redacta solo hasta su nivel, spec §3.3)
    can_edit, edit_reason = scp.can_user_edit_section(request.user, section)
    if not can_edit:
        return JsonResponse({"error": edit_reason}, status=403)

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

    _log_actor_action(
        scp,
        request.user,
        SCPActorLog.Action.FILE_EDITED,
        description=f"El actor editó la sección {section.upper()}.",
        section=section.upper(),
        reason=reason,
    )

    return JsonResponse({"success": True, "message": f"Sección {section} actualizada"})


# ==================== ACTORES SCP (spec §3.4) ====================


def _can_manage_actors(user) -> bool:
    """Quién ata o desata un personaje de un archivo SCP."""
    return bool(
        user.is_authenticated
        and (user.is_superuser or user.has_permission("assign_scp_actor"))
    )


@login_required
@require_http_methods(["POST", "DELETE"])
def scp_actor(request, scp_id):
    """
    Asigna (POST) o remueve (DELETE) el Actor SCP de un archivo (spec §3.4).

    Al asignar, el archivo pasa a aparecer en el perfil del personaje y el
    dueño gana permiso de edición sobre ese SCP —y solo sobre ese.
    """
    if not _can_manage_actors(request.user):
        return JsonResponse(
            {"error": "Sin permisos para gestionar actores SCP"}, status=403
        )

    try:
        scp = SCP.objects.select_related("actor_character").get(
            id=scp_id, is_deleted=False
        )
    except SCP.DoesNotExist:
        return JsonResponse({"error": "SCP no encontrado"}, status=404)

    if request.method == "DELETE":
        previous = scp.actor_character
        if previous is None:
            return JsonResponse({"error": "El SCP no tiene actor asignado"}, status=400)

        scp.actor_character = None
        scp.save(update_fields=["actor_character", "updated_at"])

        SCPActorLog.objects.create(
            scp=scp,
            character=previous,
            performed_by=request.user,
            action=SCPActorLog.Action.UNASSIGNED,
            description=f"{previous.codename} deja de interpretar a {scp.scp_id}.",
        )
        return JsonResponse({"success": True, "actor": None})

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    character_id = data.get("character_id")
    if not character_id:
        return JsonResponse({"error": "character_id requerido"}, status=400)

    from characters.models import Character

    try:
        character = Character.objects.select_related("owner").get(
            id=character_id, status=Character.Status.ACTIVE
        )
    except Character.DoesNotExist:
        return JsonResponse({"error": "Personaje no encontrado o inactivo"}, status=404)

    # actor_character es OneToOne: un personaje no puede interpretar dos SCPs.
    existing = SCP.objects.filter(actor_character=character).exclude(id=scp.id).first()
    if existing is not None:
        return JsonResponse(
            {
                "error": f"{character.codename} ya interpreta a {existing.scp_id}",
            },
            status=400,
        )

    previous = scp.actor_character
    scp.actor_character = character
    scp.save(update_fields=["actor_character", "updated_at"])

    if previous is not None and previous.id != character.id:
        SCPActorLog.objects.create(
            scp=scp,
            character=previous,
            performed_by=request.user,
            action=SCPActorLog.Action.UNASSIGNED,
            description=f"{previous.codename} deja de interpretar a {scp.scp_id}.",
        )

    SCPActorLog.objects.create(
        scp=scp,
        character=character,
        performed_by=request.user,
        action=SCPActorLog.Action.ASSIGNED,
        description=f"{character.codename} pasa a interpretar a {scp.scp_id}.",
        details={"owner": character.owner.roblox_username},
    )

    return JsonResponse({"success": True, "actor": scp.get_actor_data(request.user)})


@login_required
@require_http_methods(["GET", "POST"])
def scp_actor_logs(request, scp_id):
    """
    Bitácora del Actor SCP (spec §3.4).

    GET: la lee el propio actor, la supervisión de actores y quien pueda
    editar el archivo. POST: el actor registra una acción de roleplay.
    """
    try:
        scp = SCP.objects.select_related("actor_character").get(
            id=scp_id, is_deleted=False
        )
    except SCP.DoesNotExist:
        return JsonResponse({"error": "SCP no encontrado"}, status=404)

    is_actor = scp.is_actor(request.user)

    if request.method == "POST":
        if not is_actor:
            return JsonResponse(
                {"error": "Solo el Actor SCP registra acciones de este archivo"},
                status=403,
            )
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

        description = (data.get("description") or "").strip()
        if not description:
            return JsonResponse({"error": "Descripción requerida"}, status=400)
        if len(description) > 2000:
            return JsonResponse({"error": "Descripción demasiado larga"}, status=400)

        log = SCPActorLog.objects.create(
            scp=scp,
            character=scp.actor_character,
            performed_by=request.user,
            action=SCPActorLog.Action.RP_ACTION,
            description=description,
        )
        return JsonResponse({"success": True, "id": log.id}, status=201)

    can_read = (
        is_actor
        or request.user.is_superuser
        or request.user.has_permission("supervise_actors_basic")
        or scp.can_user_edit(request.user)[0]
    )
    if not can_read:
        return JsonResponse({"error": "Sin permisos"}, status=403)

    logs = scp.actor_logs.select_related("character", "performed_by")[:100]
    return JsonResponse(
        {
            "is_actor": is_actor,
            "logs": [
                {
                    "id": log.id,
                    "action": log.action,
                    "action_display": log.get_action_display(),
                    "description": log.description,
                    "character": log.character.codename if log.character else None,
                    "performed_by": log.performed_by.roblox_username
                    if log.performed_by
                    else None,
                    "details": log.details,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ],
        }
    )


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
            # Sin esto el frontend no tenía forma de saber si mostrar el botón
            # de editar, así que la edición de documentos no existía en la UI.
            "can_edit": _user_can_edit_document(user, doc),
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
        }
    )


def _user_can_edit_document(user, doc) -> bool:
    """
    Quién puede editar un documento ya publicado (spec §5.3).

    RAISA / Beta-1 / AD y el Consejo O5 editan cualquiera; el Scientific
    Department solo procedimientos y reglamentos; el autor, lo suyo.
    """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if doc.author_id == user.id:
        return True

    card = user.get_highest_access_card()
    if not card:
        return False
    if card.can_edit_any or card.can_edit_o5:
        return True
    if card.can_edit_scd:
        return doc.doc_type in (
            Document.DocType.PROCEDURE,
            Document.DocType.REGULATION,
        )
    return False


@login_required
def document_edit(request, slug):
    """Editar un documento"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        doc = Document.objects.get(slug=slug)
    except Document.DoesNotExist:
        return JsonResponse({"error": "Documento no encontrado"}, status=404)

    if not _user_can_edit_document(request.user, doc):
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


@login_required
@require_http_methods(["GET"])
def document_history(request, slug):
    """
    Versionado de un documento. DocumentEditLog se escribía en cada edición
    pero no había forma de leerlo: el historial existía y era invisible.
    """
    try:
        doc = Document.objects.get(slug=slug)
    except Document.DoesNotExist:
        return JsonResponse({"error": "Documento no encontrado"}, status=404)

    if not (doc.can_user_view(request.user) and _user_can_edit_document(request.user, doc)):
        return JsonResponse({"error": "Sin permisos"}, status=403)

    logs = doc.edit_logs.select_related("edited_by")[:50]
    return JsonResponse(
        {
            "history": [
                {
                    "id": log.id,
                    "edited_by": log.edited_by.roblox_username
                    if log.edited_by
                    else None,
                    "edit_summary": log.edit_summary,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ]
        }
    )


@login_required
def scp_create(request):
    """Crear un nuevo archivo SCP. Solo Admins o tarjetas con edición total (spec §3.1)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    card = request.user.get_highest_access_card()
    if not (request.user.is_superuser or (card and card.can_edit_any)):
        return JsonResponse({"error": "Sin permisos para crear archivos SCP"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    scp_id = (data.get("scp_id") or "").strip()
    title = (data.get("title") or "").strip()

    if not scp_id or not title:
        return JsonResponse({"error": "scp_id y title son requeridos"}, status=400)

    if SCP.objects.filter(scp_id__iexact=scp_id).exists():
        return JsonResponse({"error": "Ya existe un SCP con ese ID"}, status=400)

    scp = SCP.objects.create(
        scp_id=scp_id,
        title=title,
        object_class=data.get("object_class", SCP.ObjectClass.EUCLID),
        content_l1=data.get("content_l1", ""),
        content_l2=data.get("content_l2", ""),
        content_l3=data.get("content_l3", ""),
        content_l4=data.get("content_l4", ""),
        content_l5=data.get("content_l5", ""),
        content_l6=data.get("content_l6", ""),
        created_by=request.user,
    )

    return JsonResponse({"success": True, "id": scp.id, "scp_id": scp.scp_id})


@login_required
def scp_add_appendix(request, scp_id):
    """Agregar un apéndice a un SCP (ScD y superiores, spec §3.3)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        scp = SCP.objects.get(id=scp_id, is_active=True, is_deleted=False)
    except SCP.DoesNotExist:
        return JsonResponse({"error": "SCP no encontrado"}, status=404)

    can_add, reason = scp.can_user_add_appendix(request.user)
    if not can_add:
        return JsonResponse({"error": reason}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    level = (data.get("level") or "L1").upper()

    if not title or not content:
        return JsonResponse({"error": "Título y contenido requeridos"}, status=400)

    if level not in ("L1", "L2", "L3", "L4", "L5", "L6"):
        return JsonResponse({"error": "Nivel inválido"}, status=400)

    from django.utils import timezone

    appendices = list(scp.appendices or [])
    appendices.append(
        {
            "title": title,
            "content": content,
            "level": level,
            "author": request.user.roblox_username,
            "created_at": timezone.now().isoformat(),
        }
    )
    scp.appendices = appendices
    scp.save(update_fields=["appendices", "updated_at"])

    SCPEditLog.objects.create(
        scp=scp,
        edited_by=request.user,
        section="appendix",
        old_content="",
        new_content=f"{title}: {content}",
        edit_reason=data.get("reason", ""),
    )

    _log_actor_action(
        scp,
        request.user,
        SCPActorLog.Action.APPENDIX_ADDED,
        description=f"El actor agregó el apéndice «{title}».",
        title=title,
        level=level,
    )

    return JsonResponse({"success": True, "message": "Apéndice agregado"})


def scp_history(request, scp_id):
    """Versionado interno del SCP (spec §3.1)."""
    try:
        scp = SCP.objects.get(id=scp_id)
    except SCP.DoesNotExist:
        return JsonResponse({"error": "SCP no encontrado"}, status=404)

    can_edit, _ = scp.can_user_edit(request.user)
    if not (can_edit or request.user.is_superuser):
        return JsonResponse({"error": "Sin permisos"}, status=403)

    logs = scp.edit_logs.select_related("edited_by")[:50]
    return JsonResponse(
        {
            "history": [
                {
                    "id": log.id,
                    "section": log.section,
                    "edited_by": log.edited_by.roblox_username
                    if log.edited_by
                    else None,
                    "edit_reason": log.edit_reason,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ]
        }
    )


def _user_can_create_documents(user) -> bool:
    """Autorizados para redactar documentación (spec §5.2)."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True

    card = user.get_highest_access_card()
    if card and (card.can_edit_any or card.can_edit_o5 or card.can_edit_scd):
        return True

    # Altos cargos de otras facciones: rango con permisos de gestión
    from factions.models import CharacterFactionMembership

    return CharacterFactionMembership.objects.filter(
        character__owner=user,
        status=CharacterFactionMembership.Status.ACTIVE,
        rank__can_manage_members=True,
    ).exists()


@login_required
def document_create(request):
    """Crear un documento (spec §5.2/§5.3)."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not _user_can_create_documents(request.user):
        return JsonResponse({"error": "Sin permisos para crear documentos"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return JsonResponse({"error": "Título y contenido requeridos"}, status=400)

    min_level = (data.get("min_access_level") or "L1").upper()
    if min_level not in ("L1", "L2", "L3", "L4", "L5", "L6"):
        return JsonResponse({"error": "Nivel inválido"}, status=400)

    # El autor no puede publicar por encima de su propio nivel
    card = request.user.get_highest_access_card()
    author_level = 6 if request.user.is_superuser else (card.level_number if card else 1)
    from factions.models import LEVEL_ORDER

    if LEVEL_ORDER.get(min_level, 1) > author_level:
        return JsonResponse(
            {"error": "No puedes publicar por encima de tu nivel de acceso"}, status=403
        )

    from django.utils.text import slugify

    base_slug = slugify(title)[:180] or "documento"
    slug = base_slug
    n = 2
    while Document.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{n}"
        n += 1

    factions = request.user.get_visible_factions()
    author_faction = factions[0]["name"] if factions else ""

    doc = Document.objects.create(
        title=title,
        slug=slug,
        doc_type=data.get("doc_type", Document.DocType.OTHER),
        content=content,
        min_access_level=min_level,
        author=request.user,
        author_faction=author_faction,
    )

    return JsonResponse({"success": True, "id": doc.id, "slug": doc.slug})
