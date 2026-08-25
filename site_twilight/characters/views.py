import json
import re
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import AuditLog
from users.decorators import log_action
from .models import Character
from .forms import CharacterForm


def _calculate_age(birth_date):
    """Función helper independiente para calcular la edad"""
    today = timezone.now().date()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


LEVEL_ORDER = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6}


# El dueño marca lo que quiere tapar de su lore encerrándolo en [[...]].
_CENSOR_RE = re.compile(r"\[\[(.+?)\]\]", re.DOTALL)
_REDACTION_CHAR = "█"


def _apply_owner_censorship(text, mode):
    """
    Aplica la censura que el dueño escribió en su lore.

    mode:
      "raw"    -> dueño: texto tal cual, con las marcas a la vista para editarlas.
                  Si se las devolviéramos limpias, al guardar perdería la censura.
      "reveal" -> moderación / L6: lee el contenido, sin los corchetes.
      "block"  -> el resto: bloques █ del largo de lo tapado.

    Devuelve (texto, hubo_censura).
    """
    if not text:
        return text, False

    if mode == "raw":
        return text, bool(_CENSOR_RE.search(text))

    found = False

    def repl(match):
        nonlocal found
        found = True
        inner = match.group(1)
        if mode == "reveal":
            return inner
        return _REDACTION_CHAR * max(3, min(len(inner), 60))

    return _CENSOR_RE.sub(repl, text), found


def _viewer_access(user):
    """Nivel de visibilidad del usuario que consulta (spec §4.2)."""
    if user.is_superuser:
        return {"level": 6, "is_ethics": True, "full_access": True}

    card = user.get_highest_access_card()
    level = card.level_number if card else 1
    is_ethics = bool(
        card and card.card_type == card.CardType.ETHICS_COMMITTEE
    )
    return {"level": level, "is_ethics": is_ethics, "full_access": level >= 6}


