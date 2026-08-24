from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta
from .permissions import STAFF_PERMISSIONS

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, roblox_id, password=None, **extra_fields):
        if not roblox_id:
            raise ValueError("El usuario debe tener roblox_id")

        user = self.model(roblox_id=roblox_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, roblox_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(roblox_id, password, **extra_fields)


class User(AbstractUser):
    # Disable normal auth
    username = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128, blank=True)

    roblox_id = models.BigIntegerField(unique=True, null=True, blank=True)
    roblox_username = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "roblox_id"

    objects = UserManager()

    first_login = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Moderación fields
    warning_count = models.PositiveIntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    banned_until = models.DateTimeField(null=True, blank=True)
    banned_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="banned_users",
    )

    # Not RP related, only Django Backend
    is_staff = models.BooleanField(default=False)  # Django admin
    is_superuser = models.BooleanField(default=False)  # Django super admin

    # Boosters: pueden enviar sugerencias de lore (spec, sección final)
    is_booster = models.BooleanField(default=False)

    def has_permission(self, permission: str) -> bool:
        print(f"Checking permission '{permission}' for user {self.username}")  # Debug

        # Check superuser first
        if self.is_superuser:
            print("User is superuser - all permissions granted")
            return True

        # Check staff permissions
        for role in self.staff_roles.all():
            perms_by_level = STAFF_PERMISSIONS.get(role.scope, {})
            for lvl in range(1, role.level + 1):
                if permission in perms_by_level.get(lvl, set()):
                    print(
                        f"Permission '{permission}' found in role {role.scope} level {lvl}"
                    )
                    return True

        print(f"Permission '{permission}' not found for user")
        return False

    def update_warning_count(self):
        """Actualiza el conteo de warns activos (no expirados, no apelados)"""
        active_warns = self.warns.filter(appealed=False, expires_at__gt=timezone.now())
        self.warning_count = active_warns.count()
        self.save(update_fields=["warning_count"])
        return self.warning_count

    def check_ban_status(self):
        """Verifica si el ban ha expirado y lo limpia si es necesario"""
        if self.is_banned and self.banned_until:
            if timezone.now() > self.banned_until:
                self.is_banned = False
                self.ban_reason = ""
                self.banned_until = None
                self.banned_by = None
                self.save()
                return False
        return self.is_banned

    def get_highest_access_card(self):
        """
        Retorna la tarjeta de acceso más alta de todos los personajes del usuario.
        Determina el nivel de acceso global del usuario.
        """
        try:
            from factions.models import CharacterFactionMembership, AccessCard

            memberships = CharacterFactionMembership.objects.filter(
                character__owner=self, status=CharacterFactionMembership.Status.ACTIVE
            ).select_related("access_card")

            if not memberships.exists():
                return AccessCard.get_default_card()

            level_priority = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6}

            highest_card = None
            highest_level = 0

            for membership in memberships:
                if membership.access_card:
                    card_level = level_priority.get(membership.access_card.level, 0)
                    if card_level > highest_level:
                        highest_card = membership.access_card
                        highest_level = card_level

            if not highest_card:
                return AccessCard.get_default_card()

            # La regla de seguridad L5/Comité de Ética (spec §2.4) vive en
            # AccessCard.display_name, que ahora es una property derivada.
            return highest_card

        except ImportError:
            return None

    def get_visible_factions(self):
        """
        Retorna las fachadas de las facciones de los personajes del usuario.
        Aplica reglas de fachadas para facciones clasificadas.
        """
        from factions.models import CharacterFactionMembership, Faction

        memberships = CharacterFactionMembership.objects.filter(
            character__owner=self, status=CharacterFactionMembership.Status.ACTIVE
        ).select_related("faction")

        visible_factions = []
        for membership in memberships:
            faction = membership.faction
            visible_factions.append(
                {
                    "id": faction.id,
                    "name": faction.get_visible_name(self),
                    "rank": membership.rank.name if membership.rank else None,
                    "is_classified": faction.is_classified,
                    "real_name": faction.name
                    if self.is_superuser
                    or (self.has_permission("view_classified_factions"))
                    else None,
                }
            )

        return visible_factions

    def get_accessible_levels(self):
        """
        Retorna los niveles de acceso que el usuario puede ver según su tarjeta más alta.
        """
        card = self.get_highest_access_card()
        if not card:
            return ["L1"]

        levels = []
        if card.can_view_l1:
            levels.append("L1")
        if card.can_view_l2:
            levels.append("L2")
        if card.can_view_l3:
            levels.append("L3")
        if card.can_view_l4:
            levels.append("L4")
        if card.can_view_l5:
            levels.append("L5")
        if card.can_view_l6:
            levels.append("L6")

        return levels

    def __str__(self):
        return f"Usuario {self.roblox_username} #{self.roblox_id}"

    def get_appeal_cooldown(self):
        """Verifica si el usuario puede apelar (máximo 1 por semana)"""
        from django.utils import timezone
        from datetime import timedelta

        # Buscar la última apelación (warn o ban)
        last_warn_appeal = (
            self.warns.filter(appealed=True).order_by("-appealed_at").first()
        )
        last_ban_appeal = (
            self.bans_received.filter(appealed=True).order_by("-appealed_at").first()
        )

        # Encontrar la apelación más reciente
        last_appeal_date = None
        if last_warn_appeal and last_warn_appeal.appealed_at:
            last_appeal_date = last_warn_appeal.appealed_at
        if last_ban_appeal and last_ban_appeal.appealed_at:
            if not last_appeal_date or last_ban_appeal.appealed_at > last_appeal_date:
                last_appeal_date = last_ban_appeal.appealed_at

        if last_appeal_date:
            # Verificar si ha pasado una semana
            cooldown_end = last_appeal_date + timedelta(days=7)
            if timezone.now() < cooldown_end:
                return {
                    "can_appeal": False,
                    "cooldown_ends": cooldown_end.isoformat(),
                    "reason": f"Debes esperar hasta {cooldown_end.strftime('%d/%m/%Y %H:%M')} para apelar nuevamente",
                }

        return {"can_appeal": True, "cooldown_ends": None, "reason": None}


