from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


LEVEL_ORDER = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6}


class AccessCard(models.Model):
    """
    Tarjetas de acceso asignadas a personajes (vía rango de facción).
    Determinan la visibilidad en la DB, el acceso a documentos/SCPs
    y las funcionalidades avanzadas del sitio (spec §2.4).
    """

    class Level(models.TextChoices):
        L1 = "L1", "Nivel 1"
        L2 = "L2", "Nivel 2"
        L3 = "L3", "Nivel 3"
        L4 = "L4", "Nivel 4"
        L5 = "L5", "Nivel 5"
        L6 = "L6", "Nivel 6"

    class CardType(models.TextChoices):
        STANDARD = "standard", "Estándar"
        SCIENTIFIC = "scientific", "Scientific Department"
        ETHICS_COMMITTEE = "ethics_committee", "Comité de Ética"
        O5_COUNCIL = "o5_council", "Consejo O5"
        RAISA = "raisa", "RAISA"
        ADMIN_OFFICE = "admin_office", "Administrators Office"
        BETA_1 = "beta_1", "Beta-1"

    name = models.CharField(max_length=100, unique=True, default="Nueva Tarjeta")
    description = models.TextField(blank=True)
    is_classified = models.BooleanField(default=False)

    level = models.CharField(
        max_length=4, choices=Level.choices, default=Level.L1,
        help_text="Nivel de acceso L1-L6",
    )
    card_type = models.CharField(
        max_length=20, choices=CardType.choices, default=CardType.STANDARD,
        help_text="Casos especiales (O5, RAISA, Beta-1, Comité de Ética...)",
    )

    def __str__(self):
        return f"{self.level} - {self.name}"

    # --- Derivados del nivel (spec §2.4 / §4.2) ---

    @property
    def level_number(self) -> int:
        return LEVEL_ORDER.get(self.level, 1)

    @property
    def display_name(self) -> str:
        """
        Nombre visible de la tarjeta. Seguridad (spec §2.4):
        L5 que no es del Comité de Ética se muestra como vista L4/L5 combinada;
        la tarjeta del Comité de Ética se identifica explícitamente.
        """
        if self.level == self.Level.L5:
            if self.card_type == self.CardType.ETHICS_COMMITTEE:
                return "L4/L5 - Comité de Ética"
            return f"L4/L5 - {self.name}"
        return f"{self.level} - {self.name}"

    def can_view_level(self, level: str) -> bool:
        return self.level_number >= LEVEL_ORDER.get(level, 99)

    @property
    def can_view_l1(self):
        return self.can_view_level("L1")

    @property
    def can_view_l2(self):
        return self.can_view_level("L2")

    @property
    def can_view_l3(self):
        return self.can_view_level("L3")

    @property
    def can_view_l4(self):
        return self.can_view_level("L4")

    @property
    def can_view_l5(self):
        return self.can_view_level("L5")

    @property
    def can_view_l6(self):
        return self.can_view_level("L6")

    # --- Permisos de edición (spec §3.3 / §5.3) ---

    @property
    def can_edit_any(self) -> bool:
        """RAISA / Beta-1 / Administrative Department redactan cualquier documento."""
        return self.card_type in (
            self.CardType.RAISA,
            self.CardType.ADMIN_OFFICE,
            self.CardType.BETA_1,
        ) or self.level == self.Level.L6

    @property
    def can_edit_o5(self) -> bool:
        """Consejo O5: redacta secciones según nivel de acceso."""
        return self.card_type == self.CardType.O5_COUNCIL

    @property
    def can_edit_scd(self) -> bool:
        """Scientific Department: apéndices y comentarios, no la base."""
        return self.card_type == self.CardType.SCIENTIFIC

    @classmethod
    def get_default_card(cls):
        """Tarjeta L1 por defecto para usuarios sin membresías."""
        card, _ = cls.objects.get_or_create(
            name="Nivel 1 - Básico",
            defaults={
                "level": cls.Level.L1,
                "card_type": cls.CardType.STANDARD,
                "description": "Acceso básico al sitio.",
            },
        )
        return card


