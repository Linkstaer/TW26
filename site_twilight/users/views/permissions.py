from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import User, StaffRole, AuditLog
from users.permissions import STAFF_PERMISSIONS
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.decorators import require_staff_permission, log_action
import json
from django.shortcuts import get_object_or_404

@login_required
def api_get_user_permissions(request):
    """Obtener todos los permisos del usuario actual"""
    user = request.user
    
    # Obtener todos los permisos del usuario
    all_permissions = set()
    
    for role in user.staff_roles.all():
        perms_by_level = STAFF_PERMISSIONS.get(role.scope, {})
        for lvl in range(1, role.level + 1):
            if lvl in perms_by_level:
                all_permissions.update(perms_by_level[lvl])
    
    # Agregar permisos de superuser
    if user.is_superuser:
        all_permissions.update([
            'full_moderation_control',
            'full_discord_moderation',
            'access_moderation_dashboard',
            'create_warn',
            'register_ban',
            'manage_warns',
            'view_characters_basic',
            'change_ssu_status',
            'edit_rp_files_basic',
            'edit_rp_files_full',
            'faction_moderation_basic',
            'faction_moderation_full',
            'supervise_actors_basic',
            'supervise_actors_full'
        ])
    
    # Agregar permisos de staff
    if user.is_staff:
        all_permissions.update([
            'access_moderation_dashboard',
            'view_characters_basic'
        ])
    
    return JsonResponse({
        'permissions': list(all_permissions),
        'scopes': [
            {
                'scope': role.scope,
                'level': role.level,
                'assigned_at': role.assigned_at.isoformat(),
                'scope_display': role.get_scope_display()
            }
            for role in user.staff_roles.all()
        ]
    })

