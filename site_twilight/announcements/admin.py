from django.contrib import admin
from .models import Announcement, AnnouncementView, EventLog, Notification


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "announcement_type",
        "min_access_level",
        "is_published",
        "is_pinned",
        "created_at",
    ]
    list_filter = ["announcement_type", "is_published", "is_pinned", "min_access_level"]
    search_fields = ["title", "content"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(AnnouncementView)
class AnnouncementViewAdmin(admin.ModelAdmin):
    list_display = ["announcement", "user", "viewed_at"]
    readonly_fields = ["viewed_at"]


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ["event_type", "title", "min_access_level", "created_at"]
    list_filter = ["event_type", "min_access_level"]
    readonly_fields = ["created_at"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "notification_type", "title", "is_read", "created_at"]
    list_filter = ["notification_type", "is_read"]
    search_fields = ["title", "message", "user__roblox_username"]
    readonly_fields = ["created_at"]
