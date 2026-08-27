from django.core.management.base import BaseCommand
from users.models import User
import os


class Command(BaseCommand):
    help = "Ensure emergency admin user exists"

    def handle(self, *args, **options):
        username = os.getenv("EMERGENCY_ADMIN_USERNAME")
        password = os.getenv("EMERGENCY_ADMIN_PASSWORD")
        # USERNAME_FIELD es roblox_id, así que el login del admin de Django
        # se hace con este número, no con EMERGENCY_ADMIN_USERNAME.
        roblox_id = int(os.getenv("EMERGENCY_ADMIN_ROBLOX_ID", "1"))

        if not username or not password:
            self.stdout.write("Emergency admin vars not set, skipping")
            return

        user, created = User.objects.get_or_create(
            roblox_id=roblox_id,
            defaults={
                "username": username,
                "roblox_username": username,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        # get_or_create solo aplica defaults al crear: si el usuario ya existía
        # sin privilegios (p. ej. se creó por OAuth), había que reafirmarlos o
        # el admin de emergencia quedaba sin poder entrar.
        user.username = username
        user.roblox_username = user.roblox_username or username
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "creado" if created else "actualizado"
        self.stdout.write(
            f"Emergency admin {action}: login en /admin/ con roblox_id={roblox_id}"
        )
