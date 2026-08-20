from django.contrib import admin
from .models import (
    AccessCard,
    Faction,
    FactionRank,
    CharacterFactionMembership,
    FactionApplication,
    FactionLog,
    FactionInvitation,
)


@admin.register(AccessCard)
class AccessCardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "is_classified",
    ]
    list_filter = ["is_classified"]
    search_fields = ["name", "description"]


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_display = [
        "display_name",
        "name",
        "faction_type",
        "status",
        "is_classified",
        "is_public",
    ]
    list_filter = [
        "faction_type",
        "status",
        "is_classified",
        "is_public",
        "allow_applications",
    ]
    search_fields = ["display_name", "name"]
    filter_horizontal = ["leaders"]


@admin.register(FactionRank)
class FactionRankAdmin(admin.ModelAdmin):
    list_display = ["faction", "name", "level", "access_card"]
    list_filter = ["faction"]
    search_fields = ["name", "faction__display_name"]


@admin.register(CharacterFactionMembership)
class CharacterFactionMembershipAdmin(admin.ModelAdmin):
    list_display = ["character", "faction", "rank", "status", "joined_at"]
    list_filter = ["status", "faction"]
    search_fields = ["character__codename", "faction__display_name"]


@admin.register(FactionApplication)
class FactionApplicationAdmin(admin.ModelAdmin):
    list_display = ["character", "faction", "status", "created_at", "reviewed_by"]
    list_filter = ["status", "faction"]
    search_fields = ["character__codename", "faction__display_name"]
    readonly_fields = ["created_at"]


@admin.register(FactionInvitation)
class FactionInvitationAdmin(admin.ModelAdmin):
    list_display = ["character", "faction", "status", "invited_by", "created_at"]
    list_filter = ["status", "faction"]
    search_fields = ["character__codename", "faction__display_name"]
    readonly_fields = ["created_at"]


@admin.register(FactionLog)
class FactionLogAdmin(admin.ModelAdmin):
    list_display = ["faction", "action_type", "character", "performed_by", "created_at"]
    list_filter = ["action_type", "faction"]
    readonly_fields = ["created_at"]
