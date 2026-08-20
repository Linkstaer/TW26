from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from characters.models import Character

User = get_user_model()

def api_get_user_by_roblox_id(request, roblox_id):
    try:
        user = get_object_or_404(User, roblox_id=roblox_id)
        data = {
            "roblox_username": user.roblox_username,
            "roblox_id": user.roblox_id,
            "id": user.id,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "first_login": user.first_login.isoformat() if user.first_login else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)

def api_get_user_characters(request, roblox_id):
    try:
        user = get_object_or_404(User, roblox_id=roblox_id)
        characters = Character.objects.filter(owner=user).order_by('-created_at')
        
        characters_data = []
        for char in characters:
            characters_data.append({
                "id": char.id,
                "codename": char.codename,
                "first_name": char.first_name,
                "last_name": char.last_name,
                "country": char.country,
                "birth_date": char.birth_date.isoformat() if char.birth_date else None,
                "faction": char.faction,
                "lore": char.lore,
                "owner_username": user.roblox_username,
                "owner_id": user.id,
                "created_at": char.created_at.isoformat() if char.created_at else None,
                # Datos morph
                "morph": char.morph,
                "hat": char.hat,
                "nvg_color": char.nvg_color,
                "shirt": char.shirt,
                "pants": char.pants,
                "skin_r": char.skin_r,
                "skin_g": char.skin_g,
                "skin_b": char.skin_b,
                "ntag": char.ntag,
                "cntag_r": char.cntag_r,
                "cntag_g": char.cntag_g,
                "cntag_b": char.cntag_b,
                "rtag": char.rtag,
                "crtag_r": char.crtag_r,
                "crtag_g": char.crtag_g,
                "crtag_b": char.crtag_b,
                "rhat": char.rhat,
                "morph_command": char.morph_command(),
            })
        
        return JsonResponse({"results": characters_data}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)