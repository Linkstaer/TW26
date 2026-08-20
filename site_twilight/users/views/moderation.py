from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from users.decorators import require_staff_permission, log_action
from users.models import User, Warn, Ban, AuditLog
from characters.models import Character
from django.utils import timezone



# ==================== DASHBOARD & LISTS ====================

@require_staff_permission("access_moderation_dashboard")
def api_moderation_dashboard(request):
    """Dashboard principal de moderación"""
    # Stats
    total_warns = Warn.objects.count()
    active_warns = Warn.objects.filter(status=Warn.WarnStatus.ACTIVE).count()
    pending_appeals = Warn.objects.filter(appealed=True, appeal_response="").count()
    active_bans = Ban.objects.filter(is_active=True).count()
    
    # Usuarios con más warns
    top_warned_users = User.objects.filter(warning_count__gt=0).order_by('-warning_count')[:10]
    
    return JsonResponse({
        "stats": {
            "total_warns": total_warns,
            "active_warns": active_warns,
            "pending_appeals": pending_appeals,
            "active_bans": active_bans,
        },
        "top_warned_users": [
            {
                "roblox_username": user.roblox_username,
                "roblox_id": user.roblox_id,
                "warning_count": user.warning_count,
                "is_banned": user.is_banned
            }
            for user in top_warned_users
        ]
    })