class StaffRole(models.Model):
    class Scope(models.TextChoices):
        GLOBAL = "global", "Administración Global"
        MODERATION = "moderation", "Moderación General"
        INGAME = "ingame", "Moderación In-Game"
        DISCORD = "discord", "Moderación Discord"
        RP_ROLEPLAY = "rp_roleplay", "Equipo Roleplay"
        RP_FACTION = "rp_faction", "Moderación Facciones"
        RP_ACTORS = "rp_actors", "Supervisión Actores"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="staff_roles",
    )

    scope = models.CharField(
        max_length=20,
        choices=Scope.choices,
    )

    level = models.PositiveSmallIntegerField(
        help_text="Nivel más alto = más permisos", default=1
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "scope")
        verbose_name = "Rol de Staff"
        verbose_name_plural = "Roles de Staff"

    def __str__(self):
        nivel_texto = self.get_level_display()
        return f"{self.user} | {self.get_scope_display()} {nivel_texto}"

    def get_scope_display(self):
        """Return human-readable scope name"""
        return dict(self.Scope.choices).get(self.scope, self.scope)

    def get_level_display(self):
        """Return human-readable level name based on scope"""
        level_names = {
            "global": {1: "SSU Host", 2: "Admin+"},
            "moderation": {1: "Junior", 2: "Official", 3: "Qualified", 4: "Senior"},
            "ingame": {1: "Junior", 2: "Official", 3: "Qualified"},
            "discord": {1: "Junior", 2: "Official", 3: "Qualified", 4: "Senior"},
            "rp_roleplay": {1: "RP Team", 2: "RP Lead"},
            "rp_faction": {1: "Faction Team", 2: "RP Lead"},
            "rp_actors": {1: "SCP Team", 2: "SCP Lead"},
        }

        scope_levels = level_names.get(self.scope, {})
        return scope_levels.get(self.level, f"Nivel {self.level}")


