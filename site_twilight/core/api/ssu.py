from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
import json

from core.models import SiteState, SSUToggleLog
from users.models import StaffRole
from users.permissions import STAFF_PERMISSIONS
from core.events import emit_ssu_status_change


def check_ssu_permission(user):
    """Verificar si el usuario tiene permiso para cambiar el estado SSU"""
    if user.is_superuser:
        return True

    # Verificar si tiene el permiso específico
    if user.has_perm("users.change_ssu_status"):
        return True

    # Verificar si tiene nivel 1+ en el ámbito global
    global_roles = user.staff_roles.filter(scope="global")
    if global_roles.exists() and global_roles.first().level >= 1:
        return True

    return False


@login_required
def api_get_ssu_status(request):
    """Obtener el estado actual del SSU"""
    try:
        state = SiteState.objects.get(pk=1)
        return JsonResponse(
            {
                "ssu_status": state.ssu_status,
                "updated_at": state.updated_at.isoformat()
                if state.updated_at
                else None,
            }
        )
    except SiteState.DoesNotExist:
        # Crear estado inicial si no existe
        state = SiteState.objects.create(ssu_status=False)
        return JsonResponse(
            {"ssu_status": False, "updated_at": state.updated_at.isoformat()}
        )


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def api_toggle_ssu_status(request):
    """Cambiar el estado del SSU (solo para usuarios autorizados)"""
    try:
        # Verificar permisos
        if not check_ssu_permission(request.user):
            return JsonResponse(
                {"error": "No tienes permisos para cambiar el estado del SSU"},
                status=403,
            )

        with transaction.atomic():
            state = SiteState.objects.select_for_update().get(pk=1)
            new_status = not state.ssu_status
            old_status = state.ssu_status

            # Actualizar estado
            state.ssu_status = new_status
            state.updated_at = timezone.now()
            state.save(update_fields=["ssu_status", "updated_at"])

            # Emitir evento SSE
            emit_ssu_status_change(new_status)

            # Registrar el cambio
            SSUToggleLog.objects.create(
                user=request.user,
                action="ACTIVATED" if new_status else "DEACTIVATED",
                old_status=old_status,
                new_status=new_status,
            )

            return JsonResponse(
                {
                    "success": True,
                    "ssu_status": new_status,
                    "message": f"SSU {'activado' if new_status else 'desactivado'} correctamente",
                    "updated_at": state.updated_at.isoformat(),
                }
            )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def api_get_ssu_info(request):
    """Obtener información detallada del SSU"""
    try:
        state = SiteState.objects.get(pk=1)

        # Obtener último cambio
        last_log = SSUToggleLog.objects.filter().order_by("-created_at").first()
        last_change = None
        if last_log:
            last_change = last_log.created_at.isoformat()

        # Calcular duración actual
        current_duration = "00:00:00"
        if state.ssu_status and last_log and last_log.action == "ACTIVATED":
            duration = timezone.now() - last_log.created_at
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)
            current_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Contar cambios hoy
        today = timezone.now().date()
        changes_today = SSUToggleLog.objects.filter(created_at__date=today).count()

        # Obtener últimos 10 registros de actividad
        recent_logs = SSUToggleLog.objects.select_related("user").order_by(
            "-created_at"
        )[:10]
        activity_logs = []
        for log in recent_logs:
            activity_logs.append(
                {
                    "time": log.created_at.strftime("%H:%M:%S"),
                    "action": log.action,
                    "operator": log.user.roblox_username if log.user else "SISTEMA",
                }
            )

        return JsonResponse(
            {
                "ssu_status": state.ssu_status,
                "last_change": last_change,
                "current_duration": current_duration,
                "changes_today": changes_today,
                "current_operator": request.user.roblox_username
                if state.ssu_status
                else None,
                "activity_logs": activity_logs,
                "updated_at": state.updated_at.isoformat()
                if state.updated_at
                else None,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
