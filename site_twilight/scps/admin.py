from django.contrib import admin
from .models import SCP, SCPEditLog, Document, DocumentEditLog


@admin.register(SCP)
class SCPAdmin(admin.ModelAdmin):
    list_display = ["scp_id", "title", "object_class", "is_active", "created_at"]
    list_filter = ["object_class", "is_active"]
    search_fields = ["scp_id", "title"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(SCPEditLog)
class SCPEditLogAdmin(admin.ModelAdmin):
    list_display = ["scp", "section", "edited_by", "created_at"]
    list_filter = ["section"]
    readonly_fields = ["created_at"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "doc_type",
        "min_access_level",
        "author",
        "is_published",
        "created_at",
    ]
    list_filter = ["doc_type", "is_published", "min_access_level"]
    search_fields = ["title", "content"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(DocumentEditLog)
class DocumentEditLogAdmin(admin.ModelAdmin):
    list_display = ["document", "edited_by", "created_at"]
    readonly_fields = ["created_at"]