class Warn(models.Model):
    class WarnStatus(models.TextChoices):
        ACTIVE = "active", "Activo"
        EXPIRED = "expired", "Expirado"
        APPEALED = "appealed", "Apelado"
        REMOVED = "removed", "Removido"

    target = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="warns"
    )

    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="issued_warns"
    )

    reason = models.TextField()
    evidence = models.TextField(
        blank=True, help_text="Enlaces a evidencia (Discord, videos, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Sistema de apelación
    appealed = models.BooleanField(default=False)
    appealed_at = models.DateTimeField(null=True, blank=True)
    appealed_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appealed_warns",
    )
    appeal_response = models.TextField(
        blank=True, help_text="Respuesta del moderador a la apelación"
    )
    appeal_responded_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responded_appeals",
    )
    appeal_responded_at = models.DateTimeField(null=True, blank=True)

    # Expiración
    expires_at = models.DateTimeField(null=True, blank=True)
    expires_after_days = models.PositiveIntegerField(
        default=30, help_text="Días hasta que expire el warn"
    )

    # Metadatos
    severity = models.PositiveSmallIntegerField(
        default=1,
        choices=[(1, "Bajo"), (2, "Medio"), (3, "Alto")],
        help_text="Severidad del warn",
    )
    status = models.CharField(
        max_length=20, choices=WarnStatus.choices, default=WarnStatus.ACTIVE
    )

    # Nuevos campos para control de apelaciones
    appeal_message = models.TextField(
        blank=True, help_text="Mensaje de apelación del usuario"
    )
    last_appealed = models.DateTimeField(
        null=True, blank=True, help_text="Última vez que se apeló"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target", "status"]),
            models.Index(fields=["expires_at"]),
        ]

    def save(self, *args, **kwargs):
        """Set expires_at if not set"""
        if not self.expires_at and self.expires_after_days:
            self.expires_at = timezone.now() + timedelta(days=self.expires_after_days)

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Actualizar conteo de warns del usuario
            self.target.update_warning_count()

    def check_expiration(self):
        """Verifica si el warn ha expirado"""
        if (
            self.expires_at
            and timezone.now() > self.expires_at
            and self.status == self.WarnStatus.ACTIVE
        ):
            self.status = self.WarnStatus.EXPIRED
            self.save(update_fields=["status"])
            self.target.update_warning_count()
            return True
        return False

    def can_be_appealed(self):
        """Verifica si este warn puede ser apelado"""
        from django.utils import timezone
        from datetime import timedelta

        # No apelar si ya está apelado
        if self.appealed:
            return False, "Ya has apelado esta advertencia"

        # Verificar cooldown del usuario
        user_cooldown = self.target.get_appeal_cooldown()
        if not user_cooldown["can_appeal"]:
            return False, user_cooldown["reason"]

        # Verificar si el warn está activo
        if self.status != self.WarnStatus.ACTIVE:
            return False, "Esta advertencia no está activa"

        # Verificar si no ha expirado
        if self.expires_at and timezone.now() > self.expires_at:
            return False, "Esta advertencia ha expirado"

        return True, "Puede ser apelado"

    def appeal(self, appealed_by=None, appeal_message=""):
        """Marca el warn como apelado con cooldown"""
        from django.utils import timezone

        can_appeal, reason = self.can_be_appealed()
        if not can_appeal:
            raise ValueError(reason)

        self.appealed = True
        self.appealed_at = timezone.now()
        self.last_appealed = timezone.now()
        self.appeal_message = appeal_message
        if appealed_by:
            self.appealed_by = appealed_by
        self.save()
        self.target.update_warning_count()

        return True

    def respond_to_appeal(self, response, responder):
        """Responde a una apelación"""
        if self.appealed:
            self.appeal_response = response
            self.appeal_responded_by = responder
            self.appeal_responded_at = timezone.now()

            # Si se acepta la apelación, marcar como removido
            if "aceptado" in response.lower() or "aceptada" in response.lower():
                self.status = self.WarnStatus.REMOVED
                self.target.update_warning_count()

            self.save()

    @property
    def is_active(self):
        return self.status == self.WarnStatus.ACTIVE and not self.appealed

    def __str__(self):
        return f"Warn #{self.id} -> {self.target.roblox_username}"


