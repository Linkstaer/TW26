from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "announcements"
    verbose_name = "Anuncios y Feed"

    def ready(self):
        from . import signals  # noqa: F401 — eventos automáticos (spec §5.1)