def _serialize_character(c, viewer, access, membership=None, division=None):
    """
    Serializa un personaje aplicando la matriz de visibilidad de §4.2:
    - Todos: solo personajes no clasificados (info básica).
    - L4/ISD: ve personajes L5 pero solo Codename + Facción.
    - L5: toda la info de L5, salvo archivos privados (morphs).
    - Comité de Ética: toda la info L5 con Codename.
    - L6 (RAISA/Admin Office): acceso completo.
    Devuelve None si el personaje no es visible para el viewer.
    """
    is_owner = viewer.is_authenticated and c.owner_id == viewer.id
    is_moderator = viewer.is_authenticated and (
        viewer.is_superuser or viewer.has_permission("view_characters_basic")
    )

    char_level = LEVEL_ORDER.get(c.get_access_level(), 1)
    # "Clasificado" es el estado del personaje (spec §4.1). La pertenencia a una
    # facción clasificada se oculta con la fachada, no escondiendo al personaje.
    is_classified_char = c.status == c.Status.CLASSIFIED

    if c.status == c.Status.DELETED and not (is_owner or is_moderator):
        return None

    v_level = access["level"]

    # Visibilidad del registro completo
    if not (is_owner or is_moderator or access["full_access"]):
        if is_classified_char and v_level < 5:
            return None
        if char_level >= 5 and v_level < 4:
            # "Todos" no puede ver L5
            return None

    # ¿Puede ver info completa (nombre real, país, nacimiento, lore)?
    can_see_full = (
        is_owner
        or is_moderator
        or access["full_access"]
        or access["is_ethics"]
        or v_level >= char_level
    )
    # L4 mirando un L5: solo Codename + Facción (spec §4.2)
    codename_only = char_level >= 5 and v_level == 4 and not (
        is_owner or is_moderator or access["is_ethics"] or access["full_access"]
    )
    if codename_only:
        can_see_full = False

    # Morph data: archivos privados — solo dueño y moderación/L6
    can_see_private = is_owner or is_moderator or access["full_access"]

    faction_name = None
    rank_name = None
    if membership:
        faction = membership.faction
        # El dueño conoce la facción de su propio personaje: mostrarle la
        # fachada ahí no oculta nada y contradice a /characters/mine/.
        if is_owner:
            faction_name = faction.display_name
        else:
            faction_name = faction.get_visible_name(
                viewer if viewer.is_authenticated else None
            )
        # Si al viewer le toca la fachada, el rango la delata: "O5-9 a O5-13"
        # identifica al Consejo O5 aunque la facción se muestre como
        # "Site Direction". La división filtra por el mismo lado.
        shows_facade = faction.is_classified and faction_name != faction.display_name
        if shows_facade:
            division = None
        else:
            rank_name = membership.rank.name if membership.rank else None

    data = {
        "id": c.id,
        "codename": c.codename,
        "status": c.status,
        "owner_id": c.owner_id,
        "owner_username": c.owner.roblox_username,
        "faction": faction_name or c.faction,
        "faction_data": {"name": faction_name, "rank": rank_name}
        if membership
        else None,
        "division": division,
        "access_level": c.get_access_level()
        if (can_see_full or v_level >= 4)
        else None,
        "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Redacción en vez de ocultamiento: los campos que el viewer no puede leer
    # viajan vacíos pero anunciados en "redacted", para que la UI muestre
    # [DATOS EXPURGADOS] en vez de un hueco. Lo que sí se sigue ocultando por
    # completo es la existencia del personaje (los return None de más arriba).
    redacted = []

    if can_see_full:
        # La censura del dueño no sirve para esconderse de moderación ni de L6.
        if is_owner:
            censor_mode = "raw"
        elif is_moderator or access["full_access"]:
            censor_mode = "reveal"
        else:
            censor_mode = "block"
        lore, has_censorship = _apply_owner_censorship(c.lore, censor_mode)

        data.update(
            {
                "first_name": c.first_name,
                "last_name": c.last_name,
                "country": c.country,
                "birth_date": c.birth_date.strftime("%Y-%m-%d")
                if c.birth_date
                else None,
                "age": _calculate_age(c.birth_date) if c.birth_date else None,
                "lore": lore,
                "lore_censored_by_owner": has_censorship,
                "lore_censorship_revealed": has_censorship
                and censor_mode in ("raw", "reveal"),
            }
        )
    else:
        redacted += ["first_name", "last_name", "country", "birth_date", "age", "lore"]
        data.update(
            {
                "first_name": None,
                "last_name": None,
                "country": None,
                "birth_date": None,
                "age": None,
                "lore": None,
                "lore_censored_by_owner": False,
                "lore_censorship_revealed": False,
            }
        )

    if can_see_private:
        data.update(
            {
                "morph": c.morph,
                "hat": c.hat,
                "nvg_color": c.nvg_color,
                "shirt": c.shirt,
                "pants": c.pants,
                "skin_r": c.skin_r,
                "skin_g": c.skin_g,
                "skin_b": c.skin_b,
                "ntag": c.ntag,
                "cntag_r": c.cntag_r,
                "cntag_g": c.cntag_g,
                "cntag_b": c.cntag_b,
                "rtag": c.rtag,
                "crtag_r": c.crtag_r,
                "crtag_g": c.crtag_g,
                "crtag_b": c.crtag_b,
                "rhat": c.rhat,
                "morph_command": c.morph_command(),
            }
        )
    else:
        redacted.append("morph")

    if data.get("access_level") is None:
        redacted.append("access_level")

    data["redacted"] = redacted
    # Nivel que haría falta para leer lo tapado.
    data["redaction_required_level"] = c.get_access_level() if redacted else None

    return data


@login_required
@require_http_methods(["GET"])
def character_list_all(request):
    from factions.models import CharacterFactionMembership, FactionDivision

    search_query = request.GET.get("search", "")

    characters = Character.objects.select_related("owner").all().order_by("codename")

    if search_query:
        characters = characters.filter(
            Q(codename__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(owner__roblox_username__icontains=search_query)
        )

    # Membresías activas (con facción para fachadas)
    memberships = CharacterFactionMembership.objects.filter(
        status=CharacterFactionMembership.Status.ACTIVE
    ).select_related("faction", "rank", "access_card")
    membership_by_char = {m.character_id: m for m in memberships}

    # Membresías de división
    division_memberships = FactionDivision.members.through.objects.all()
    division_by_char = {}
    for dm in division_memberships:
        division = FactionDivision.objects.filter(id=dm.factiondivision_id).first()
        if division:
            division_by_char[dm.character_id] = division.name

    access = _viewer_access(request.user)

    results = []
    for c in characters:
        data = _serialize_character(
            c,
            request.user,
            access,
            membership=membership_by_char.get(c.id),
            division=division_by_char.get(c.id),
        )
        if data is not None:
            results.append(data)

    return JsonResponse({"results": results})


@login_required
@require_http_methods(["GET"])
def character_list_user(request):
    from factions.models import CharacterFactionMembership, FactionDivision

    search_query = request.GET.get("search", "")

    characters = Character.objects.filter(owner=request.user).order_by("codename")

    if search_query:
        characters = characters.filter(
            Q(codename__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

    # Character.faction es un campo legacy que nadie llena: la pertenencia real
    # vive en CharacterFactionMembership. Sin esto "Mis agentes" muestra la
    # facción vacía. Al ser el dueño el que consulta, no hay fachada que aplicar.
    membership_by_char = {
        m.character_id: m
        for m in CharacterFactionMembership.objects.filter(
            character__owner=request.user,
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

    def _faction_data(c):
        m = membership_by_char.get(c.id)
        if not m:
            return None
        return {
            "name": m.faction.display_name,
            "rank": m.rank.name if m.rank else None,
        }

    return JsonResponse(
        {
            "results": [
                {
                    "id": c.id,
                    "first_name": c.first_name,
                    "last_name": c.last_name,
                    "country": c.country,
                    "birth_date": c.birth_date.strftime("%Y-%m-%d")
                    if c.birth_date
                    else None,
                    "age": _calculate_age(c.birth_date) if c.birth_date else None,
                    "codename": c.codename,
                    "faction": (_faction_data(c) or {}).get("name") or c.faction,
                    "faction_data": _faction_data(c),
                    "division": division_by_char.get(c.id),
                    "owner_id": c.owner_id,
                    "owner_username": c.owner.roblox_username,
                    "lore": c.lore,
                    "morph": c.morph,
                    "hat": c.hat,
                    "nvg_color": c.nvg_color,
                    "shirt": c.shirt,
                    "pants": c.pants,
                    "skin_r": c.skin_r,
                    "skin_g": c.skin_g,
                    "skin_b": c.skin_b,
                    "ntag": c.ntag,
                    "cntag_r": c.cntag_r,
                    "cntag_g": c.cntag_g,
                    "cntag_b": c.cntag_b,
                    "rtag": c.rtag,
                    "crtag_r": c.crtag_r,
                    "crtag_g": c.crtag_g,
                    "crtag_b": c.crtag_b,
                    "rhat": c.rhat,
                    "morph_command": c.morph_command(),
                    "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for c in characters
            ]
        }
    )


@login_required
@require_http_methods(["GET"])
def character_detail(request, pk):
    from factions.models import CharacterFactionMembership

    character = get_object_or_404(Character, pk=pk)

    membership = (
        CharacterFactionMembership.objects.filter(
            character=character, status=CharacterFactionMembership.Status.ACTIVE
        )
        .select_related("faction", "rank", "access_card")
        .first()
    )

    access = _viewer_access(request.user)
    data = _serialize_character(character, request.user, access, membership=membership)

    if data is None:
        return JsonResponse({"error": "Personaje no encontrado"}, status=404)

    data["owner_roblox_id"] = character.owner.roblox_id
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
@log_action("character_created")
def character_create(request):
    try:
        data = json.loads(request.body)

        # Preparar datos para el formulario
        form_data = data.copy()

        # Convertir campos booleanos para el formulario
        if "rhat" in form_data:
            if isinstance(form_data["rhat"], str):
                form_data["rhat"] = form_data["rhat"].lower() in ["true", "1", "yes"]

        # Manejar campos vacíos para valores numéricos
        for field in [
            "skin_r",
            "skin_g",
            "skin_b",
            "cntag_r",
            "cntag_g",
            "cntag_b",
            "crtag_r",
            "crtag_g",
            "crtag_b",
        ]:
            if field in form_data and form_data[field] == "":
                form_data[field] = None

        # Crear formulario con los datos
        form = CharacterForm(form_data)

        if form.is_valid():
            try:
                # Guardar con commit=False para poder asignar el owner
                character = form.save(commit=False)
                character.owner = request.user

                # Ejecutar validación completa del modelo
                character.full_clean()

                # Guardar en la base de datos
                character.save()

                # Registrar acción de auditoría con detalles adicionales
                AuditLog.log_action(
                    request=request,
                    action_type="character_created",
                    target_user=request.user,
                    target_character=character,
                    details={
                        "character_id": character.id,
                        "character_name": character.codename,
                        "faction": character.faction,
                        "details": "Personaje creado exitosamente",
                    },
                )

                return JsonResponse(
                    {
                        "success": True,
                        "id": character.id,
                        "morph_command": character.morph_command(),
                    },
                    status=201,
                )

            except ValidationError as e:
                # Capturar errores de validación del modelo
                error_dict = {}
                for field, errors in e.message_dict.items():
                    error_dict[field] = (
                        errors[0] if isinstance(errors, list) else errors
                    )

                return JsonResponse(
                    {"success": False, "errors": error_dict}, status=400
                )

        else:
            # Retornar errores del formulario
            errors = {}
            for field, error_list in form.errors.items():
                # Tomar solo el primer error por campo para simplificar
                errors[field] = error_list[0] if error_list else "Error desconocido"

            return JsonResponse({"success": False, "errors": errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_http_methods(["PUT"])
@log_action("character_updated")
def character_update(request, pk):
    try:
        character = get_object_or_404(Character, pk=pk)

        # Solo el owner puede editar
        if character.owner != request.user:
            return JsonResponse(
                {"error": "No tienes permiso para editar este personaje"}, status=403
            )

        data = json.loads(request.body)

        # Preparar datos para el formulario
        form_data = data.copy()

        # Si no se envía algún campo, usar el valor actual
        current_data = {
            "first_name": character.first_name,
            "last_name": character.last_name,
            "country": character.country,
            "birth_date": character.birth_date,
            "codename": character.codename,
            "faction": character.faction,
            "lore": character.lore,
            "morph": character.morph,
            "hat": character.hat,
            "nvg_color": character.nvg_color,
            "shirt": character.shirt,
            "pants": character.pants,
            "skin_r": character.skin_r,
            "skin_g": character.skin_g,
            "skin_b": character.skin_b,
            "ntag": character.ntag,
            "cntag_r": character.cntag_r,
            "cntag_g": character.cntag_g,
            "cntag_b": character.cntag_b,
            "rtag": character.rtag,
            "crtag_r": character.crtag_r,
            "crtag_g": character.crtag_g,
            "crtag_b": character.crtag_b,
            "rhat": character.rhat,
        }

        # Combinar datos actuales con nuevos datos
        for key, value in current_data.items():
            if key not in form_data:
                form_data[key] = value

        # Convertir campos booleanos para el formulario
        if "rhat" in form_data:
            if isinstance(form_data["rhat"], str):
                form_data["rhat"] = form_data["rhat"].lower() in ["true", "1", "yes"]

        # Manejar campos vacíos para valores numéricos
        for field in [
            "skin_r",
            "skin_g",
            "skin_b",
            "cntag_r",
            "cntag_g",
            "cntag_b",
            "crtag_r",
            "crtag_g",
            "crtag_b",
        ]:
            if field in form_data and form_data[field] == "":
                form_data[field] = None

        # Crear formulario con los datos y la instancia existente
        form = CharacterForm(form_data, instance=character)

        if form.is_valid():
            try:
                # Guardar con commit=False para ejecutar validación
                character = form.save(commit=False)

                # Ejecutar validación completa del modelo
                character.full_clean()

                # Guardar en la base de datos
                character.save()

                # Registrar acción de auditoría
                AuditLog.log_action(
                    request=request,
                    action_type="character_updated",
                    target_user=request.user,
                    target_character=character,
                    details={
                        "character_id": character.id,
                        "character_name": character.codename,
                        "faction": character.faction,
                        "changes": data,  # Guardar los cambios realizados
                    },
                )

                return JsonResponse(
                    {
                        "success": True,
                        "id": character.id,
                        "morph_command": character.morph_command(),
                    }
                )

            except ValidationError as e:
                # Capturar errores de validación del modelo
                error_dict = {}
                for field, errors in e.message_dict.items():
                    error_dict[field] = (
                        errors[0] if isinstance(errors, list) else errors
                    )

                return JsonResponse(
                    {"success": False, "errors": error_dict}, status=400
                )

        else:
            # Retornar errores del formulario
            errors = {}
            for field, error_list in form.errors.items():
                # Tomar solo el primer error por campo para simplificar
                errors[field] = error_list[0] if error_list else "Error desconocido"

            return JsonResponse({"success": False, "errors": errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_http_methods(["DELETE"])
@log_action("character_deleted")
def character_delete(request, pk):
    try:
        character = get_object_or_404(Character, pk=pk)

        # Solo el owner puede eliminar
        if character.owner != request.user:
            return JsonResponse(
                {"error": "No tienes permiso para eliminar este personaje"}, status=403
            )

        # Guardar información antes de eliminar para el log
        character_info = {
            "character_id": character.id,
            "character_name": character.codename,
            "faction": character.faction,
            "owner_username": character.owner.roblox_username,
        }

        character.delete()

        # Registrar acción de auditoría
        AuditLog.log_action(
            request=request,
            action_type="character_deleted",
            target_user=request.user,
            details=character_info,
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
