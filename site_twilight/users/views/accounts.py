
# Create your views here.

import secrets
from django.shortcuts import redirect
from django.conf import settings
import requests
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from ..models import User

def roblox_login(request):
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    url = (
        "https://apis.roblox.com/oauth/v1/authorize"
        f"?client_id={settings.ROBLOX_CLIENT_ID}"
        f"&redirect_uri={settings.ROBLOX_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid profile"
        f"&state={state}"
    )
    return redirect(url)

def roblox_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code or state != request.session.get("oauth_state"):
        return HttpResponseForbidden("OAuth inválido")

    token_res = requests.post(
        "https://apis.roblox.com/oauth/v1/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.ROBLOX_CLIENT_ID,
            "client_secret": settings.ROBLOX_CLIENT_SECRET,
            "redirect_uri": settings.ROBLOX_REDIRECT_URI,
        },
    ).json()

    access_token = token_res.get("access_token")
    if not access_token:
        return HttpResponseForbidden("Error obteniendo access token")

    profile = requests.get(
        "https://apis.roblox.com/oauth/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    roblox_id = int(profile["sub"])
    roblox_username = profile["preferred_username"]

    user, created = User.objects.get_or_create(
        roblox_id=roblox_id,
        defaults={"roblox_username": roblox_username},
    )

    if created:
        user.set_unusable_password()
        user.save()

    # Ensure Django knows the backend
    login(request, user)

    return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/")
