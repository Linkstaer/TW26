from django.contrib import admin

# Register your models here.

from core.models import SiteState

@admin.register(SiteState)
class SiteStateAdmin(admin.ModelAdmin):
    list_display = ("ssu_status", "updated_at")
    
    def has_add_permission(self, request):
        return False