from django.urls import path
from . import views

urlpatterns = [
    path("characters/all/", views.character_list_all, name="character_list_all"),
    path("characters/mine/", views.character_list_user, name="character_list_user"),
    path("characters/create/", views.character_create, name="character_create"),
    path("characters/<int:pk>/", views.character_detail, name="character_detail"),
    path("characters/<int:pk>/update/", views.character_update, name="character_update"),
    path("characters/<int:pk>/delete/", views.character_delete, name="character_delete"),
]