from django.urls import path, include
from . import views
from .api import users
from .api import ssu

urlpatterns = [
    path("auth/user/", views.api_get_current_user),
    path("events/", views.sse_events, name="sse_events"),
    path("ssu/", ssu.api_get_ssu_status),
    path("ssu/toggle/", ssu.api_toggle_ssu_status),
    path("ssu/info/", ssu.api_get_ssu_info),
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
    path("", include("characters.urls")),
]
