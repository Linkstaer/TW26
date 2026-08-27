from django.urls import path, include
from . import views
from .api import users
from .api import ssu
from .api import ai

urlpatterns = [
    path("auth/user/", views.api_get_current_user),
    path("events/", views.sse_events, name="sse_events"),
    path("ssu/", ssu.api_get_ssu_status),
    path("ssu/toggle/", ssu.api_toggle_ssu_status),
    path("ssu/info/", ssu.api_get_ssu_info),
    path("ai/query/", ai.api_ai_query, name="api_ai_query"),
    path("ai/history/", ai.api_ai_history, name="api_ai_history"),
    path("", include("characters.urls")),
    path(
        "users/<int:roblox_id>/",
        users.api_get_user_by_roblox_id,
        name="api_get_user_by_roblox_id",
    ),
    path(
        "users/<int:roblox_id>/characters/",
        users.api_get_user_characters,
        name="api_get_user_characters",
    ),
]
