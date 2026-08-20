from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StaffRole, Warn, Ban

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('roblox_username', 'roblox_id', 'warning_count', 'is_banned', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_banned')
    search_fields = ('roblox_username', 'roblox_id')
    ordering = ('-warning_count',)
    
    fieldsets = (
        (None, {'fields': ('roblox_id', 'roblox_username')}),
        ('Moderation', {'fields': ('warning_count', 'is_banned', 'ban_reason', 'banned_until', 'banned_by')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('first_login', 'last_login')}),
    )
    
    readonly_fields = ('warning_count', 'first_login', 'last_login')


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'scope', 'level', 'assigned_at')
    list_filter = ('scope', 'level')
    search_fields = ('user__roblox_username', 'user__roblox_id')
    raw_id_fields = ('user',)


@admin.register(Warn)
class WarnAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'created_by', 'severity', 'status', 'appealed', 'created_at', 'expires_at')
    list_filter = ('status', 'severity', 'appealed', 'created_at')
    search_fields = ('target__roblox_username', 'target__roblox_id', 'reason')
    raw_id_fields = ('target', 'created_by', 'appealed_by', 'appeal_responded_by')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('target', 'created_by', 'reason', 'evidence', 'severity')
        }),
        ('Appeal System', {
            'fields': ('appealed', 'appealed_at', 'appealed_by', 'appeal_response', 
                      'appeal_responded_by', 'appeal_responded_at')
        }),
        ('Expiration', {
            'fields': ('expires_at', 'expires_after_days', 'status')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'ban_type', 'is_active', 'created_by', 'created_at', 'ends_at')
    list_filter = ('ban_type', 'is_active', 'can_appeal', 'created_at')
    search_fields = ('target__roblox_username', 'target__roblox_id', 'reason')
    raw_id_fields = ('target', 'created_by', 'revoked_by')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('target', 'created_by', 'reason', 'evidence')
        }),
        ('Ban Details', {
            'fields': ('ban_type', 'duration_days', 'ends_at', 'can_appeal', 'appealed', 'appeal_response')
        }),
        ('Revocation', {
            'fields': ('is_active', 'revoked_at', 'revoked_by', 'revocation_reason')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )