import json
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

    # Obtener membresías activas
    memberships = CharacterFactionMembership.objects.filter(
        status=CharacterFactionMembership.Status.ACTIVE
    ).select_related("faction")

    membership_by_char = {m.character_id: m for m in memberships}

    # Obtener membresías de división
    from factions.models import FactionDivision

    division_memberships = FactionDivision.members.through.objects.all()
    division_by_char = {}
    for dm in division_memberships:
        division = FactionDivision.objects.filter(id=dm.factiondivision_id).first()
        if division:
            division_by_char[dm.character_id] = division.name

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
                    "owner_id": c.owner_id,
                    "owner_username": c.owner.roblox_username,
                    "faction": c.faction,
                    "faction_data": {
                        "name": membership_by_char.get(c.id).faction.display_name
                        if membership_by_char.get(c.id)
                        else None,
                        "rank": membership_by_char.get(c.id).rank.name
                        if membership_by_char.get(c.id)
                        and membership_by_char.get(c.id).rank
                        else None,
                    }
                    if membership_by_char.get(c.id)
                    else None,
                    "division": division_by_char.get(c.id),
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
def character_list_user(request):
    search_query = request.GET.get("search", "")

    characters = Character.objects.filter(owner=request.user).order_by("codename")

    if search_query:
        characters = characters.filter(
            Q(codename__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

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
                    "faction": c.faction,
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
    character = get_object_or_404(Character, pk=pk)

    return JsonResponse(
        {
            "id": character.id,
            "first_name": character.first_name,
            "last_name": character.last_name,
            "country": character.country,
            "birth_date": character.birth_date.strftime("%Y-%m-%d")
            if character.birth_date
            else None,
            "age": _calculate_age(character.birth_date)
            if character.birth_date
            else None,
            "codename": character.codename,
            "faction": character.faction,
            "lore": character.lore,
            "owner_id": character.owner_id,
            "owner_roblox_id": character.owner.roblox_id,
            "owner_username": character.owner.roblox_username,
            # Morph data
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
            "morph_command": character.morph_command(),
            "created_at": character.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


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
