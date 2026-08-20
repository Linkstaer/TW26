from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator


class Announcement(models.Model):
    """
    Anuncios del sitio con filtros por nivel de acceso.
    """

    class AnnouncementType(models.TextChoices):
        IN_RP = "in_rp", "In-RP"
        OFF_RP = "off_rp", "Off-RP"
        AUTOMATIC = "automatic", "Automático"
        CRITICAL = "critical", "Crítico"

    title = models.CharField(max_length=200)
    content = models.TextField(validators=[MaxLengthValidator(10000)])
    announcement_type = models.CharField(
        max_length=20, choices=AnnouncementType.choices
    )

    # Nivel mínimo para ver
    min_access_level = models.CharField(max_length=10, default="L1")

    # Facción restrictiva
    faction = models.ForeignKey(
        "factions.Faction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
    )

    # SCP relacionado (para automáticos)
    related_scp = models.ForeignKey(
        "scps.SCP",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
    )

    # Autor
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="announcements",
    )

    # Visibilidad
    is_published = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)

    # Métricas
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_announcement_type_display()})"

    def can_user_view(self, user) -> bool:
        """Verifica si el usuario puede ver este anuncio"""
        if not user.is_authenticated:
            return (
                self.min_access_level == "L1"
                and self.announcement_type != self.AnnouncementType.CRITICAL
            )

        if user.is_superuser:
            return True

        # Verificar nivel de acceso
        accessible_levels = user.get_accessible_levels()
        level_priority = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6}

        user_level = max([level_priority.get(l, 0) for l in accessible_levels])
        required_level = level_priority.get(self.min_access_level, 1)

        if user_level < required_level:
            return False

        # Verificar restricción de facción
        if self.faction:
            user_factions = user.get_visible_factions()
            if not any(f["id"] == self.faction.id for f in user_factions):
                return False

        return True


class AnnouncementView(models.Model):
    """Registra quién ha visto cada anuncio"""

    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE, related_name="views_log"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="announcement_views",
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("announcement", "user")
        verbose_name = "Vista de Anuncio"
        verbose_name_plural = "Vistas de Anuncios"


class EventLog(models.Model):
    """
    Logs de eventos automáticos del sistema.
    """

    class EventType(models.TextChoices):
        SCP_CREATED = "scp_created", "Nuevo SCP"
        SCP_DELETED = "scp_deleted", "SCP Eliminado"
        FACTION_CREATED = "faction_created", "Facción Creada"
        FACTION_DISSOLVED = "faction_dissolved", "Facción Disuelta"
        DOCUMENT_CREATED = "document_created", "Documento Creado"
        USER_JOINED_FACTION = "user_joined_faction", "Usuario se unió a Facción"
        USER_LEFT_FACTION = "user_left_faction", "Usuario salió de Facción"

    event_type = models.CharField(max_length=30, choices=EventType.choices)

    # Referencias
    scp = models.ForeignKey(
        "scps.SCP",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    faction = models.ForeignKey(
        "factions.Faction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    document = models.ForeignKey(
        "scps.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Nivel de acceso del evento
    min_access_level = models.CharField(max_length=10, default="L1")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.title}"


class Notification(models.Model):
    """
    Notificaciones de usuario.
    """

    class NotificationType(models.TextChoices):
        FACTION_INVITATION = "faction_invitation", "Invitación de Facción"
        FACTION_APPLICATION = "faction_application", "Solicitud de Ingreso"
        APPLICATION_ACCEPTED = "application_accepted", "Solicitud Aceptada"
        APPLICATION_REJECTED = "application_rejected", "Solicitud Rechazada"
        ANNOUNCEMENT = "announcement", "Anuncio"
        SYSTEM = "system", "Sistema"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=30, choices=NotificationType.choices
    )

    title = models.CharField(max_length=200)
    message = models.TextField()

    # Referencias opcionales
    related_faction = models.ForeignKey(
        "factions.Faction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    related_application = models.ForeignKey(
        "factions.FactionApplication",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    related_invitation = models.ForeignKey(
        "factions.FactionInvitation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    related_announcement = models.ForeignKey(
        Announcement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )

    # Estado
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.user.roblox_username}"

    def mark_as_read(self):
        self.is_read = True
        from django.utils import timezone

        self.read_at = timezone.now()
        self.save()


from django.utils import timezone
