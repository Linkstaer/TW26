from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User
import os

class Command(BaseCommand):
    help = "Ensure emergency admin user exists"

    def handle(self, *args, **options):
        username = os.getenv("EMERGENCY_ADMIN_USERNAME")
        password = os.getenv("EMERGENCY_ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write("Emergency admin vars not set, skipping")
            return

        user, created = User.objects.get_or_create(
            roblox_id=1,
            defaults={
                "username": username,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.set_password(password)
        user.save()

        self.stdout.write("Emergency admin ensured")
