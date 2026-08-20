from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import json
import csv
from django.http import HttpResponse
from django.db.models import Q
from users.models import AuditLog, User
from users.decorators import require_staff_permission

@csrf_exempt
@require_http_methods(["GET"])
@require_staff_permission("full_moderation_control")
def api_get_audit_logs(request):
    """Obtener logs de auditoría con filtros"""
    try:
        # Parámetros de filtro
        action_type = request.GET.get('action_type', 'all')
        user_id = request.GET.get('user_id', 'all')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        sort = request.GET.get('sort', '-created_at')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        # Query base
        queryset = AuditLog.objects.select_related(
            'action_user',
            'target_user',
            'target_warn',
            'target_ban',
            'target_character'
        ).all()
        
        # Aplicar filtros
        if action_type != 'all':
            queryset = queryset.filter(action_type=action_type)
        
        if user_id != 'all':
            user_id = int(user_id)
            queryset = queryset.filter(
                Q(action_user__id=user_id) | 
                Q(target_user__id=user_id)
            )
        
        if start_date:
            start_date = timezone.datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            queryset = queryset.filter(created_at__gte=start_date)
        
        if end_date:
            end_date = timezone.datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            end_date = end_date + timedelta(days=1)  # Incluir todo el día
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Ordenar
        if sort == '-created_at':
            queryset = queryset.order_by('-created_at')
        elif sort == 'created_at':
            queryset = queryset.order_by('created_at')
        elif sort == 'action_type':
            queryset = queryset.order_by('action_type')
        elif sort == '-action_type':
            queryset = queryset.order_by('-action_type')
        
        # Paginación
        total = queryset.count()
        total_pages = (total + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        logs = queryset[offset:offset + page_size]
        
        # Serializar logs
        logs_data = []
        for log in logs:
            log_data = {
                'id': log.id,
                'action_type': log.action_type,
                'action_type_display': log.get_action_type_display(),
                'created_at': log.created_at.isoformat() if log.created_at else None,
                'ip_address': log.ip_address,
                'user_agent': log.user_agent,
                'details': log.details,
                'action_user': None,
                'target_user': None,
                'target_warn': None,
                'target_ban': None,
                'target_character': None
            }
            
            if log.action_user:
                log_data['action_user'] = {
                    'id': log.action_user.id,
                    'roblox_username': log.action_user.roblox_username,
                    'roblox_id': log.action_user.roblox_id
                }
            
            if log.target_user:
                log_data['target_user'] = {
                    'id': log.target_user.id,
                    'roblox_username': log.target_user.roblox_username,
                    'roblox_id': log.target_user.roblox_id
                }
            
            if log.target_warn:
                log_data['target_warn'] = {
                    'id': log.target_warn.id,
                    'reason': log.target_warn.reason,
                    'severity': log.target_warn.severity
                }
            
            if log.target_ban:
                log_data['target_ban'] = {
                    'id': log.target_ban.id,
                    'reason': log.target_ban.reason,
                    'ban_type': log.target_ban.ban_type
                }
            
            if log.target_character:
                log_data['target_character'] = {
                    'id': log.target_character.id,
                    'codename': log.target_character.codename,
                    'faction': log.target_character.faction
                }
            
            logs_data.append(log_data)
        
        return JsonResponse({
            'logs': logs_data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': total_pages
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@require_staff_permission("full_moderation_control")
def api_get_audit_users(request):
    """Obtener lista de usuarios para filtros"""
    try:
        # Obtener usuarios que han realizado acciones o han sido afectados
        user_ids = set(
            list(AuditLog.objects.exclude(action_user=None).values_list('action_user__id', flat=True)) +
            list(AuditLog.objects.exclude(target_user=None).values_list('target_user__id', flat=True))
        )
        
        users = User.objects.filter(id__in=user_ids).order_by('roblox_username')
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'roblox_username': user.roblox_username,
                'roblox_id': user.roblox_id
            })
        
        return JsonResponse({
            'users': users_data,
            'total': len(users_data)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@require_staff_permission("full_moderation_control")
def api_export_audit_logs(request):
    """Exportar logs a CSV"""
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="audit-logs-{timezone.now().date()}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Fecha', 'Acción', 'Usuario', 'ID Usuario', 
            'Usuario Afectado', 'ID Usuario Afectado', 'IP', 'Detalles'
        ])
        
        logs = AuditLog.objects.select_related(
            'action_user', 'target_user'
        ).order_by('-created_at')
        
        for log in logs:
            writer.writerow([
                log.id,
                log.created_at.strftime('%Y-%m-%d %H:%M:%S') if log.created_at else '',
                log.get_action_type_display(),
                log.action_user.roblox_username if log.action_user else 'Sistema',
                log.action_user.roblox_id if log.action_user else '',
                log.target_user.roblox_username if log.target_user else '',
                log.target_user.roblox_id if log.target_user else '',
                log.ip_address or '',
                json.dumps(log.details, ensure_ascii=False)
            ])
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@require_staff_permission("full_moderation_control")
def api_clean_old_logs(request):
    """Eliminar logs antiguos (más de 30 días)"""
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        deleted_count, _ = AuditLog.objects.filter(
            created_at__lt=thirty_days_ago
        ).delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Se eliminaron {deleted_count} registros antiguos'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
@require_staff_permission("full_moderation_control")
def api_delete_audit_log(request, log_id):
    """Eliminar un registro específico de auditoría"""
    try:
        log = AuditLog.objects.get(id=log_id)
        log.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Registro #{log_id} eliminado'
        })
        
    except AuditLog.DoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@require_staff_permission("full_moderation_control")
def api_get_audit_stats(request):
    """Obtener estadísticas de auditoría"""
    try:
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Total logs
        total_logs = AuditLog.objects.count()
        
        # Logs por tipo
        logs_by_type = {}
        for log_type, display in AuditLog.ActionType.choices:
            count = AuditLog.objects.filter(action_type=log_type).count()
            if count > 0:
                logs_by_type[display] = count
        
        # Actividad reciente
        today_logs = AuditLog.objects.filter(
            created_at__date=today
        ).count()
        
        weekly_logs = AuditLog.objects.filter(
            created_at__date__gte=week_ago
        ).count()
        
        monthly_logs = AuditLog.objects.filter(
            created_at__date__gte=month_ago
        ).count()
        
        # Usuarios más activos
        active_users = []
        from django.db.models import Count
        
        user_activity = AuditLog.objects.exclude(action_user=None).values(
            'action_user__roblox_username',
            'action_user__roblox_id'
        ).annotate(
            action_count=Count('id')
        ).order_by('-action_count')[:10]
        
        for activity in user_activity:
            active_users.append({
                'username': activity['action_user__roblox_username'],
                'roblox_id': activity['action_user__roblox_id'],
                'action_count': activity['action_count']
            })
        
        return JsonResponse({
            'stats': {
                'total_logs': total_logs,
                'today_logs': today_logs,
                'weekly_logs': weekly_logs,
                'monthly_logs': monthly_logs,
                'logs_by_type': logs_by_type,
                'active_users': active_users
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)