@require_staff_permission("access_moderation_dashboard")
def api_list_warns(request):
    """Lista todos los warns con filtros"""

    """Lista todos los warns con filtros"""
    # Debug: Check user permissions
    print(f"User: {request.user}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    print(f"Is staff: {request.user.is_staff}")
    print(f"Is superuser: {request.user.is_superuser}")
    
    # Filtros
    status = request.GET.get('status', 'all')
    target_id = request.GET.get('target_id')
    moderator_id = request.GET.get('moderator_id')
    
    warns = Warn.objects.select_related('target', 'created_by', 'appealed_by')
    
    # Aplicar filtros
    if status != 'all':
        warns = warns.filter(status=status)
    
    if target_id:
        warns = warns.filter(target__roblox_id=target_id)
    
    if moderator_id:
        warns = warns.filter(created_by__roblox_id=moderator_id)
    
    # Ordenar
    sort = request.GET.get('sort', '-created_at')
    warns = warns.order_by(sort)
    
    data = []
    for warn in warns:
        data.append({
            "id": warn.id,
            "target": {
                "roblox_username": warn.target.roblox_username,
                "roblox_id": warn.target.roblox_id,
                "id": warn.target.id,
            },
            "created_by": {
                "roblox_username": warn.created_by.roblox_username if warn.created_by else None,
                "roblox_id": warn.created_by.roblox_id if warn.created_by else None,
            },
            "reason": warn.reason,
            "evidence": warn.evidence,
            "created_at": warn.created_at.isoformat(),
            "appealed": warn.appealed,
            "appealed_at": warn.appealed_at.isoformat() if warn.appealed_at else None,
            "appealed_by": warn.appealed_by.roblox_username if warn.appealed_by else None,
            "appeal_response": warn.appeal_response,
            "appeal_responded_at": warn.appeal_responded_at.isoformat() if warn.appeal_responded_at else None,
            "expires_at": warn.expires_at.isoformat() if warn.expires_at else None,
            "severity": warn.severity,
            "status": warn.status,
            "is_active": warn.is_active,
        })
    
    return JsonResponse({"warns": data})


@require_staff_permission("access_moderation_dashboard")
def api_list_bans(request):
    """Lista todos los bans"""
    bans = Ban.objects.select_related('target', 'created_by', 'revoked_by').filter(is_active=True)
    
    data = []
    for ban in bans:
        data.append({
            "id": ban.id,
            "target": {
                "roblox_username": ban.target.roblox_username,
                "roblox_id": ban.target.roblox_id,
            },
            "created_by": ban.created_by.roblox_username if ban.created_by else None,
            "reason": ban.reason,
            "evidence": ban.evidence,
            "created_at": ban.created_at.isoformat(),
            "ban_type": ban.ban_type,
            "duration_days": ban.duration_days,
            "ends_at": ban.ends_at.isoformat() if ban.ends_at else None,
            "can_appeal": ban.can_appeal,
            "appealed": ban.appealed,
            "is_permanent": ban.is_permanent,
        })
    
    return JsonResponse({"bans": data})


# ==================== WARN OPERATIONS ====================

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("create_warn")
@log_action("warn_created")
def api_create_warn(request):
    """Crea un nuevo warn"""
    try:
        print(f"DEBUG: Creating warn - User: {request.user.roblox_username}")
        print(f"DEBUG: Request body: {request.body}")
        
        data = json.loads(request.body)
        print(f"DEBUG: Parsed data: {data}")
        
        target_id = data.get('target_id')
        reason = data.get('reason', '')
        evidence = data.get('evidence', '')
        severity = int(data.get('severity', 1))
        expires_after_days = int(data.get('expires_after_days', 30))
        
        print(f"DEBUG: Target ID: {target_id}")
        print(f"DEBUG: Reason: {reason}")
        print(f"DEBUG: Severity: {severity}")
        print(f"DEBUG: Expires after days: {expires_after_days}")
        
        if not target_id:
            print("ERROR: target_id is required")
            return JsonResponse({"error": "target_id is required"}, status=400)
        
        print(f"DEBUG: Looking for user with roblox_id: {target_id}")
        target = get_object_or_404(User, roblox_id=target_id)
        print(f"DEBUG: Found target user: {target.roblox_username}")
        
        print("DEBUG: Creating warn object...")
        warn = Warn.objects.create(
            target=target,
            created_by=request.user,
            reason=reason,
            evidence=evidence,
            severity=severity,
            expires_after_days=expires_after_days
        )
        
        print(f"DEBUG: Warn created successfully with ID: {warn.id}")
        
        # Registrar en audit log (también manejado por el decorador)
        AuditLog.log_action(
            request=request,
            action_type="warn_created",
            target_user=target,
            target_warn=warn,
            details={
                "warn_id": warn.id,
                "reason": reason,
                "severity": severity,
                "expires_after_days": expires_after_days,
                "moderator": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "warn_id": warn.id,
            "message": f"Warn created for {target.roblox_username}",
            "warning_count": target.warning_count
        })
    
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except ValueError as e:
        print(f"ERROR: Value error: {e}")
        return JsonResponse({"error": f"Invalid data: {str(e)}"}, status=400)
    except Exception as e:
        print(f"ERROR: Unexpected error in api_create_warn: {str(e)}")
        import traceback
        print(f"ERROR: Traceback: {traceback.format_exc()}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("manage_warns")
@log_action("warn_updated")
def api_update_warn(request, warn_id):
    """Actualiza un warn existente"""
    try:
        warn = get_object_or_404(Warn, id=warn_id)
        data = json.loads(request.body)
        
        old_reason = warn.reason
        old_severity = warn.severity
        
        if 'reason' in data:
            warn.reason = data['reason']
        if 'evidence' in data:
            warn.evidence = data['evidence']
        if 'severity' in data:
            warn.severity = int(data['severity'])
        if 'expires_after_days' in data:
            warn.expires_after_days = int(data['expires_after_days'])
        
        warn.save()
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="warn_updated",
            target_user=warn.target,
            target_warn=warn,
            details={
                "warn_id": warn.id,
                "old_reason": old_reason,
                "new_reason": warn.reason,
                "old_severity": old_severity,
                "new_severity": warn.severity,
                "moderator": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Warn updated"
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("manage_warns")
@log_action("warn_removed")
def api_remove_warn(request, warn_id):
    """Elimina un warn (marcar como removido)"""
    try:
        warn = get_object_or_404(Warn, id=warn_id)
        
        # Registrar antes de cambiar el estado
        AuditLog.log_action(
            request=request,
            action_type="warn_removed",
            target_user=warn.target,
            target_warn=warn,
            details={
                "warn_id": warn.id,
                "reason": warn.reason,
                "severity": warn.severity,
                "moderator": request.user.roblox_username
            }
        )
        
        warn.status = Warn.WarnStatus.REMOVED
        warn.save()
        
        warn.target.update_warning_count()
        
        return JsonResponse({
            "success": True,
            "message": "Warn removed"
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==================== APPEAL SYSTEM ====================

@csrf_exempt
@require_http_methods(["POST"])
@log_action("warn_appealed")
def api_appeal_warn(request, warn_id):
    """Usuario apela un warn con cooldown"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    try:
        warn = get_object_or_404(Warn, id=warn_id)
        
        # Verificar que el usuario es el dueño del warn
        if warn.target != request.user:
            return JsonResponse({"error": "Not your warn"}, status=403)
        
        data = json.loads(request.body)
        appeal_message = data.get('message', '')
        
        # Intentar apelar
        try:
            warn.appeal(appealed_by=request.user, appeal_message=appeal_message)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="warn_appealed",
            action_user=request.user,
            target_user=warn.target,
            target_warn=warn,
            details={
                "warn_id": warn.id,
                "appeal_message": appeal_message,
                "user": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Appeal submitted",
            "cooldown_info": request.user.get_appeal_cooldown()
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("manage_warns")
@log_action("warn_appeal_responded")
def api_respond_appeal(request, warn_id):
    """Moderador responde a una apelación"""
    try:
        warn = get_object_or_404(Warn, id=warn_id)
        
        if not warn.appealed:
            return JsonResponse({"error": "Warn not appealed"}, status=400)
        
        data = json.loads(request.body)
        response = data.get('response', '')
        
        warn.respond_to_appeal(response, request.user)
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="warn_appeal_responded",
            target_user=warn.target,
            target_warn=warn,
            details={
                "warn_id": warn.id,
                "appeal_response": response,
                "moderator": request.user.roblox_username,
                "appeal_accepted": "aceptado" in response.lower() or "aceptada" in response.lower()
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Appeal response saved"
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==================== BAN OPERATIONS ====================

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("register_ban")
@log_action("ban_created")
def api_create_ban(request):
    """Crea un nuevo ban"""
    try:
        data = json.loads(request.body)
        
        target_id = data.get('target_id')
        reason = data.get('reason', '')
        evidence = data.get('evidence', '')
        ban_type = data.get('ban_type', 'temporary')
        duration_days = data.get('duration_days')
        can_appeal = data.get('can_appeal', True)
        
        if not target_id:
            return JsonResponse({"error": "target_id is required"}, status=400)
        
        target = get_object_or_404(User, roblox_id=target_id)
        
        # Verificar que no sea staff
        if target.has_permission("register_ban") or target.is_staff:
            return JsonResponse({"error": "Cannot ban staff members"}, status=403)
        
        # Verificar que no esté ya baneado
        if target.is_banned:
            return JsonResponse({"error": "User already banned"}, status=400)
        
        ban = Ban.objects.create(
            target=target,
            created_by=request.user,
            reason=reason,
            evidence=evidence,
            ban_type=ban_type,
            duration_days=duration_days if ban_type == 'temporary' else None,
            can_appeal=can_appeal
        )
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="ban_created",
            target_user=target,
            target_ban=ban,
            details={
                "ban_id": ban.id,
                "reason": reason,
                "ban_type": ban_type,
                "duration_days": duration_days,
                "moderator": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "ban_id": ban.id,
            "message": f"Ban created for {target.roblox_username}",
            "ends_at": ban.ends_at.isoformat() if ban.ends_at else None
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("register_ban")
@log_action("ban_revoked")
def api_revoke_ban(request, ban_id):
    """Revoca un ban activo"""
    try:
        ban = get_object_or_404(Ban, id=ban_id)
        
        if not ban.is_active:
            return JsonResponse({"error": "Ban not active"}, status=400)
        
        data = json.loads(request.body)
        reason = data.get('reason', '')
        
        ban.revoke(request.user, reason)
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="ban_revoked",
            target_user=ban.target,
            target_ban=ban,
            details={
                "ban_id": ban.id,
                "revocation_reason": reason,
                "moderator": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Ban revoked"
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==================== USER SPECIFIC ====================

@require_staff_permission("access_moderation_dashboard")
def api_get_user_moderation_info(request, roblox_id):
    """Obtiene información de moderación de un usuario específico"""
    try:
        user = get_object_or_404(User, roblox_id=roblox_id)
        
        # Warns activos y recientes
        active_warns = user.warns.filter(status=Warn.WarnStatus.ACTIVE)
        recent_warns = user.warns.all().order_by('-created_at')[:10]
        
        # Bans activos y anteriores
        active_bans = user.bans_received.filter(is_active=True)
        past_bans = user.bans_received.filter(is_active=False)
        
        return JsonResponse({
            "user": {
                "roblox_username": user.roblox_username,
                "roblox_id": user.roblox_id,
                "warning_count": user.warning_count,
                "is_banned": user.is_banned,
                "ban_reason": user.ban_reason,
                "banned_until": user.banned_until.isoformat() if user.banned_until else None,
            },
            "active_warns": [
                {
                    "id": w.id,
                    "reason": w.reason,
                    "created_at": w.created_at.isoformat(),
                    "expires_at": w.expires_at.isoformat() if w.expires_at else None,
                    "severity": w.severity,
                }
                for w in active_warns
            ],
            "recent_warns": [
                {
                    "id": w.id,
                    "reason": w.reason,
                    "created_at": w.created_at.isoformat(),
                    "status": w.status,
                    "appealed": w.appealed,
                }
                for w in recent_warns
            ],
            "active_bans": [
                {
                    "id": b.id,
                    "reason": b.reason,
                    "ban_type": b.ban_type,
                    "ends_at": b.ends_at.isoformat() if b.ends_at else None,
                    "created_at": b.created_at.isoformat(),
                }
                for b in active_bans
            ],
            "ban_history": [
                {
                    "id": b.id,
                    "reason": b.reason,
                    "ban_type": b.ban_type,
                    "created_at": b.created_at.isoformat(),
                    "revoked_at": b.revoked_at.isoformat() if b.revoked_at else None,
                    "was_active": b.is_active,
                }
                for b in past_bans
            ]
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==================== CHARACTER MODERATION ====================

@require_staff_permission("view_characters_basic")
def api_characters_for_moderation(request):
    """Lista personajes para moderación"""
    characters = (
        Character.objects
        .select_related("owner", "faction", "access_card")
        .all()
    )

    data = [
        {
            "id": c.id,
            "user": {
                "username": c.owner.roblox_username,
                "id": c.owner.roblox_id,
                "warning_count": c.owner.warning_count,
                "is_banned": c.owner.is_banned,
            },
            "character": {
                "name": c.display_name,
                "codename": c.codename,
                "faction": c.faction.display_name if c.faction else None,
                "status": c.status,
            }
        }
        for c in characters
    ]

    return JsonResponse({"characters": data})

def api_search_users(request, query):
    """Buscar usuarios por ID o username"""
    try:
        print(f"DEBUG: Searching for user with query: {query}")
        
        # Intentar buscar por ID primero
        if query.isdigit():
            users = User.objects.filter(roblox_id=int(query))
        else:
            # Buscar por username (case insensitive)
            users = User.objects.filter(
                Q(roblox_username__icontains=query)
            )
        
        users = users.order_by('roblox_username')[:10]  # Limitar a 10 resultados
        
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'roblox_username': user.roblox_username,
                'roblox_id': user.roblox_id,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'warning_count': user.warning_count,
                'is_banned': user.is_banned,
                'first_login': user.first_login.isoformat() if user.first_login else None,
            })
        
        print(f"DEBUG: Found {len(data)} users")
        if data:
            print(f"DEBUG: First user: {data[0]}")
        
        return JsonResponse({
            'results': data,
            'count': len(data)
        })
        
    except Exception as e:
        print(f"ERROR in api_search_users: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def api_get_user_appeals(request):
    """Obtiene todas las apelaciones del usuario actual"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    try:
        user = request.user
        
        # Debug log
        print(f"DEBUG: Getting appeals for user {user.roblox_username} ({user.id})")
        
        # 1. Obtener TODOS los warns del usuario que estén apelados
        appealed_warns = Warn.objects.filter(
            target=user,
            appealed=True
        ).order_by('-appealed_at')
        
        print(f"DEBUG: Found {appealed_warns.count()} appealed warns")
        
        # 2. Obtener TODOS los bans del usuario que estén apelados
        appealed_bans = Ban.objects.filter(
            target=user,
            appealed=True
        ).order_by('-appealed_at')
        
        print(f"DEBUG: Found {appealed_bans.count()} appealed bans")
        
        # 3. Obtener warns que PUEDEN ser apelados (no apelados aún)
        appealable_warns = Warn.objects.filter(
            target=user,
            appealed=False,
            status=Warn.WarnStatus.ACTIVE
        ).order_by('-created_at')
        
        print(f"DEBUG: Found {appealable_warns.count()} appealable warns")
        
        # 4. Obtener bans que PUEDEN ser apelados (no apelados aún)
        appealable_bans = Ban.objects.filter(
            target=user,
            appealed=False,
            is_active=True,
            can_appeal=True
        ).order_by('-created_at')
        
        print(f"DEBUG: Found {appealable_bans.count()} appealable bans")
        
        # Formatear warns apelados (para historial)
        appealed_warnings_data = []
        for warn in appealed_warns:
            responded_by_name = None
            if warn.appeal_responded_by_id:
                try:
                    responded_by = User.objects.get(id=warn.appeal_responded_by_id)
                    responded_by_name = responded_by.roblox_username
                except User.DoesNotExist:
                    responded_by_name = None

            appeal_response_lower = warn.appeal_response.lower() if warn.appeal_response else ""
            accepted_keywords = ['aceptado', 'aceptada', 'aprobado', 'aprobada', 'acepto', 'acepta']
            rejected_keywords = ['rechazado', 'rechazada', 'denegado', 'denegada', 'rechazo', 'rechaza']
            
            is_accepted = any(keyword in appeal_response_lower for keyword in accepted_keywords)
            is_rejected = any(keyword in appeal_response_lower for keyword in rejected_keywords)
            
            # Si el warn fue removido, fue aceptado
            if warn.status == Warn.WarnStatus.REMOVED:
                is_accepted = True
                is_rejected = False
            
            appeal_status = "pending"
            if warn.appeal_response:
                if is_accepted:
                    appeal_status = "approved"
                elif is_rejected:
                    appeal_status = "rejected"
                else:
                    appeal_status = "responded"  # Respondida pero sin decisión clara
            
            appealed_warnings_data.append({
                "id": warn.id,
                "type": "warning",
                "reason": warn.reason,
                "evidence": warn.evidence,
                "severity": warn.severity,
                "created_at": warn.created_at.isoformat() if warn.created_at else None,
                "appealed_at": warn.appealed_at.isoformat() if warn.appealed_at else None,
                "appeal_message": warn.appeal_message or "Apelación presentada",
                "appeal_response": warn.appeal_response,
                "appeal_responded_at": warn.appeal_responded_at.isoformat() if warn.appeal_responded_at else None,
                "appeal_responded_by": responded_by_name,
                "status": warn.status,
                "appeal_status": appeal_status,  # Nuevo campo para estado de apelación
                "expires_at": warn.expires_at.isoformat() if warn.expires_at else None,
                "is_resolved": bool(warn.appeal_response),
                "resolved_at": warn.appeal_responded_at.isoformat() if warn.appeal_responded_at else None,
                "can_appeal_again": False
            })
        
        # Formatear bans apelados (para historial)
        appealed_bans_data = []
        for ban in appealed_bans:
            responded_by_name = None
            if ban.appeal_responded_by_id:
                try:
                    responded_by = User.objects.get(id=ban.appeal_responded_by_id)
                    responded_by_name = responded_by.roblox_username
                except User.DoesNotExist:
                    responded_by_name = None
            
            appealed_bans_data.append({
                "id": ban.id,
                "type": "ban",
                "reason": ban.reason,
                "evidence": ban.evidence,
                "ban_type": ban.ban_type,
                "created_at": ban.created_at.isoformat() if ban.created_at else None,
                "appealed_at": ban.appealed_at.isoformat() if ban.appealed_at else None,
                "appeal_message": ban.appeal_message or "Apelación presentada",
                "appeal_response": ban.appeal_response,
                "appeal_responded_at": ban.appeal_responded_at.isoformat() if ban.appeal_responded_at else None,
                "appeal_responded_by": responded_by_name,
                "status": "active" if ban.is_active else "revoked",
                "ends_at": ban.ends_at.isoformat() if ban.ends_at else None,
                "is_resolved": bool(ban.appeal_response),  # Resuelto si tiene respuesta
                "resolved_at": ban.appeal_responded_at.isoformat() if ban.appeal_responded_at else None,
                "can_appeal": ban.can_appeal,
                "can_appeal_again": False  # Ya apelado
            })
        
        # Formatear warns apelables (para sección de apelar)
        appealable_warnings_data = []
        for warn in appealable_warns:
            can_appeal, reason = warn.can_be_appealed()
            appealable_warnings_data.append({
                "id": warn.id,
                "type": "warning",
                "reason": warn.reason,
                "evidence": warn.evidence,
                "severity": warn.severity,
                "created_at": warn.created_at.isoformat() if warn.created_at else None,
                "expires_at": warn.expires_at.isoformat() if warn.expires_at else None,
                "can_appeal": can_appeal,
                "cannot_appeal_reason": reason if not can_appeal else None,
                "status": warn.status
            })
        
        # Formatear bans apelables (para sección de apelar)
        appealable_bans_data = []
        for ban in appealable_bans:
            can_appeal, reason = ban.can_be_appealed()
            appealable_bans_data.append({
                "id": ban.id,
                "type": "ban",
                "reason": ban.reason,
                "evidence": ban.evidence,
                "ban_type": ban.ban_type,
                "created_at": ban.created_at.isoformat() if ban.created_at else None,
                "ends_at": ban.ends_at.isoformat() if ban.ends_at else None,
                "can_appeal": can_appeal,
                "cannot_appeal_reason": reason if not can_appeal else None,
                "status": "active" if ban.is_active else "revoked"
            })
        
        # Obtener cooldown del usuario
        cooldown_info = user.get_appeal_cooldown()
        
        print(f"DEBUG: Cooldown info: {cooldown_info}")
        
        return JsonResponse({
            "appealed_warnings": appealed_warnings_data,      # Apelados (historial)
            "appealed_bans": appealed_bans_data,              # Apelados (historial)
            "appealable_warnings": appealable_warnings_data,  # Por apelar
            "appealable_bans": appealable_bans_data,          # Por apelar
            "appeal_cooldown": cooldown_info
        })
    
    except Exception as e:
        print(f"ERROR en api_get_user_appeals: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({"error": str(e)}, status=500)

# ==================== BAN APPEAL SYSTEM ====================

@csrf_exempt
@require_http_methods(["POST"])
@log_action("ban_appealed")
def api_appeal_ban(request, ban_id):
    """Usuario apela un ban"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    try:
        ban = get_object_or_404(Ban, id=ban_id)
        
        # Verificar que el usuario es el dueño del ban
        if ban.target != request.user:
            return JsonResponse({"error": "Not your ban"}, status=403)
        
        data = json.loads(request.body)
        appeal_message = data.get('message', '')
        
        # Intentar apelar
        try:
            ban.appeal(appealed_by=request.user, appeal_message=appeal_message)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="ban_appealed",
            action_user=request.user,
            target_user=ban.target,
            target_ban=ban,
            details={
                "ban_id": ban.id,
                "appeal_message": appeal_message,
                "user": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Appeal submitted"
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("register_ban")
@log_action("ban_appeal_responded")
def api_respond_ban_appeal(request, ban_id):
    """Moderador responde a una apelación de ban"""
    try:
        ban = get_object_or_404(Ban, id=ban_id)
        
        if not ban.appealed:
            return JsonResponse({"error": "Ban not appealed"}, status=400)
        
        data = json.loads(request.body)
        response = data.get('response', '')
        
        ban.appeal_response = response
        ban.appeal_responded_by = request.user
        ban.appeal_responded_at = timezone.now()
        ban.save()
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="ban_appeal_responded",
            target_user=ban.target,
            target_ban=ban,
            details={
                "ban_id": ban.id,
                "appeal_response": response,
                "moderator": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Appeal response saved"
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)