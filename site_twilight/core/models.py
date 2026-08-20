# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class SiteState(models.Model):
    ssu_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
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