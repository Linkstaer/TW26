def get_current_user_service(user):
    if user.is_authenticated:
        # Nivel real del usuario, derivado de la tarjeta más alta de sus
        # personajes. La cabecera de varias vistas lo mostraba fijo en
        # "LEVEL 2" sin consultar nada.
        card = user.get_highest_access_card()
        # Los admins operan como L6 en todo el backend (ver _viewer_access),
        # así que la cabecera no puede mostrarles el nivel de su tarjeta.
        if user.is_superuser:
            access_level, access_level_number = "L6", 6
        else:
            access_level = card.level if card else None
            access_level_number = card.level_number if card else 1
        return {
            "roblox_username": user.roblox_username,
            "roblox_id": user.roblox_id,  # Añade este campo
            "id": user.id,
            "is_authenticated": True,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "first_login": user.first_login.isoformat() if user.first_login else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "access_level": access_level,
            "access_level_number": access_level_number,
            "access_card": card.name if card else None,
        }
    
    return {
        "is_authenticated": False
    }