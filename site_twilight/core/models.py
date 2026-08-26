# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class SiteState(models.Model):
    ssu_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get(cls):
        """Estado global del sitio. Es una fila unica, siempre pk=1."""
        state, _ = cls.objects.get_or_create(pk=1, defaults={"ssu_status": False})
        return state

    def __str__(self):
        return f"Site State - SSU: {'ON' if self.ssu_status else 'OFF'}"

class SSUToggleLog(models.Model):
    ACTION_CHOICES = [
        ('ACTIVATED', 'Activado'),
        ('DEACTIVATED', 'Desactivado'),
    ]
    
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ssu_toggles'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    old_status = models.BooleanField()
    new_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        user_name = self.user.roblox_username if self.user else 'SYSTEM'
        return f"{user_name} - {self.action} at {self.created_at}"

class AIQueryLog(models.Model):
    """
    Log de consultas a la AI de Consulta (spec §7).
    "Todas las consultas sensibles quedan logueadas."
    """

    class Mode(models.TextChoices):
        RP = "rp", "In-RP"
        TECHNICAL = "technical", "Técnico"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="ai_queries",
    )
    mode = models.CharField(max_length=16, choices=Mode.choices, default=Mode.RP)
    access_level = models.CharField(max_length=4, default="L1")
    query = models.TextField()
    response = models.TextField(blank=True)
    used_llm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Consulta AI"
        verbose_name_plural = "Consultas AI"

    def __str__(self):
        user_name = self.user.roblox_username if self.user else "?"
        return f"{user_name} [{self.access_level}] {self.query[:40]}"
