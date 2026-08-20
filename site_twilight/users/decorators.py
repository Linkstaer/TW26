from functools import wraps
from django.http import JsonResponse
from users.models import AuditLog, User
import json

def require_staff_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Debug logging
            print(f"Permission check for: {permission}")
            print(f"User: {request.user.username if request.user else 'Anonymous'}")
            print(f"Is authenticated: {request.user.is_authenticated if request.user else False}")
            
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)
            
            if request.user.has_permission(permission):
                return view_func(request, *args, **kwargs)
            
            # Debug: List all user permissions
            print(f"User permissions check failed for: {permission}")
            # You might want to add: print(f"User has permissions: {list_user_permissions(request.user)}")
            
            return JsonResponse({"error": "Insufficient permissions"}, status=403)
        return _wrapped_view
    return decorator

def log_action(action_type):
    """Decorador para registrar automáticamente acciones en los logs de auditoría"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Ejecutar la vista primero
            response = view_func(request, *args, **kwargs)
            
            # Solo registrar si la respuesta fue exitosa
            if hasattr(response, 'status_code') and response.status_code in [200, 201]:
                try:
                    # Extraer datos de la respuesta
                    response_data = None
                    if hasattr(response, 'content'):
                        try:
                            response_data = json.loads(response.content)
                        except:
                            response_data = {}
                    
                    # Determinar target_user si está en los datos de la respuesta
                    target_user = None
                    target_warn = None
                    target_ban = None
                    target_character = None
                    details = {}
                    
                    # Extraer información basada en el tipo de acción
                    if action_type in ['warn_created', 'warn_updated', 'warn_removed', 'warn_appealed', 'warn_appeal_responded']:
                        from users.models import Warn
                        warn_id = kwargs.get('warn_id') or (response_data.get('warn', {}).get('id') if response_data else None)
                        if warn_id:
                            try:
                                target_warn = Warn.objects.get(id=warn_id)
                                target_user = target_warn.target
                            except Warn.DoesNotExist:
                                pass
                    
                    elif action_type in ['ban_created', 'ban_revoked', 'ban_appealed', 'ban_appeal_responded']:
                        from users.models import Ban
                        ban_id = kwargs.get('ban_id') or (response_data.get('ban', {}).get('id') if response_data else None)
                        if ban_id:
                            try:
                                target_ban = Ban.objects.get(id=ban_id)
                                target_user = target_ban.target
                            except Ban.DoesNotExist:
                                pass
                    
                    elif action_type in ['character_created', 'character_updated', 'character_deleted']:
                        from characters.models import Character
                        character_id = kwargs.get('pk') or (response_data.get('character', {}).get('id') if response_data else None)
                        if character_id:
                            try:
                                target_character = Character.objects.get(id=character_id)
                                target_user = target_character.user
                            except Character.DoesNotExist:
                                pass
                    
                    elif action_type in ['permissions_update', 'role_assigned', 'role_removed']:
                        target_user_id = kwargs.get('user_id') or (request.POST.get('user_id') if request.method == 'POST' else None)
                        if target_user_id:
                            try:
                                target_user = User.objects.get(id=target_user_id)
                            except User.DoesNotExist:
                                pass
                    
                    # Crear el log de auditoría
                    AuditLog.log_action(
                        request=request,
                        action_type=action_type,
                        target_user=target_user,
                        target_warn=target_warn,
                        target_ban=target_ban,
                        target_character=target_character,
                        details=details
                    )
                    
                except Exception as e:
                    print(f"Error registrando acción de auditoría: {e}")
            
            return response
        return wrapper
    return decorator