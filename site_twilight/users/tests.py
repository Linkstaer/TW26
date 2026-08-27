# -*- coding: utf-8 -*-
"""
Control de acceso de la API: quién puede llamar a qué.

Estas pruebas cubren tres agujeros que existían y que un refactor podría
reabrir sin que nadie lo note:

  - /api/moderation/users/search/ no pedía autenticación ni permisos.
  - /api/users/<roblox_id>/ tampoco: exponía la base de usuarios entera.
  - Los POST de moderación iban con @csrf_exempt.
"""

import json
from datetime import date

from django.test import TestCase
from django.urls import reverse

from characters.models import Character
from factions.models import (
    AccessCard,
    CharacterFactionMembership,
    Faction,
    FactionRank,
)
from users.models import StaffRole, User


class APIAccessTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.target = User.objects.create(roblox_id=555, roblox_username="objetivo")
        cls.plain_user = User.objects.create(roblox_id=556, roblox_username="civil")

        cls.moderator = User.objects.create(roblox_id=557, roblox_username="mod")
        StaffRole.objects.create(
            user=cls.moderator, scope=StaffRole.Scope.MODERATION, level=1
        )

        cls.ingame_mod = User.objects.create(roblox_id=558, roblox_username="ingame")
        StaffRole.objects.create(
            user=cls.ingame_mod, scope=StaffRole.Scope.INGAME, level=1
        )

    @staticmethod
    def make_character(owner, codename):
        return Character.objects.create(
            owner=owner,
            codename=codename,
            first_name="Ana",
            last_name="Lopez",
            country="Chile",
            birth_date=date(1995, 3, 3),
            morph="777",
        )


class BusquedaDeUsuariosEsPrivada(APIAccessTestCase):
    def url(self, query="objetivo"):
        return reverse("search_users", args=[query])

    def test_anonimo_no_puede_enumerar_usuarios(self):
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 401)

    def test_usuario_comun_tampoco(self):
        self.client.force_login(self.plain_user)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 403)

    def test_moderador_si_puede(self):
        self.client.force_login(self.moderator)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_busqueda_por_roblox_id(self):
        self.client.force_login(self.moderator)
        response = self.client.get(self.url("555"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["roblox_username"], "objetivo")

    def test_un_id_fuera_del_rango_de_bigint_no_revienta(self):
        """
        roblox_id es un bigint. isdigit() acepta "9"*30 y Python lo convierte
        sin problema, pero Postgres corta con "bigint out of range" y la vista
        devolvía 500. SQLite lo tragaba, así que solo aparecía en producción.
        """
        self.client.force_login(self.moderator)
        response = self.client.get(self.url("9" * 30))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)


class ParseoDeRobloxID(TestCase):
    def test_acepta_un_bigint_valido(self):
        from users.views.moderation import parse_roblox_id

        self.assertEqual(parse_roblox_id("123456"), 123456)

    def test_rechaza_lo_que_desborda_bigint(self):
        from users.views.moderation import BIGINT_MAX, parse_roblox_id

        self.assertEqual(parse_roblox_id(str(BIGINT_MAX)), BIGINT_MAX)
        self.assertIsNone(parse_roblox_id(str(BIGINT_MAX + 1)))
        self.assertIsNone(parse_roblox_id("9" * 40))

    def test_rechaza_lo_que_no_es_numero(self):
        from users.views.moderation import parse_roblox_id

        self.assertIsNone(parse_roblox_id("abc"))
        self.assertIsNone(parse_roblox_id(""))
        self.assertIsNone(parse_roblox_id(None))


class PerfilDeUsuarioRequiereSesion(APIAccessTestCase):
    def url(self):
        return reverse("api_get_user_by_roblox_id", args=[555])

    def test_anonimo_es_rechazado(self):
        response = self.client.get(self.url())
        self.assertIn(response.status_code, (302, 401, 403))

    def test_usuario_logueado_ve_el_perfil(self):
        self.client.force_login(self.plain_user)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["roblox_username"], "objetivo")

    def test_el_perfil_trae_los_campos_del_spec(self):
        """spec §1.2: roles especiales, primer acceso, facciones y tarjeta."""
        self.client.force_login(self.plain_user)
        data = self.client.get(self.url()).json()
        for field in (
            "roblox_id",
            "roblox_username",
            "first_login",
            "special_roles",
            "factions",
            "access_card",
        ):
            self.assertIn(field, data)

    def test_el_estado_de_moderacion_no_es_publico(self):
        self.client.force_login(self.plain_user)
        data = self.client.get(self.url()).json()
        self.assertNotIn("warning_count", data)
        self.assertNotIn("is_banned", data)

    def test_un_moderador_si_ve_el_estado_de_moderacion(self):
        self.client.force_login(self.moderator)
        data = self.client.get(self.url()).json()
        self.assertIn("warning_count", data)

    def test_el_acceso_derivado_es_la_tarjeta_mas_alta(self):
        card = AccessCard.objects.create(name="Nivel 4", level=AccessCard.Level.L4)
        faction = Faction.objects.create(
            name="ISD", display_name="ISD", faction_type=Faction.Type.DEPARTMENT
        )
        rank = FactionRank.objects.create(
            faction=faction, name="Agente", level=1, access_card=card
        )
        character = self.make_character(self.target, "OBJ-1")
        CharacterFactionMembership.objects.create(
            character=character, faction=faction, rank=rank, access_card=card
        )

        self.client.force_login(self.plain_user)
        data = self.client.get(self.url()).json()
        self.assertEqual(data["access_card"]["level"], "L4")
        self.assertEqual(data["factions"][0]["name"], "ISD")


