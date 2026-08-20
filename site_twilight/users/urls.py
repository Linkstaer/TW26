from django.urls import path
from .views import accounts, moderation, permissions, audit
from .views.permissions import (
    api_get_user_permissions,
    api_get_current_user,
    api_update_user_permissions,
    api_get_user_permissions_admin,
    api_get_staff_users,
    api_get_permissions_structure
)

urlpatterns = [
    path("login/roblox/", accounts.roblox_login, name="roblox_login"),
    path("login/roblox/callback/", accounts.roblox_callback, name="roblox_callback"),
    path("logout/", accounts.logout_view, name="logout"),
    path('auth/user/', permissions.api_get_current_user, name='current_user'),
    
    # Dashboard
    path('moderation/dashboard/', moderation.api_moderation_dashboard, name='moderation_dashboard'),
    
    # Staff management
    path("staff/users/", api_get_staff_users, name="api_get_staff_users"),
    path("staff/permissions/structure/", api_get_permissions_structure, name="api_get_permissions_structure"),
    
    # Warns
    path('moderation/warns/', moderation.api_list_warns, name='list_warns'),
    path('moderation/warns/create/', moderation.api_create_warn, name='create_warn'),
    path('moderation/warns/<int:warn_id>/update/', moderation.api_update_warn, name='update_warn'),
    path('moderation/warns/<int:warn_id>/remove/', moderation.api_remove_warn, name='remove_warn'),
    
    # Appeals
    path('moderation/warns/<int:warn_id>/appeal/', moderation.api_appeal_warn, name='appeal_warn'),
    path('moderation/warns/<int:warn_id>/respond-appeal/', moderation.api_respond_appeal, name='respond_appeal'),
    
    # Bans
    path('moderation/bans/', moderation.api_list_bans, name='list_bans'),
    path('moderation/bans/create/', moderation.api_create_ban, name='create_ban'),
    path('moderation/bans/<int:ban_id>/revoke/', moderation.api_revoke_ban, name='revoke_ban'),
    
    # User-specific
    path('moderation/user/<int:roblox_id>/', moderation.api_get_user_moderation_info, name='user_moderation_info'),
    
    # Search users
    path('moderation/users/search/<str:query>/', moderation.api_search_users, name='search_users'),

    # Apeals
    path('moderation/user/appeals/', moderation.api_get_user_appeals, name='user_appeals'),
    
    # Characters
    path('moderation/characters/', moderation.api_characters_for_moderation, name='characters_moderation'),
    
    # Permissions
    path("auth/user/permissions/", api_get_user_permissions, name="api_get_user_permissions"),
    path("auth/user/<int:user_id>/permissions/", api_update_user_permissions, name="api_update_user_permissions"),
    path("auth/user/<int:user_id>/permissions/view/", api_get_user_permissions_admin, name="api_get_user_permissions_admin"),
    path('audit/logs/', audit.api_get_audit_logs, name='api_get_audit_logs'),
    path('audit/logs/export/', audit.api_export_audit_logs, name='api_export_audit_logs'),
    path('audit/logs/clean/', audit.api_clean_old_logs, name='api_clean_old_logs'),
    path('audit/logs/<int:log_id>/delete/', audit.api_delete_audit_log, name='api_delete_audit_log'),
    path('audit/users/', audit.api_get_audit_users, name='api_get_audit_users'),
    path('audit/stats/', audit.api_get_audit_stats, name='api_get_audit_stats'),
    
]