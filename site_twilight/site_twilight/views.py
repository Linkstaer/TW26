from django.shortcuts import render
from django.http import HttpResponse


from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def spa_view(request):
    return render(request, 'index.html')


def check_login(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Logged in as {request.user.roblox_username}")
    return HttpResponse("Not logged in")