class Ban(models.Model):
    class BanType(models.TextChoices):
        TEMPORARY = "temporary", "Temporal"
        PERMANENT = "permanent", "Permanente"

    target = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="bans_received"
    )

    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="issued_bans"
    )

    reason = models.TextField()
    evidence = models.TextField(blank=True, help_text="Enlaces a evidencia")
    created_at = models.DateTimeField(auto_now_add=True)

    # Duración del ban
    ban_type = models.CharField(
        max_length=20, choices=BanType.choices, default=BanType.TEMPORARY
    )
    duration_days = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duración en días (solo para bans temporales)"
    )
    ends_at = models.DateTimeField(null=True, blank=True)

    # Sistema de apelación
    can_appeal = models.BooleanField(default=True)
    appealed = models.BooleanField(default=False)
    appealed_at = models.DateTimeField(null=True, blank=True)
    appeal_response = models.TextField(blank=True)
    appeal_responded_by = models.ForeignKey(  # Asegúrate de que este campo existe
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responded_ban_appeals",  # Usa un related_name diferente
    )
    appeal_responded_at = models.DateTimeField(null=True, blank=True)

    # Estado
    is_active = models.BooleanField(default=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    revoked_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revoked_bans",
    )
    revocation_reason = models.TextField(blank=True)

    # Nuevo campo para mensaje de apelación
    appeal_message = models.TextField(
        blank=True, help_text="Mensaje de apelación del usuario"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target", "is_active"]),
            models.Index(fields=["ends_at"]),
        ]

    def save(self, *args, **kwargs):
        """Configura fechas y actualiza estado del usuario"""
        if (
            self.ban_type == Ban.BanType.TEMPORARY
            and self.duration_days
            and not self.ends_at
        ):
            self.ends_at = timezone.now() + timedelta(days=self.duration_days)

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.is_active:
            # Actualizar estado del usuario
            self.target.is_banned = True
            self.target.ban_reason = self.reason
            self.target.banned_until = self.ends_at
            self.target.banned_by = self.created_by
            self.target.save()

    def revoke(self, revoker, reason=""):
        """Revoca un ban activo"""
        if self.is_active:
            self.is_active = False
            self.revoked_at = timezone.now()
            self.revoked_by = revoker
            self.revocation_reason = reason
            self.save()

            # Actualizar estado del usuario
            self.target.is_banned = False
            self.target.ban_reason = ""
            self.target.banned_until = None
            self.target.banned_by = None
            self.target.save()

    def check_expiration(self):
        """Verifica si un ban temporal ha expirado"""
        if self.ban_type == Ban.BanType.TEMPORARY and self.ends_at and self.is_active:
            if timezone.now() > self.ends_at:
                self.revoke(revoker=None, reason="Expirado automáticamente")
                return True
        return False

    def can_be_appealed(self):
        """Verifica si este ban puede ser apelado"""
        from django.utils import timezone

        # Verificar si permite apelación
        if not self.can_appeal:
            return False, "Este baneo no permite apelaciones"

        # No apelar si ya está apelado
        if self.appealed:
            return False, "Ya has apelado este baneo"

        # Verificar si está activo
        if not self.is_active:
            return False, "Este baneo no está activo"

        # Verificar cooldown del usuario
        user_cooldown = self.target.get_appeal_cooldown()
        if not user_cooldown["can_appeal"]:
            return False, user_cooldown["reason"]

        return True, "Puede ser apelado"

    def appeal(self, appealed_by=None, appeal_message=""):
        """Marca el ban como apelado"""
        from django.utils import timezone

        can_appeal, reason = self.can_be_appealed()
        if not can_appeal:
            raise ValueError(reason)

        self.appealed = True
        self.appealed_at = timezone.now()
        self.appeal_message = appeal_message
        self.save()

        return True

    @property
    def is_permanent(self):
        return self.ban_type == Ban.BanType.PERMANENT

    def __str__(self):
        ban_type = "Permanente" if self.is_permanent else "Temporal"
        return f"Ban {ban_type} -> {self.target.roblox_username}"

    class BanType(models.TextChoices):
        TEMPORARY = "temporary", "Temporal"
        PERMANENT = "permanent", "Permanente"

    target = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="bans_received"
    )

    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="issued_bans"
    )

    reason = models.TextField()
    evidence = models.TextField(blank=True, help_text="Enlaces a evidencia")
    created_at = models.DateTimeField(auto_now_add=True)

    # Duración del ban
    ban_type = models.CharField(
        max_length=20, choices=BanType.choices, default=BanType.TEMPORARY
    )
    duration_days = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duración en días (solo para bans temporales)"
    )
    ends_at = models.DateTimeField(null=True, blank=True)

    # Sistema de apelación
    can_appeal = models.BooleanField(default=True)
    appealed = models.BooleanField(default=False)
    appealed_at = models.DateTimeField(null=True, blank=True)
    appeal_response = models.TextField(blank=True)

    # Estado
    is_active = models.BooleanField(default=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    revoked_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revoked_bans",
    )
    revocation_reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target", "is_active"]),
            models.Index(fields=["ends_at"]),
        ]

    def save(self, *args, **kwargs):
        """Configura fechas y actualiza estado del usuario"""
        if (
            self.ban_type == Ban.BanType.TEMPORARY
            and self.duration_days
            and not self.ends_at
        ):
            self.ends_at = timezone.now() + timedelta(days=self.duration_days)

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.is_active:
            # Actualizar estado del usuario
            self.target.is_banned = True
            self.target.ban_reason = self.reason
            self.target.banned_until = self.ends_at
            self.target.banned_by = self.created_by
            self.target.save()

    def revoke(self, revoker, reason=""):
        """Revoca un ban activo"""
        if self.is_active:
            self.is_active = False
            self.revoked_at = timezone.now()
            self.revoked_by = revoker
            self.revocation_reason = reason
            self.save()

            # Actualizar estado del usuario
            self.target.is_banned = False
            self.target.ban_reason = ""
            self.target.banned_until = None
            self.target.banned_by = None
            self.target.save()

    def check_expiration(self):
        """Verifica si un ban temporal ha expirado"""
        if self.ban_type == Ban.BanType.TEMPORARY and self.ends_at and self.is_active:
            if timezone.now() > self.ends_at:
                self.revoke(revoker=None, reason="Expirado automáticamente")
                return True
        return False

    @property
    def is_permanent(self):
        return self.ban_type == Ban.BanType.PERMANENT

    def __str__(self):
        ban_type = "Permanente" if self.is_permanent else "Temporal"
        return f"Ban {ban_type} -> {self.target.roblox_username}"

    appeal_message = models.TextField(
        blank=True, help_text="Mensaje de apelación del usuario"
    )

    def can_be_appealed(self):
        """Verifica si este ban puede ser apelado"""
        from django.utils import timezone

        # Verificar si permite apelación
        if not self.can_appeal:
            return False, "Este baneo no permite apelaciones"

        # No apelar si ya está apelado
        if self.appealed:
            return False, "Ya has apelado este baneo"

        # Verificar si está activo
        if not self.is_active:
            return False, "Este baneo no está activo"

        # Verificar cooldown del usuario
        user_cooldown = self.target.get_appeal_cooldown()
        if not user_cooldown["can_appeal"]:
            return False, user_cooldown["reason"]

        return True, "Puede ser apelado"

    def appeal(self, appealed_by=None, appeal_message=""):
        """Marca el ban como apelado"""
        from django.utils import timezone

        can_appeal, reason = self.can_be_appealed()
        if not can_appeal:
            raise ValueError(reason)

        self.appealed = True
        self.appealed_at = timezone.now()
        self.appeal_message = appeal_message
        self.save()

        return True