class FactionType(models.Model):
    """
    Tipos de facción personalizados que pueden ser creados desde el admin.
    """

    key = models.CharField(
        max_length=50, unique=True, help_text="Clave única (e.g., 'mtf', 'research')"
    )
    display_name = models.CharField(max_length=100, help_text="Nombre a mostrar")
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#aa2222", help_text="Color hex")
    icon = models.CharField(
        max_length=50, blank=True, help_text="Icono (nombre de archivo)"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Tipo de Facción"
        verbose_name_plural = "Tipos de Facción"
        ordering = ["order", "display_name"]

    def __str__(self):
        return self.display_name


class Faction(models.Model):
    """
    Facciones del sitio SCP con soporte para fachadas.
    """

    class Type(models.TextChoices):
        DEPARTMENT = "department", "Departamento"
        COUNCIL = "council", "Consejo"
        SPECIAL_FORCE = "special_force", "Fuerza Especial"
        CLASSIFIED = "classified", "Clasificada"

    class Status(models.TextChoices):
        ACTIVE = "active", "Activa"
        DISSOLVED = "dissolved", "Disuelta"
        RESTRICTED = "restricted", "Restringida"

    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(
        max_length=100, help_text="Nombre visible para usuarios normales"
    )
    faction_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    # Fachada para facciones clasificadas
    is_classified = models.BooleanField(default=False)
    facade_name = models.CharField(
        max_length=100, blank=True, help_text="Nombre visible代替 real"
    )

    # Visibilidad
    is_public = models.BooleanField(
        default=True,
        help_text="Si es False, solo admins y miembros pueden ver la facción",
    )
    allow_applications = models.BooleanField(
        default=True, help_text="Permitir solicitudes de ingreso públicas"
    )

    # Metadata
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#1a1a2e")

    # Líderes
    leaders = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="led_factions", blank=True
    )

    # Rango temporal por defecto para nuevos miembros
    default_rank = models.ForeignKey(
        "FactionRank",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_faction",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Facción"
        verbose_name_plural = "Facciones"
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name

    def get_visible_name(self, user=None):
        """Retorna el nombre según el nivel de acceso del usuario"""
        if self.is_classified and self.facade_name:
            if user:
                if getattr(user, "is_superuser", False):
                    return self.display_name
                if hasattr(user, "characters"):
                    highest_card = user.get_highest_access_card()
                    if highest_card and highest_card.level in ["L5", "L6"]:
                        return self.display_name
            return self.facade_name
        return self.display_name


class FactionDivision(models.Model):
    """
    Divisiones dentro de una facción.
    Cada facción puede tener hasta 5 divisiones.
    """

    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="divisions"
    )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(
        default=True, help_text="Si es False, solo líderes pueden ver la división"
    )

    # Tarjeta asociada a esta división
    access_card = models.ForeignKey(
        "AccessCard",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faction_divisions",
    )

    # Miembros de la división
    members = models.ManyToManyField(
        "characters.Character",
        related_name="division_memberships",
        blank=True,
    )

    class Meta:
        verbose_name = "División de Facción"
        verbose_name_plural = "Divisiones de Facción"
        unique_together = ("faction", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.faction.display_name} - {self.name}"


class FactionDivisionRank(models.Model):
    """
    Rangos dentro de una división.
    """

    division = models.ForeignKey(
        FactionDivision, on_delete=models.CASCADE, related_name="ranks"
    )
    name = models.CharField(max_length=50)
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ("division", "name")
        ordering = ["level"]

    def __str__(self):
        return f"{self.division.name} - {self.name}"


class FactionRank(models.Model):
    """
    Rangos dentro de una facción con tarjeta asignada.
    """

    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, related_name="ranks")
    name = models.CharField(max_length=50)
    level = models.PositiveSmallIntegerField(
        default=1, help_text="Nivel jerárquico (1=más bajo)"
    )

    # Tarjeta asociada a este rango
    access_card = models.ForeignKey(
        AccessCard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faction_ranks",
    )

    # Permisos especiales del rango
    can_manage_members = models.BooleanField(default=False)
    can_review_applications = models.BooleanField(default=False)
    can_assign_ranks = models.BooleanField(default=False)

    class Meta:
        unique_together = ("faction", "name")
        ordering = ["faction", "-level"]
        verbose_name = "Rango de Facción"
        verbose_name_plural = "Rangos de Facción"

    def __str__(self):
        return f"{self.faction.display_name} - {self.name}"


