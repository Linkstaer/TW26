from django.urls import path
from . import views

urlpatterns = [
    # SCPs
    path("scps/", views.scp_list, name="scp_list"),
    path("scps/create/", views.scp_create, name="scp_create"),
    path("scps/<int:scp_id>/", views.scp_detail, name="scp_detail"),
    path("scps/<int:scp_id>/edit/", views.scp_edit, name="scp_edit"),
    path(
        "scps/<int:scp_id>/appendix/",
        views.scp_add_appendix,
        name="scp_add_appendix",
    ),
    path("scps/<int:scp_id>/history/", views.scp_history, name="scp_history"),
    # Documentos
    path("documents/", views.document_list, name="document_list"),
    path("documents/create/", views.document_create, name="document_create"),
    path("documents/<slug:slug>/", views.document_detail, name="document_detail"),
    path("documents/<slug:slug>/edit/", views.document_edit, name="document_edit"),
]
