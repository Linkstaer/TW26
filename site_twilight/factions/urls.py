from django.urls import path
from . import views

urlpatterns = [
    # Facciones públicas
    path("factions/types/", views.faction_types_list, name="faction_types_list"),
    path("factions/", views.faction_list, name="faction_list"),
    path("factions/my/", views.my_factions, name="my_factions"),
    path("factions/all/", views.faction_all, name="faction_all"),
    path("factions/create/", views.faction_create, name="faction_create"),
    path(
        "factions/<int:faction_id>/update/", views.faction_update, name="faction_update"
    ),
    path(
        "factions/<int:faction_id>/members/",
        views.faction_members,
        name="faction_members",
    ),
    path("factions/<int:faction_id>/apply/", views.faction_apply, name="faction_apply"),
    # Rangos
    path("factions/<int:faction_id>/ranks/", views.faction_ranks, name="faction_ranks"),
    # Invitaciones
    path(
        "factions/<int:faction_id>/invite/",
        views.invite_member,
        name="invite_member",
    ),
    # Detail should be last
    path("factions/<int:faction_id>/", views.faction_detail, name="faction_detail"),
    # Solicitudes
    path("applications/", views.my_applications, name="my_applications"),
    path(
        "applications/<int:app_id>/cancel/",
        views.cancel_application,
        name="cancel_application",
    ),
    # Invitaciones personales
    path("invitations/", views.my_invitations, name="my_invitations"),
    path(
        "invitations/<int:invitation_id>/respond/",
        views.respond_invitation,
        name="respond_invitation",
    ),
    # Invitaciones de facción
    path(
        "factions/<int:faction_id>/invitations/",
        views.faction_invitations,
        name="faction_invitations",
    ),
    path(
        "factions/invitations/<int:invitation_id>/cancel/",
        views.cancel_invitation,
        name="cancel_invitation",
    ),
    # Dashboard de facción (para líderes)
    path(
        "faction-dashboard/<int:faction_id>/",
        views.faction_dashboard,
        name="faction_dashboard",
    ),
    path(
        "faction-dashboard/<int:faction_id>/applications/",
        views.faction_applications,
        name="faction_applications",
    ),
    path(
        "faction-dashboard/<int:faction_id>/applications/<int:app_id>/",
        views.review_application,
        name="review_application",
    ),
    path(
        "faction-dashboard/<int:faction_id>/members/<int:member_id>/",
        views.manage_member,
        name="manage_member",
    ),
    # Tarjetas
    path("cards/", views.access_cards_list, name="access_cards_list"),
    path("cards/create/", views.create_access_card, name="create_access_card"),
    path("cards/<int:card_id>/", views.access_card_detail, name="access_card_detail"),
    path(
        "cards/<int:card_id>/update/",
        views.update_access_card,
        name="update_access_card",
    ),
    # Rangos
    path(
        "faction-dashboard/<int:faction_id>/ranks/create/",
        views.create_faction_rank,
        name="create_faction_rank",
    ),
    path(
        "faction-dashboard/<int:faction_id>/ranks/<int:rank_id>/update/",
        views.update_faction_rank,
        name="update_faction_rank",
    ),
    path(
        "faction-dashboard/<int:faction_id>/ranks/<int:rank_id>/delete/",
        views.delete_faction_rank,
        name="delete_faction_rank",
    ),
    # Divisiones
    path(
        "faction-dashboard/<int:faction_id>/divisions/",
        views.faction_divisions,
        name="faction_divisions",
    ),
    path(
        "faction-dashboard/<int:faction_id>/divisions/create/",
        views.create_division,
        name="create_division",
    ),
    path(
        "faction-dashboard/<int:faction_id>/divisions/<int:division_id>/add-member/",
        views.add_member_to_division,
        name="add_member_to_division",
    ),
    # Notificaciones
    path("notifications/", views.notifications_list, name="notifications_list"),
    path(
        "notifications/unread-count/",
        views.notifications_unread_count,
        name="notifications_unread_count",
    ),
    path(
        "notifications/<int:notification_id>/read/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
    path(
        "notifications/read-all/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
]
