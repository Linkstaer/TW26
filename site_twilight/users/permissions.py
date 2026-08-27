STAFF_PERMISSIONS = {
    # ───────────────── GLOBAL ─────────────────
    "global": {
        1: {"change_ssu_status"},              # Host
        2: {"full_moderation_control"},        # Moderation Lead
    },

    # ─────────────── MODERATION (BASE) ───────────────
    "moderation": {
        1: {"access_moderation_dashboard"},    # Any moderator
        2: {"full_moderation_control"},        # Lead / Management
    },

    # ─────────────── IN-GAME ───────────────
    "ingame": {
        1: {"view_characters_basic", "create_warn"},  # Junior
        2: {"create_warn", "register_ban"},           # Official
        3: {"register_ban", "manage_warns"},          # Qualified +
    },

    # ─────────────── DISCORD ───────────────
    "discord": {
        1: {"access_moderation_dashboard", "create_warn"},  # Junior
        2: {"register_ban"},
        3: {"manage_warns"},
        4: {"full_discord_moderation"},
    },

    # ───────────── RP: ROLEPLAY TEAM ─────────────
    "rp_roleplay": {
        1: {"access_moderation_dashboard", "edit_rp_files_basic"},  # Team Member
        2: {"edit_rp_files_full"},              # Director Roleplay
    },

    # ───────────── RP: FACTION MODERATION ─────────────
    "rp_faction": {
        # view_classified_factions: ve el nombre real detrás de la fachada
        # (spec §2.1). Lo consultaban User.get_visible_factions y
        # Faction.can_user_see_real_identity, pero no estaba declarado en
        # ningún scope, así que siempre daba False salvo para superusuarios.
        1: {"access_moderation_dashboard", "moderate_factions_basic"},  # Team Member
        2: {"moderate_factions_full", "view_classified_factions"},      # Director
    },

    # ───────────── RP: ACTORS SUPERVISION ─────────────
    "rp_actors": {
        # assign_scp_actor: ata un personaje a un archivo SCP (spec §3.4).
        1: {"access_moderation_dashboard", "supervise_actors_basic"},  # Team Member
        2: {"supervise_actors_full", "assign_scp_actor"},               # Director
    },
}