@login_required
def api_get_current_user(request):
    """Obtener información del usuario actual"""
    user = request.user
    
    # Registrar login en audit log (solo si no es una solicitud frecuente)
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        AuditLog.log_action(
            request=request,
            action_type="user_login",
            target_user=user,
            details={
                "user": user.roblox_username,
                "action": "get_current_user"
            }
        )
    
    return JsonResponse({
        'id': user.id,
        'roblox_username': user.roblox_username,
        'roblox_id': user.roblox_id,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_authenticated': user.is_authenticated,
        'first_login': user.first_login.isoformat() if user.first_login else None,
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'warning_count': user.warning_count,
        'is_banned': user.is_banned,
    })

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("full_moderation_control")
@log_action("permissions_update")
def api_update_user_permissions(request, user_id):
    """Actualizar roles de staff de un usuario (solo admin)"""
    try:
        user = get_object_or_404(User, id=user_id)
        data = json.loads(request.body)
        roles = data.get('roles', [])
        individual_permissions = data.get('individual_permissions', [])
        
        # Obtener roles actuales antes de cambiar
        old_roles = list(user.staff_roles.all())
        old_roles_data = [{
            'scope': role.scope,
            'level': role.level,
            'scope_display': role.get_scope_display(),
            'level_display': role.get_level_display()
        } for role in old_roles]
        
        # Crear un diccionario para manejar scopes únicos
        roles_dict = {}
        for role_data in roles:
            scope = role_data['scope']
            # Si ya existe un role con este scope, actualizar el nivel
            if scope in roles_dict:
                roles_dict[scope]['level'] = max(roles_dict[scope]['level'], role_data['level'])
            else:
                roles_dict[scope] = role_data
        
        # Obtener roles actuales del usuario
        existing_roles = {role.scope: role for role in user.staff_roles.all()}
        
        # Actualizar o crear roles
        for scope, role_data in roles_dict.items():
            if scope in existing_roles:
                # Actualizar rol existente
                role = existing_roles[scope]
                role.level = role_data['level']
                role.save(update_fields=['level'])
            else:
                # Crear nuevo rol
                StaffRole.objects.create(
                    user=user,
                    scope=role_data['scope'],
                    level=role_data['level']
                )
        
        # Eliminar roles que ya no están en la lista
        scopes_to_keep = set(roles_dict.keys())
        for scope, role in existing_roles.items():
            if scope not in scopes_to_keep:
                role.delete()
        
        # Actualizar is_staff basado en roles
        user.is_staff = len(roles_dict) > 0
        user.save(update_fields=['is_staff'])
        
        # Obtener nuevos roles para el log
        new_roles = list(user.staff_roles.all())
        new_roles_data = [{
            'scope': role.scope,
            'level': role.level,
            'scope_display': role.get_scope_display(),
            'level_display': role.get_level_display()
        } for role in new_roles]
        
        # Registrar en audit log (también manejado por decorador)
        AuditLog.log_action(
            request=request,
            action_type="permissions_update",
            target_user=user,
            details={
                "user_id": user.id,
                "username": user.roblox_username,
                "old_roles": old_roles_data,
                "new_roles": new_roles_data,
                "admin": request.user.roblox_username,
                "individual_permissions": individual_permissions
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": f"Roles updated for {user.roblox_username}",
            "roles": list(roles_dict.values()),
            "individual_permissions": individual_permissions
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_staff_permission("full_moderation_control")
def api_get_user_permissions_admin(request, user_id):
    """Obtener permisos de un usuario (vista admin)"""
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Obtener todos los permisos del usuario
        all_permissions = set()
        user_roles = []
        
        for role in user.staff_roles.all():
            perms_by_level = STAFF_PERMISSIONS.get(role.scope, {})
            for lvl in range(1, role.level + 1):
                if lvl in perms_by_level:
                    # Traducir los permisos
                    translated_perms = [get_permission_display(p) for p in perms_by_level[lvl]]
                    all_permissions.update(translated_perms)
            
            user_roles.append({
                'scope': role.scope,
                'level': role.level,
                'scope_display': role.get_scope_display(),
                'level_display': role.get_level_display(),
                'assigned_at': role.assigned_at.isoformat() if role.assigned_at else None
            })
        
        return JsonResponse({
            "roles": user_roles,
            "permissions": list(all_permissions),
            "user": {
                "id": user.id,
                "roblox_username": user.roblox_username,
                "roblox_id": user.roblox_id,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "warning_count": user.warning_count,
                "is_banned": user.is_banned
            }
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@require_staff_permission("full_moderation_control")
def api_get_staff_users(request):
    """Obtener todos los usuarios con roles de staff"""
    try:
        # Obtener usuarios con roles de staff
        staff_users = User.objects.filter(
            staff_roles__isnull=False
        ).distinct().prefetch_related('staff_roles')
        
        staff_data = []
        for user in staff_users:
            roles = []
            all_permissions = set()
            
            for role in user.staff_roles.all():
                roles.append({
                    'scope': role.scope,
                    'level': role.level,
                    'scope_display': role.get_scope_display(),
                    'level_display': role.get_level_display()
                })
                
                perms_by_level = STAFF_PERMISSIONS.get(role.scope, {})
                for lvl in range(1, role.level + 1):
                    if lvl in perms_by_level:
                        # Traducir permisos
                        translated_perms = [get_permission_display(p) for p in perms_by_level[lvl]]
                        all_permissions.update(translated_perms)
            
            staff_data.append({
                'id': user.id,
                'roblox_username': user.roblox_username,
                'roblox_id': user.roblox_id,
                'roles': roles,
                'permissions_count': len(all_permissions),
                'is_superuser': user.is_superuser,
                'is_banned': user.is_banned,
                'warning_count': user.warning_count,
                'first_login': user.first_login.isoformat() if user.first_login else None
            })
        
        return JsonResponse({
            "staff_users": staff_data,
            "total": len(staff_data)
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@require_staff_permission("full_moderation_control")
def api_get_permissions_structure(request):
    """Obtener la estructura completa de permisos para el frontend"""
    try:
        # Transformar STAFF_PERMISSIONS a formato más usable
        permissions_structure = {}
        
        for scope, levels in STAFF_PERMISSIONS.items():
            scope_permissions = {}
            for level, permissions in levels.items():
                # Traducir los nombres de permisos
                translated_permissions = [get_permission_display(p) for p in permissions]
                scope_permissions[f"level_{level}"] = {
                    'permissions': translated_permissions,
                    'description': f"Nivel {level}",
                    'level_display': get_level_display(scope, level)
                }
            permissions_structure[scope] = scope_permissions
        
        # Agregar información de display usando las choices del modelo
        from users.models import StaffRole
        scope_choices = dict(StaffRole.Scope.choices)
        
        # Traducir todos los permisos disponibles
        all_permissions_en = [
            'create_warn',
            'register_ban',
            'access_moderation_dashboard',
            'manage_warns',
            'view_characters_basic',
            'full_discord_moderation',
            'full_moderation_control',
            'change_ssu_status',
            'edit_rp_files_basic',
            'edit_rp_files_full',
            'moderate_factions_basic',
            'moderate_factions_full',
            'supervise_actors_basic',
            'supervise_actors_full'
        ]
        
        all_permissions_es = [get_permission_display(p) for p in all_permissions_en]
        
        return JsonResponse({
            "permissions_structure": permissions_structure,
            "scope_choices": scope_choices,
            "all_permissions": all_permissions_es,
            "all_permissions_en": all_permissions_en  # Mantener también en inglés para el backend
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_permission_display(permission):
    """Convertir nombres de permisos a español"""
    permission_translations = {
        'create_warn': 'Crear Warn',
        'register_ban': 'Registrar Ban',
        'access_moderation_dashboard': 'Acceso al Dashboard de Moderación',
        'manage_warns': 'Gestionar Warns',
        'view_characters_basic': 'Ver Personajes Básico',
        'full_discord_moderation': 'Moderación Discord Completa',
        'change_ssu_status': 'Cambiar Estado SSU',
        'edit_rp_files_basic': 'Editar Archivos RP Básico',
        'edit_rp_files_full': 'Editar Archivos RP Completo',
        'moderate_factions_basic': 'Moderar Facciones Básico',
        'moderate_factions_full': 'Moderar Facciones Completo',
        'supervise_actors_basic': 'Supervisar Actores Básico',
        'supervise_actors_full': 'Supervisar Actores Completo',
        'change_ssu_status': 'Cambiar Estado SSU',
        'full_moderation_control': 'Control Moderación Total'
    }
    return permission_translations.get(permission, permission)


def get_level_display(scope, level):
    """Return human-readable level name based on scope"""
    level_names = {
        "global": {
            1: "SSU Host",
            2: "Admin+"
        },
        "moderation": {
            1: "Junior",
            2: "Official",
            3: "Qualified",
            4: "Senior"
        },
        "ingame": {
            1: "Junior",
            2: "Official",
            3: "Qualified+"
        },
        "discord": {
            1: "Junior",
            2: "Official",
            3: "Qualified",
            4: "Senior"
        },
        "rp_roleplay": {
            1: "RP Team",
            2: "RP Lead"
        },
        "rp_faction": {
            1: "Faction Team",
            2: "Faction Lead"
        },
        "rp_actors": {
            1: "SCP Team",
            2: "SCP Lead"
        }
    }
    
    scope_levels = level_names.get(scope, {})
    return scope_levels.get(level, f"Nivel {level}")

# ==================== FUNCIONES PARA MANEJO DE ROLES ====================

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("full_moderation_control")
@log_action("role_assigned")
def api_assign_role(request):
    """Asigna un rol específico a un usuario"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        scope = data.get('scope')
        level = int(data.get('level', 1))
        
        user = get_object_or_404(User, id=user_id)
        
        # Verificar si el rol ya existe
        existing_role = user.staff_roles.filter(scope=scope).first()
        if existing_role:
            existing_role.level = level
            existing_role.save()
            action = "updated"
        else:
            StaffRole.objects.create(
                user=user,
                scope=scope,
                level=level
            )
            action = "assigned"
        
        # Actualizar is_staff si es necesario
        user.is_staff = user.staff_roles.exists()
        user.save(update_fields=['is_staff'])
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="role_assigned",
            target_user=user,
            details={
                "user_id": user.id,
                "username": user.roblox_username,
                "scope": scope,
                "level": level,
                "action": action,
                "admin": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": f"Role {action} for {user.roblox_username}",
            "scope": scope,
            "level": level
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("full_moderation_control")
@log_action("role_removed")
def api_remove_role(request):
    """Elimina un rol específico de un usuario"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        scope = data.get('scope')
        
        user = get_object_or_404(User, id=user_id)
        
        # Buscar y eliminar el rol
        role = user.staff_roles.filter(scope=scope).first()
        if not role:
            return JsonResponse({"error": "Role not found"}, status=404)
        
        role_data = {
            "scope": role.scope,
            "level": role.level,
            "scope_display": role.get_scope_display(),
            "level_display": role.get_level_display()
        }
        
        role.delete()
        
        # Actualizar is_staff si es necesario
        user.is_staff = user.staff_roles.exists()
        user.save(update_fields=['is_staff'])
        
        # Registrar en audit log
        AuditLog.log_action(
            request=request,
            action_type="role_removed",
            target_user=user,
            details={
                "user_id": user.id,
                "username": user.roblox_username,
                "removed_role": role_data,
                "admin": request.user.roblox_username
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": f"Role removed from {user.roblox_username}",
            "removed_role": role_data
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)