class AuditLog(models.Model):
    class ActionType(models.TextChoices):
        # Permisos y usuarios
        USER_LOGIN = "user_login", "Inicio de sesión"
        USER_LOGOUT = "user_logout", "Cierre de sesión"
        PERMISSIONS_UPDATE = "permissions_update", "Actualización de permisos"
        ROLE_ASSIGNED = "role_assigned", "Rol asignado"
        ROLE_REMOVED = "role_removed", "Rol removido"

        # Moderación
        WARN_CREATED = "warn_created", "Advertencia creada"
        WARN_UPDATED = "warn_updated", "Advertencia actualizada"
        WARN_REMOVED = "warn_removed", "Advertencia eliminada"
        WARN_APPEALED = "warn_appealed", "Advertencia apelada"
        WARN_APPEAL_RESPONDED = "warn_appeal_responded", "Respuesta a apelación"

        # Baneos
        BAN_CREATED = "ban_created", "Baneo creado"
        BAN_REVOKED = "ban_revoked", "Baneo revocado"
        BAN_APPEALED = "ban_appealed", "Baneo apelado"
        BAN_APPEAL_RESPONDED = "ban_appeal_responded", "Respuesta a apelación de baneo"

        # Personajes
        CHARACTER_CREATED = "character_created", "Personaje creado"
        CHARACTER_UPDATED = "character_updated", "Personaje actualizado"
        CHARACTER_DELETED = "character_deleted", "Personaje eliminado"

        # Sistema
        SSU_STATUS_CHANGED = "ssu_status_changed", "Estado SSU cambiado"

        # Archivos RP
        RP_FILE_EDITED = "rp_file_edited", "Archivo RP editado"
        FACTION_MODERATED = "faction_moderated", "Facción moderada"
        ACTOR_SUPERVISED = "actor_supervised", "Actor supervisado"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="audit_logs",
        null=True,
        blank=True,
    )

    action_user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actions_performed",
        help_text="Usuario que realizó la acción",
    )

    action_type = models.CharField(max_length=50, choices=ActionType.choices)

    target_user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="targeted_audit_logs",
        help_text="Usuario afectado por la acción",
    )

    # Para referencias a otros modelos
    target_warn = models.ForeignKey(
        "users.Warn", on_delete=models.SET_NULL, null=True, blank=True
    )

    target_ban = models.ForeignKey(
        "users.Ban", on_delete=models.SET_NULL, null=True, blank=True
    )

    target_character = models.ForeignKey(
        "characters.Character", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Información detallada
    details = models.JSONField(
        default=dict, help_text="Detalles adicionales en formato JSON"
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action_type", "created_at"]),
            models.Index(fields=["action_user", "created_at"]),
            models.Index(fields=["target_user", "created_at"]),
        ]
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.created_at}"

    @classmethod
    def log_action(
        cls,
        request,
        action_type,
        target_user=None,
        target_warn=None,
        target_ban=None,
        target_character=None,
        details=None,
    ):
        """Método helper para crear logs de auditoría"""
        user = request.user if request.user.is_authenticated else None

        log_data = {
            "action_user": user,
            "action_type": action_type,
            "target_user": target_user,
            "target_warn": target_warn,
            "target_ban": target_ban,
            "target_character": target_character,
            "details": details or {},
            "ip_address": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        }

        return cls.objects.create(**log_data)


class UsernameHistory(models.Model):
    """
    Historial de usernames de Roblox (spec §1.1).
    Se registra cada vez que el callback OAuth detecta un cambio.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="username_history",
    )
    old_username = models.CharField(max_length=100)
    new_username = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Username"
        verbose_name_plural = "Historial de Usernames"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.user.roblox_id}: {self.old_username} -> {self.new_username}"
