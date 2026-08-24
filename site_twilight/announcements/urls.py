from django.urls import path
from . import views

urlpatterns = [
    # Anuncios
    path("announcements/", views.announcement_list, name="announcement_list"),
    path(
        "announcements/create/",
        views.announcement_create,
        name="announcement_create",
    ),
    path(
        "announcements/<int:announcement_id>/",
        views.announcement_detail,
        name="announcement_detail",
    ),
    path(
        "announcements/<int:announcement_id>/view/",
        views.view_announcement,
        name="view_announcement",
    ),
    # Eventos
    path("feed/events/", views.event_list, name="event_list"),
    # Sugerencias de Lore (Boosters)
    path("lore/suggestions/", views.lore_suggestion_list, name="lore_suggestion_list"),
    path(
        "lore/suggestions/create/",
        views.lore_suggestion_create,
        name="lore_suggestion_create",
    ),
    path(
        "lore/suggestions/<int:suggestion_id>/review/",
        views.lore_suggestion_review,
        name="lore_suggestion_review",
    ),
]
