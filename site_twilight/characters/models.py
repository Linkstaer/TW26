from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, URLValidator

User = settings.AUTH_USER_MODEL


class Character(models.Model):
    # Estado del personaje (spec §4.1)
    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        CLASSIFIED = "classified", "Clasificado"
        DELETED = "deleted", "Eliminado"

    # === Datos base ===
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")

    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ACTIVE
    )

    first_name = models.CharField(max_length=64, validators=[MaxLengthValidator(64)])
    last_name = models.CharField(max_length=64, validators=[MaxLengthValidator(64)])
    country = models.CharField(max_length=64, validators=[MaxLengthValidator(64)])
    birth_date = models.DateField()

    codename = models.CharField(max_length=32, validators=[MaxLengthValidator(32)])

    # Foto del personaje. Se guarda el enlace y no el archivo: el contenedor
    # de Railway es efimero y cualquier subida se perderia en cada redeploy.
    photo_url = models.URLField(
        max_length=500,
        blank=True,
        default="",
        validators=[URLValidator(schemes=["http", "https"])],
        help_text="Enlace directo a la imagen (Discord, imgur, etc.)",
    )
    # Campo legacy de texto; la pertenencia real vive en CharacterFactionMembership.
    # Opcional: un personaje puede estar sin facción (spec §1.3).
    faction = models.CharField(
        max_length=32, blank=True, default="", validators=[MaxLengthValidator(64)]
    )

    lore = models.CharField(max_length=5000, blank=True, validators=[MaxLengthValidator(5000)])

    # === Morph data (todos opcionales) ===
    morph = models.CharField(max_length=100, blank=True, validators=[MaxLengthValidator(100)])
    hat = models.CharField(max_length=100, blank=True, validators=[MaxLengthValidator(100)])

    nvg_color = models.CharField(max_length=16, blank=True, validators=[MaxLengthValidator(16)])

    shirt = models.CharField(max_length=64, blank=True, validators=[MaxLengthValidator(64)])
    pants = models.CharField(max_length=64, blank=True, validators=[MaxLengthValidator(64)])

    skin_r = models.PositiveSmallIntegerField(null=True, blank=True)
    skin_g = models.PositiveSmallIntegerField(null=True, blank=True)
    skin_b = models.PositiveSmallIntegerField(null=True, blank=True)

    ntag = models.CharField(max_length=64, blank=True, validators=[MaxLengthValidator(64)])
    
    # CAMBIO: Default 255 255 255 para cntag
    cntag_r = models.PositiveSmallIntegerField(null=True, blank=True, default=255)
    cntag_g = models.PositiveSmallIntegerField(null=True, blank=True, default=255)
    cntag_b = models.PositiveSmallIntegerField(null=True, blank=True, default=255)

    rtag = models.TextField(max_length=500, blank=True, validators=[MaxLengthValidator(500)])
    
    # CAMBIO: Default 255 255 255 para crtag
    crtag_r = models.PositiveSmallIntegerField(null=True, blank=True, default=255)
    crtag_g = models.PositiveSmallIntegerField(null=True, blank=True, default=255)
    crtag_b = models.PositiveSmallIntegerField(null=True, blank=True, default=255)

    rhat = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # Métodos de validación adicionales
    def clean(self):
        # Validación de campos de color
        if self.skin_r is not None and not (0 <= self.skin_r <= 255):
            raise ValidationError({'skin_r': 'El valor de skin_r debe estar entre 0 y 255'})
        if self.skin_g is not None and not (0 <= self.skin_g <= 255):
            raise ValidationError({'skin_g': 'El valor de skin_g debe estar entre 0 y 255'})
        if self.skin_b is not None and not (0 <= self.skin_b <= 255):
            raise ValidationError({'skin_b': 'El valor de skin_b debe estar entre 0 y 255'})
            
        if self.cntag_r is not None and not (0 <= self.cntag_r <= 255):
            raise ValidationError({'cntag_r': 'El valor de cntag_r debe estar entre 0 y 255'})
        if self.cntag_g is not None and not (0 <= self.cntag_g <= 255):
            raise ValidationError({'cntag_g': 'El valor de cntag_g debe estar entre 0 y 255'})
        if self.cntag_b is not None and not (0 <= self.cntag_b <= 255):
            raise ValidationError({'cntag_b': 'El valor de cntag_b debe estar entre 0 y 255'})
            
        if self.crtag_r is not None and not (0 <= self.crtag_r <= 255):
            raise ValidationError({'crtag_r': 'El valor de crtag_r debe estar entre 0 y 255'})
        if self.crtag_g is not None and not (0 <= self.crtag_g <= 255):
            raise ValidationError({'crtag_g': 'El valor de crtag_g debe estar entre 0 y 255'})
        if self.crtag_b is not None and not (0 <= self.crtag_b <= 255):
            raise ValidationError({'crtag_b': 'El valor de crtag_b debe estar entre 0 y 255'})

        # Validación de que al menos un campo de morph esté definido
        morph_fields = [
            self.morph, self.hat, self.nvg_color,
            self.shirt, self.pants,
            self.skin_r, self.skin_g, self.skin_b,
            self.ntag, self.cntag_r, self.cntag_g, self.cntag_b,
            self.rtag, self.crtag_r, self.crtag_g, self.crtag_b,
        ]
        if not any(field for field in morph_fields if field not in (None, '')):
            raise ValidationError("Al menos un campo de morph debe estar definido.")

    # Meta para mejorar la organización
    class Meta:
        verbose_name = "Personaje"
        verbose_name_plural = "Personajes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['codename']),
            models.Index(fields=['owner', 'created_at']),
            models.Index(fields=['faction']),
        ]

    # ============================
    # Roblox command builder ACTUALIZADO
    # ============================
    def morph_command(self):
        cmds = []
        
        # Obtener el nombre de usuario del owner
        username = self.owner.roblox_username if hasattr(self.owner, 'roblox_username') else str(self.owner)
        
        # Construir comandos individuales
        if self.morph:
            cmd = f"permmorph {username} {self.morph}"
            if self.rhat:
                cmd += f" & rhat {username}"
            cmds.append(cmd)
        
        if self.hat:
            cmds.append(f"permhat {username} {self.hat}")
        
        if self.shirt:
            cmds.append(f"permshirt {username} {self.shirt}")
        
        if self.pants:
            cmds.append(f"permpants {username} {self.pants}")
        
        if self.nvg_color:
            cmds.append(f"permcolornvg {username} {self.nvg_color}")
        
        if all(v is not None for v in [self.skin_r, self.skin_g, self.skin_b]):
            cmds.append(
                f"permskin {username} "
                f"{self.skin_r} {self.skin_g} {self.skin_b}"
            )
        
        if self.ntag:
            # Escapar comillas para el comando
            ntag_escaped = self.ntag.replace('"', '\\"')
            cmds.append(f'permntag {username} "{ntag_escaped}"')
        
        # CNTag - usar defaults solo si son 0
        cntag_r = self.cntag_r if self.cntag_r != 0 else 255
        cntag_g = self.cntag_g if self.cntag_g != 0 else 255
        cntag_b = self.cntag_b if self.cntag_b != 0 else 255
        
        cmds.append(
            f"permcntag {username} "
            f"{cntag_r} {cntag_g} {cntag_b}"
        )
        
        if self.rtag:
            # Escapar comillas para el comando
            rtag_escaped = self.rtag.replace('"', '\\"')
            cmds.append(f"permrtag {username} \"{rtag_escaped}\"")
        
        # CRTag - usar defaults solo si son 0
        crtag_r = self.crtag_r if self.crtag_r != 0 else 255
        crtag_g = self.crtag_g if self.crtag_g != 0 else 255
        crtag_b = self.crtag_b if self.crtag_b != 0 else 255
        
        cmds.append(
            f"permcrtag {username} "
            f"{crtag_r} {crtag_g} {crtag_b}"
        )
        
        # Agregar "run " al inicio y unir comandos con " & "
        if cmds:
            return f"run {' & '.join(cmds)}"
        return ""

    @property
    def is_scp_actor(self) -> bool:
        """El personaje interpreta a un SCP (spec §3.4)."""
        return hasattr(self, "scp_file") and self.scp_file is not None

    def get_scp_actor_data(self):
        """
        Archivo SCP que interpreta este personaje, para mostrarlo en su perfil
        (spec §3.4). None si no es Actor SCP.
        """
        scp = getattr(self, "scp_file", None)
        if scp is None or scp.is_deleted:
            return None
        return {
            "id": scp.id,
            "scp_id": scp.scp_id,
            "title": scp.title,
            "object_class": scp.object_class,
            "object_class_display": scp.get_object_class_display(),
        }

    def get_access_level(self) -> str:
        """
        Nivel de la tarjeta asignada al personaje vía su membresía activa (spec §1.3).
        Sin membresía o sin tarjeta => L1.
        """
        from factions.models import CharacterFactionMembership

        membership = (
            self.faction_memberships.filter(
                status=CharacterFactionMembership.Status.ACTIVE
            )
            .select_related("access_card")
            .first()
        )
        if membership and membership.access_card:
            return membership.access_card.level
        return "L1"

    def __str__(self):
        return f"{self.codename} ({self.owner})"
    
    def to_dict(self):
        skin_data = {
            "skin_r": self.skin_r,
            "skin_g": self.skin_g,
            "skin_b": self.skin_b,
        }
        
        cntag_data = {
            "cntag_r": 255 if self.cntag_r is None else self.cntag_r,
            "cntag_g": 255 if self.cntag_g is None else self.cntag_g,
            "cntag_b": 255 if self.cntag_b is None else self.cntag_b,
        }
        
        crtag_data = {
            "crtag_r": 255 if self.crtag_r is None else self.crtag_r,
            "crtag_g": 255 if self.crtag_g is None else self.crtag_g,
            "crtag_b": 255 if self.crtag_b is None else self.crtag_b,
        }
        
        return {
            "id": self.id,
            "codename": self.codename,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "country": self.country,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "faction": self.faction,
            "lore": self.lore,
            "owner_username": self.owner.roblox_username,
            "owner_id": self.owner.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "morph": self.morph,
            "hat": self.hat,
            # nvg es un solo campo de texto (nvg_color). Antes esto leía
            # self.nvg_r/g/b, que no existen en el modelo: cualquier llamada
            # a to_dict() reventaba con AttributeError.
            "nvg_color": self.nvg_color,
            "shirt": self.shirt,
            "pants": self.pants,
            **skin_data,
            "ntag": self.ntag,
            **cntag_data,
            "rtag": self.rtag,
            **crtag_data,
            "rhat": self.rhat,
            "morph_command": self.morph_command(),
        }