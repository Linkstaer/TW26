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


def divisions_by_character(character_ids=None):
    """
    Mapa {character_id: nombre_de_división} en dos queries.

    Antes cada llamador iteraba la tabla intermedia y hacía un
    FactionDivision.objects.filter(id=...).first() por fila: un N+1 sobre el
    listado completo de personajes, repetido en tres vistas distintas.
    """
    from factions.models import FactionDivision

    through = FactionDivision.members.through.objects
    if character_ids is not None:
        through = through.filter(character_id__in=list(character_ids))

    rows = list(through.values_list("character_id", "factiondivision_id"))
    if not rows:
        return {}

    names = dict(
        FactionDivision.objects.filter(
            id__in={division_id for _, division_id in rows}
        ).values_list("id", "name")
    )
    return {
        character_id: names[division_id]
        for character_id, division_id in rows
        if division_id in names
    }


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
    card_display = None
    card_level = None
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
            # La tarjeta delata igual que el rango: "L6 - Consejo O5" identifica
            # a la facción. Además va detrás del mismo umbral que access_level
            # (L4+ o acceso pleno), si no sería una forma de leer el clearance
            # ajeno esquivando ese gate. display_name ya aplica el enmascarado
            # L4/L5 de la spec §2.4.
            card = membership.access_card
            if card and (can_see_full or v_level >= 4):
                card_display = card.display_name
                card_level = card.level

    data = {
        "id": c.id,
        "codename": c.codename,
        "status": c.status,
        "owner_id": c.owner_id,
        "owner_username": c.owner.roblox_username,
        "faction": faction_name or c.faction,
        "faction_data": {
            "name": faction_name,
            "rank": rank_name,
            "card": card_display,
            "card_level": card_level,
        }
        if membership
        else None,
        "division": division,
        # card_level ya viene filtrado por fachada y por clearance.
        "access_level": card_level,
        # Integración con SCP (spec §3.4): si el personaje es Actor SCP, su
        # archivo aparece en el perfil. Va detrás del mismo gate que el resto
        # de la identidad —saber quién interpreta a un SCP es información de
        # contención, no de dominio público.
        "scp_actor": c.get_scp_actor_data()
        if (is_owner or is_moderator or access["full_access"])
        else None,
        "is_scp_actor": c.is_scp_actor,
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
                "photo_url": c.photo_url,
                "lore": lore,
                "lore_censored_by_owner": has_censorship,
                "lore_censorship_revealed": has_censorship
                and censor_mode in ("raw", "reveal"),
            }
        )
    else:
        redacted += [
            "first_name",
            "last_name",
            "country",
            "birth_date",
            "age",
            "lore",
        ]
        # La cara es identidad: si no podés leer el nombre, tampoco la foto.
        if c.photo_url:
            redacted.append("photo_url")
        data.update(
            {
                "first_name": None,
                "last_name": None,
                "country": None,
                "birth_date": None,
                "age": None,
                "photo_url": None,
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

    if membership and membership.access_card and card_level is None:
        redacted.append("access_level")

    data["redacted"] = redacted
    # Nivel que haría falta para leer lo tapado.
    data["redaction_required_level"] = c.get_access_level() if redacted else None

    return data


@login_required
@require_http_methods(["GET"])
def character_list_all(request):
    """
    Database de IDs (spec §4).

    Búsqueda por nombre / codename / usuario (§4.3) y filtros avanzados por
    facción, nivel de tarjeta, estado y condición de Actor SCP.
    """
    from factions.models import CharacterFactionMembership, Faction

    search_query = request.GET.get("search", "")
    faction_filter = request.GET.get("faction", "")
    level_filter = (request.GET.get("level", "") or "").upper()
    status_filter = request.GET.get("status", "")
    actor_filter = request.GET.get("actor", "")

    characters = (
        Character.objects.select_related("owner", "scp_file").all().order_by("codename")
    )

    if search_query:
        characters = characters.filter(
            Q(codename__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(owner__roblox_username__icontains=search_query)
        )

    if status_filter in dict(Character.Status.choices):
        characters = characters.filter(status=status_filter)

    if actor_filter in ("true", "1"):
        characters = characters.filter(scp_file__isnull=False)
    elif actor_filter in ("false", "0"):
        characters = characters.filter(scp_file__isnull=True)

    # El filtro por facción acepta el id real o el nombre visible. Se resuelve
    # sobre las facciones que el viewer puede identificar: filtrar por el
    # nombre real de una facción clasificada sería una forma de confirmar la
    # fachada sin tener el nivel para verla.
    #
    # Primero se resuelven las FACCIONES que matchean (decenas) y recién
    # después se filtran los personajes con una subconsulta. Hacerlo al revés
    # —juntar ids de personaje en Python y pasarlos como id__in— genera un IN
    # sin cota: Postgres corta en 65535 parámetros por consulta.
    if faction_filter:
        matching_factions = [
            faction.id
            for faction in Faction.objects.all()
            if str(faction.id) == faction_filter
            or faction.get_visible_name(request.user).lower()
            == faction_filter.lower()
        ]
        characters = characters.filter(
            id__in=CharacterFactionMembership.objects.filter(
                status=CharacterFactionMembership.Status.ACTIVE,
                faction_id__in=matching_factions,
            ).values("character_id")
        )

    characters = list(characters)
    character_ids = [c.id for c in characters]

    # Membresías activas (con facción para fachadas)
    memberships = CharacterFactionMembership.objects.filter(
        character_id__in=character_ids,
        status=CharacterFactionMembership.Status.ACTIVE,
    ).select_related("faction", "rank", "access_card")
    membership_by_char = {m.character_id: m for m in memberships}

    division_by_char = divisions_by_character(character_ids)

    access = _viewer_access(request.user)

    results = []
    for c in characters:
        membership = membership_by_char.get(c.id)
        if level_filter in LEVEL_ORDER:
            card = membership.access_card if membership else None
            if (card.level if card else "L1") != level_filter:
                continue
        data = _serialize_character(
            c,
            request.user,
            access,
            membership=membership,
            division=division_by_char.get(c.id),
        )
        if data is not None:
            results.append(data)

    return JsonResponse({"results": results, "count": len(results)})


@login_required
@require_http_methods(["GET"])
def character_list_user(request):
    from factions.models import CharacterFactionMembership

    search_query = request.GET.get("search", "")

    characters = (
        Character.objects.filter(owner=request.user)
        .select_related("owner", "scp_file")
        .order_by("codename")
    )

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
    division_by_char = divisions_by_character([c.id for c in characters])

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
                    "photo_url": c.photo_url,
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
                    # El dueño siempre ve su propio archivo de Actor SCP (§3.4)
                    "scp_actor": c.get_scp_actor_data(),
                    "is_scp_actor": c.is_scp_actor,
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

    character = get_object_or_404(
        Character.objects.select_related("owner", "scp_file"), pk=pk
    )

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