class BusquedaDePersonajesParaModeracion(APIAccessTestCase):
    """spec §6: búsqueda por username, user ID o codename."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.character = cls.make_character(cls.target, "NOMAD")

    def url(self):
        return reverse("characters_moderation")

    def test_requiere_permiso_de_personajes(self):
        self.client.force_login(self.plain_user)
        self.assertEqual(self.client.get(self.url()).status_code, 403)

    def test_busca_por_codename(self):
        self.client.force_login(self.ingame_mod)
        response = self.client.get(self.url(), {"search": "NOMAD"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_busca_por_roblox_user_id(self):
        self.client.force_login(self.ingame_mod)
        response = self.client.get(self.url(), {"search": "555"})
        self.assertEqual(response.json()["count"], 1)

    def test_un_id_fuera_del_rango_de_bigint_no_revienta(self):
        self.client.force_login(self.ingame_mod)
        response = self.client.get(self.url(), {"search": "9" * 30})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_busca_por_roblox_username(self):
        self.client.force_login(self.ingame_mod)
        response = self.client.get(self.url(), {"search": "objetivo"})
        self.assertEqual(response.json()["count"], 1)

    def test_la_vista_consolidada_trae_solicitudes_e_historial(self):
        self.client.force_login(self.ingame_mod)
        response = self.client.get(
            reverse("character_moderation_detail", args=[self.character.id])
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("pending_applications", data)
        self.assertIn("history", data)
        self.assertIn("actor_logs", data)
        self.assertEqual(data["character"]["codename"], "NOMAD")

    def test_es_solo_lectura(self):
        """spec §1.4: moderación no edita personajes ni tarjetas."""
        self.client.force_login(self.ingame_mod)
        self.assertEqual(self.client.post(self.url()).status_code, 405)


class CSRFEnAccionesDestructivas(APIAccessTestCase):
    """Los POST de moderación ya no van con @csrf_exempt."""

    def setUp(self):
        # enforce_csrf_checks emula al navegador: sin token, la petición cae.
        self.csrf_client = self.client_class(enforce_csrf_checks=True)

    def test_crear_warn_sin_token_csrf_falla(self):
        self.csrf_client.force_login(self.moderator)
        response = self.csrf_client.post(
            reverse("create_warn"),
            data=json.dumps({"target_id": 555, "reason": "prueba"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_crear_ban_sin_token_csrf_falla(self):
        self.csrf_client.force_login(self.moderator)
        response = self.csrf_client.post(
            reverse("create_ban"),
            data=json.dumps({"target_id": 555, "reason": "prueba"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)


class RutasDeApelacionDeBan(APIAccessTestCase):
    """Las vistas existían pero no estaban ruteadas: apelar era imposible."""

    def test_la_ruta_de_apelacion_existe(self):
        self.assertEqual(reverse("appeal_ban", args=[1]), "/api/moderation/bans/1/appeal/")

    def test_la_ruta_de_respuesta_existe(self):
        self.assertEqual(
            reverse("respond_ban_appeal", args=[1]),
            "/api/moderation/bans/1/respond-appeal/",
        )


class PermisosDeStaff(APIAccessTestCase):
    def test_view_classified_factions_esta_declarado(self):
        """Lo consultaba el código pero no existía en ningún scope."""
        director = User.objects.create(roblox_id=600, roblox_username="faction_lead")
        StaffRole.objects.create(
            user=director, scope=StaffRole.Scope.RP_FACTION, level=2
        )
        self.assertTrue(director.has_permission("view_classified_factions"))

    def test_assign_scp_actor_esta_declarado(self):
        lead = User.objects.create(roblox_id=601, roblox_username="scp_lead")
        StaffRole.objects.create(user=lead, scope=StaffRole.Scope.RP_ACTORS, level=2)
        self.assertTrue(lead.has_permission("assign_scp_actor"))

    def test_un_usuario_comun_no_tiene_ninguno(self):
        self.assertFalse(self.plain_user.has_permission("view_classified_factions"))
        self.assertFalse(self.plain_user.has_permission("assign_scp_actor"))