class CharacterFactionMembership(models.Model):
    """
    Membresía de un personaje en una facción.
    Un personaje solo puede estar en una facción activa.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        CLASSIFIED = "classified", "Clasificado"

    character = models.ForeignKey(
        "characters.Character",
        on_delete=models.CASCADE,
        related_name="faction_memberships",
    )
    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="memberships"
    )
    rank = models.ForeignKey(
        FactionRank, on_delete=models.SET_NULL, null=True, blank=True
    )
    access_card = models.ForeignKey(
        AccessCard, on_delete=models.SET_NULL, null=True, blank=True
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("character", "faction")
        verbose_name = "Membresía de Personaje"
        verbose_name_plural = "Membresías de Personajes"

    def __str__(self):
        return f"{self.character.codename} - {self.faction.display_name}"

    def clean(self):
        if self.faction.status != Faction.Status.ACTIVE:
            raise ValidationError("No puedes unirte a una facción inactiva")


class FactionApplication(models.Model):
    """
    Solicitudes de ingreso a facciones.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        ACCEPTED = "accepted", "Aceptada"
        REJECTED = "rejected", "Rechazada"

    character = models.ForeignKey(
        "characters.Character",
        on_delete=models.CASCADE,
        related_name="faction_applications",
    )
    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="applications"
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    message = models.TextField(blank=True, help_text="Mensaje del solicitante")

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitud de Ingreso"
        verbose_name_plural = "Solicitudes de Ingreso"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.character.codename} -> {self.faction.display_name}"

    def clean(self):
        from django.db.models import Q

        if CharacterFactionMembership.objects.filter(
            character=self.character, status=CharacterFactionMembership.Status.ACTIVE
        ).exists():
            raise ValidationError("El personaje ya tiene una membresía activa")

        pending_exists = FactionApplication.objects.filter(
            character=self.character, status=self.Status.PENDING
        ).exists()
        if pending_exists:
            raise ValidationError(
                "Ya existe una solicitud pendiente para este personaje"
            )


class FactionLog(models.Model):
    """
    Logs de acciones en facciones (ascensos, expulsiones, etc.)
    """

    class ActionType(models.TextChoices):
        MEMBER_JOINED = "member_joined", "Miembro se unió"
        MEMBER_LEFT = "member_left", "Miembro salió"
        RANK_CHANGED = "rank_changed", "Rango cambiado"
        MEMBER_EXPELLED = "member_expelled", "Miembro expulsado"
        APPLICATION_ACCEPTED = "application_accepted", "Solicitud aceptada"
        APPLICATION_REJECTED = "application_rejected", "Solicitud rechazada"
        FACTION_CREATED = "faction_created", "Facción creada"
        FACTION_DISSOLVED = "faction_disolved", "Facción disuelta"

    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, related_name="logs")
    action_type = models.CharField(max_length=30, choices=ActionType.choices)

    character = models.ForeignKey(
        "characters.Character",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faction_logs",
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faction_actions",
    )

    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Facción"
        verbose_name_plural = "Logs de Facciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.faction.display_name} - {self.get_action_type_display()}"


class FactionInvitation(models.Model):
    """
    Invitaciones a facciones privadas.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        ACCEPTED = "accepted", "Aceptada"
        DECLINED = "declined", "Rechazada"
        EXPIRED = "expired", "Expirada"

    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="invitations"
    )
    # Usuario invitado (puede tener varios personajes)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="faction_invitations",
        null=True,
        blank=True,
    )
    # Personaje invitado (legacy, para backwards compatibility)
    character = models.ForeignKey(
        "characters.Character",
        on_delete=models.CASCADE,
        related_name="faction_invitations",
        null=True,
        blank=True,
    )

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_invitations",
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    message = models.TextField(blank=True)

    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Invitación de Facción"
        verbose_name_plural = "Invitaciones de Facciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.character.codename} -> {self.faction.display_name}"

    def accept(self):
        self.status = self.Status.ACCEPTED
        self.responded_at = timezone.now()
        self.save()

        lowest_rank = self.faction.ranks.order_by("level").first()
        access_card = (
            lowest_rank.access_card if lowest_rank else AccessCard.get_default_card()
        )

        # Reactivar si ya existió una membresía (unique_together character+faction)
        CharacterFactionMembership.objects.update_or_create(
            character=self.character,
            faction=self.faction,
            defaults={
                "rank": lowest_rank,
                "access_card": access_card,
                "status": CharacterFactionMembership.Status.ACTIVE,
                "left_at": None,
            },
        )

    def decline(self):
        self.status = self.Status.DECLINED
        self.responded_at = timezone.now()
        self.save()


from django.utils import timezone
