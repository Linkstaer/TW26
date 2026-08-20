from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator


class SCP(models.Model):
    """
    Archivos SCP con secciones segmentadas por nivel de acceso.
    """

    class ObjectClass(models.TextChoices):
        SAFE = "safe", "Safe"
        EUCLID = "euclid", "Euclid"
        KETER = "keter", "Keter"
        THAUMIEL = "thaumiel", "Thaumiel"
        NEUTRALIZED = "neutralized", "Neutralized"
        APOLLYON = "apollyon", "Apollyon"
        ARCHON = "archon", "Archon"

    scp_id = models.CharField(max_length=20, unique=True, help_text="ej: SCP-2995")
    title = models.CharField(max_length=200)
    object_class = models.CharField(
        max_length=20, choices=ObjectClass.choices, default=ObjectClass.EUCLID
    )

    # Contenido segmentado por nivel
    content_l1 = models.TextField(blank=True, validators=[MaxLengthValidator(50000)])
    content_l2 = models.TextField(blank=True, validators=[MaxLengthValidator(50000)])
    content_l3 = models.TextField(blank=True, validators=[MaxLengthValidator(50000)])
    content_l4 = models.TextField(blank=True, validators=[MaxLengthValidator(50000)])
    content_l5 = models.TextField(blank=True, validators=[MaxLengthValidator(50000)])
    content_l6 = models.TextField(blank=True, validators=[MaxLengthValidator(50000)])

    # Apéndices (cualquier nivel puede agregar)
    appendices = models.JSONField(
        default=list, help_text="Lista de apéndices con nivel y contenido"
    )

    # Estado
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="scps_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Actor SCP asociado (si es un personaje SCP)
    actor_character = models.OneToOneField(
        "characters.Character",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scp_file",
    )

    class Meta:
        verbose_name = "Archivo SCP"
        verbose_name_plural = "Archivos SCP"
        ordering = ["scp_id"]

    def __str__(self):
        return f"{self.scp_id} - {self.title}"

    def get_content_for_level(self, level: str) -> str:
        """Retorna el contenido según el nivel de acceso"""
        level_map = {
            "L1": self.content_l1,
            "L2": self.content_l2,
            "L3": self.content_l3,
            "L4": self.content_l4,
            "L5": self.content_l5,
            "L6": self.content_l6,
        }
        return level_map.get(level, "")

    def can_user_edit(self, user) -> tuple[bool, str]:
        """Verifica si el usuario puede editar este SCP"""
        if not user.is_authenticated:
            return False, "Debes iniciar sesión"

        if user.is_superuser:
            return True, "Acceso total como administrador"

        # Obtener tarjeta de acceso del usuario
        card = user.get_highest_access_card()
        if not card:
            return False, "Sin tarjeta de acceso"

        # O5 puede editar cualquier cosa
        if card.can_edit_any:
            return True, "Acceso total O5/Admin"

        # Actor SCP puede editar solo su archivo
        if self.actor_character:
            if user.characters.filter(id=self.actor_character.id).exists():
                return True, "Acceso como Actor SCP"

        return False, "Sin permisos para editar"

    def to_dict(self, user=None):
        """Serializa el SCP según el nivel de acceso del usuario"""
        data = {
            "id": self.id,
            "scp_id": self.scp_id,
            "title": self.title,
            "object_class": self.object_class,
            "appendices": self.appendices,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if user and user.is_authenticated:
            accessible_levels = user.get_accessible_levels()

            # Agregar contenido por nivel
            for level in accessible_levels:
                data[f"content_{level.lower()}"] = self.get_content_for_level(level)

        return data


class SCPEditLog(models.Model):
    """
    Versionado interno de ediciones de SCP.
    """

    scp = models.ForeignKey(SCP, on_delete=models.CASCADE, related_name="edit_logs")
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="scp_edits",
    )

    section = models.CharField(max_length=20, help_text="L1, L2, etc. o appendix")
    old_content = models.TextField(blank=True)
    new_content = models.TextField()

    edit_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Edición SCP"
        verbose_name_plural = "Logs de Edición SCP"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.scp.scp_id} - {self.section} - {self.created_at}"


class Document(models.Model):
    """
    Documentación interna del sitio.
    """

    class DocType(models.TextChoices):
        PROCEDURE = "procedure", "Procedimiento"
        MEMO = "memo", "Memo"
        BRIEFING = "briefing", "Briefing"
        REGULATION = "regulation", "Reglamento"
        OTHER = "other", "Otro"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    doc_type = models.CharField(
        max_length=20, choices=DocType.choices, default=DocType.OTHER
    )

    # Contenido en Markdown
    content = models.TextField(validators=[MaxLengthValidator(100000)])

    # Nivel de acceso requerido para ver
    min_access_level = models.CharField(max_length=10, default="L1")

    # Facción restrictiva (opcional)
    restricted_faction = models.ForeignKey(
        "factions.Faction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )

    # Autor
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents_authored",
    )

    # Facción del autor (para filtrar)
    author_faction = models.CharField(max_length=100, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def can_user_view(self, user) -> bool:
        """Verifica si el usuario puede ver este documento"""
        if not user.is_authenticated:
            return self.min_access_level == "L1"

        if user.is_superuser:
            return True

        accessible_levels = user.get_accessible_levels()
        level_priority = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6}

        user_level = max([level_priority.get(l, 0) for l in accessible_levels])
        required_level = level_priority.get(self.min_access_level, 1)

        if user_level < required_level:
            return False

        # Verificar restricción de facción
        if self.restricted_faction:
            user_factions = user.get_visible_factions()
            if not any(f["id"] == self.restricted_faction.id for f in user_factions):
                return False

        return True


class DocumentEditLog(models.Model):
    """
    Versionado de ediciones de documentos.
    """

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="edit_logs"
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="document_edits",
    )

    old_content = models.TextField(blank=True)
    new_content = models.TextField()

    edit_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Edición de Documento"
        verbose_name_plural = "Logs de Edición de Documentos"
        ordering = ["-created_at"]
