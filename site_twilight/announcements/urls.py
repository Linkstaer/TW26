from django.urls import path
from . import views

urlpatterns = [
    # Anuncios
    path("announcements/", views.announcement_list, name="announcement_list"),
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
    path("events/", views.event_list, name="event_list"),
]
