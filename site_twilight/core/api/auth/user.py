def get_current_user_service(user):
    if user.is_authenticated:
        return {
            "roblox_username": user.roblox_username,
            "roblox_id": user.roblox_id,  # Añade este campo
            "id": user.id,
            "is_authenticated": True,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "first_login": user.first_login.isoformat() if user.first_login else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        }
    
    return {
        "is_authenticated": False
    }