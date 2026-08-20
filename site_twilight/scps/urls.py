from django.urls import path
from . import views

urlpatterns = [
    # SCPs
    path("scps/", views.scp_list, name="scp_list"),
    path("scps/<int:scp_id>/", views.scp_detail, name="scp_detail"),
    path("scps/<int:scp_id>/edit/", views.scp_edit, name="scp_edit"),
    # Documentos
    path("documents/", views.document_list, name="document_list"),
    path("documents/<slug:slug>/", views.document_detail, name="document_detail"),
    path("documents/<slug:slug>/edit/", views.document_edit, name="document_edit"),
]
