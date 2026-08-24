from django.conf import settings


import os


class DevAuthMiddleware:
    """
    Middleware that bypasses authentication in DEV mode.

    Por defecto crea/loguea un superusuario ficticio (dev_admin).
    Si DEV_USER_ROBLOX_ID está definido en el entorno, loguea en su lugar
    a ese usuario como usuario NORMAL (sin staff ni superuser), creándolo
    si no existe — útil para probar la matriz de niveles de acceso.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEV and not request.user.is_authenticated:
            from users.models import User

            dev_roblox_id = os.getenv("DEV_USER_ROBLOX_ID")

            if dev_roblox_id:
                # Sesión de prueba como usuario normal
                dev_user, created = User.objects.get_or_create(
                    roblox_id=int(dev_roblox_id),
                    defaults={
                        "roblox_username": os.getenv(
                            "DEV_USER_NAME", f"test_user_{dev_roblox_id}"
                        ),
                    },
                )
            else:
                # Comportamiento original: superusuario ficticio
                dev_user, created = User.objects.get_or_create(
                    roblox_id=999999999,
                    defaults={
                        "roblox_username": "dev_admin",
                        "is_superuser": True,
                        "is_staff": True,
                    },
                )

            if created:
                dev_user.set_unusable_password()
                dev_user.save()

            # Force login the dev user
            request.user = dev_user

        return self.get_response(request)
