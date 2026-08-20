from django.conf import settings


class DevAuthMiddleware:
    """
    Middleware that bypasses authentication in DEV mode.
    Creates a fake admin user for testing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEV and not request.user.is_authenticated:
            # Create a fake superuser for testing
            from users.models import User

            # Try to get or create a dev user
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
