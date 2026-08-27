# -*- coding: utf-8 -*-
"""
Actores SCP (spec §3.4) y permisos de edición de archivos (spec §3.3).
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
from scps.models import SCP, SCPActorLog
from users.models import StaffRole, User


class SCPBaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.scp = SCP.objects.create(
            scp_id="SCP-2995",
            title="La Transmisión",
            content_l1="Procedimientos básicos.",
            content_l5="Datos de contención reservados.",
        )
        cls.actor_user = User.objects.create(roblox_id=101, roblox_username="actor")
        cls.actor_character = cls.make_character(cls.actor_user, "PROTEO")
        cls.outsider = User.objects.create(roblox_id=102, roblox_username="ajeno")

        cls.supervisor = User.objects.create(roblox_id=103, roblox_username="scp_lead")
        StaffRole.objects.create(
            user=cls.supervisor, scope=StaffRole.Scope.RP_ACTORS, level=2
        )

    @staticmethod
    def make_character(owner, codename):
        return Character.objects.create(
            owner=owner,
            codename=codename,
            first_name="Ivan",
            last_name="Petrov",
            country="Rusia",
            birth_date=date(1988, 2, 2),
            morph="999",
        )


class AsignacionDeActor(SCPBaseTestCase):
    """POST/DELETE /api/scps/<id>/actor/ (spec §3.4)."""

    def url(self):
        return reverse("scp_actor", args=[self.scp.id])

    def test_sin_permiso_no_puede_asignar(self):
        self.client.force_login(self.outsider)
        response = self.client.post(
            self.url(),
            data=json.dumps({"character_id": self.actor_character.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.scp.refresh_from_db()
        self.assertIsNone(self.scp.actor_character)

    def test_anonimo_es_redirigido_al_login(self):
        response = self.client.post(
            self.url(),
            data=json.dumps({"character_id": self.actor_character.id}),
            content_type="application/json",
        )
        self.assertIn(response.status_code, (302, 401, 403))

    def test_la_supervision_asigna_y_queda_logueado(self):
        self.client.force_login(self.supervisor)
        response = self.client.post(
            self.url(),
            data=json.dumps({"character_id": self.actor_character.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.scp.refresh_from_db()
        self.assertEqual(self.scp.actor_character_id, self.actor_character.id)

        log = SCPActorLog.objects.get(scp=self.scp, action=SCPActorLog.Action.ASSIGNED)
        self.assertEqual(log.character_id, self.actor_character.id)
        self.assertEqual(log.performed_by_id, self.supervisor.id)

    def test_un_personaje_no_interpreta_dos_scps(self):
        self.scp.actor_character = self.actor_character
        self.scp.save()
        otro = SCP.objects.create(scp_id="SCP-3001", title="Otro")

        self.client.force_login(self.supervisor)
        response = self.client.post(
            reverse("scp_actor", args=[otro.id]),
            data=json.dumps({"character_id": self.actor_character.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("SCP-2995", response.json()["error"])

    def test_remover_actor_deja_rastro(self):
        self.scp.actor_character = self.actor_character
        self.scp.save()

        self.client.force_login(self.supervisor)
        response = self.client.delete(self.url())
        self.assertEqual(response.status_code, 200)

        self.scp.refresh_from_db()
        self.assertIsNone(self.scp.actor_character)
        self.assertTrue(
            SCPActorLog.objects.filter(
                scp=self.scp, action=SCPActorLog.Action.UNASSIGNED
            ).exists()
        )


class ElSCPApareceEnElPerfilDelPersonaje(SCPBaseTestCase):
    """"El SCP aparece en su perfil de personaje" (spec §3.4)."""

    def setUp(self):
        self.scp.actor_character = self.actor_character
        self.scp.save()

    def test_el_modelo_expone_el_archivo(self):
        self.actor_character.refresh_from_db()
        self.assertTrue(self.actor_character.is_scp_actor)
        data = self.actor_character.get_scp_actor_data()
        self.assertEqual(data["scp_id"], "SCP-2995")
        self.assertEqual(data["title"], "La Transmisión")

    def test_el_endpoint_de_mis_personajes_lo_incluye(self):
        self.client.force_login(self.actor_user)
        response = self.client.get(reverse("character_list_user"))
        self.assertEqual(response.status_code, 200)
        personaje = response.json()["results"][0]
        self.assertTrue(personaje["is_scp_actor"])
        self.assertEqual(personaje["scp_actor"]["scp_id"], "SCP-2995")

    def test_un_personaje_sin_scp_no_reporta_actor(self):
        suelto = self.make_character(self.outsider, "SUELTO")
        self.assertFalse(suelto.is_scp_actor)
        self.assertIsNone(suelto.get_scp_actor_data())


class IdentidadDelActorEsSensible(SCPBaseTestCase):
    """Quién interpreta a un SCP no es información de dominio público."""

    def setUp(self):
        self.scp.actor_character = self.actor_character
        self.scp.save()

    def test_un_tercero_solo_sabe_que_hay_actor(self):
        data = self.scp.get_actor_data(self.outsider)
        self.assertTrue(data["has_actor"])
        self.assertIsNone(data["codename"])
        self.assertIsNone(data["owner"])

    def test_el_propio_actor_ve_su_ficha(self):
        data = self.scp.get_actor_data(self.actor_user)
        self.assertEqual(data["codename"], "PROTEO")

    def test_la_supervision_ve_la_identidad(self):
        data = self.scp.get_actor_data(self.supervisor)
        self.assertEqual(data["owner"], "actor")


class BitacoraDelActor(SCPBaseTestCase):
    """"Sus acciones quedan registradas en logs" (spec §3.4)."""

    def setUp(self):
        self.scp.actor_character = self.actor_character
        self.scp.save()
        self.url = reverse("scp_actor_logs", args=[self.scp.id])

    def test_el_actor_registra_una_accion_rp(self):
        self.client.force_login(self.actor_user)
        response = self.client.post(
            self.url,
            data=json.dumps({"description": "Brecha de contención en el Sector C."}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            SCPActorLog.objects.filter(
                scp=self.scp, action=SCPActorLog.Action.RP_ACTION
            ).exists()
        )

    def test_un_tercero_no_puede_registrar_acciones(self):
        self.client.force_login(self.outsider)
        response = self.client.post(
            self.url,
            data=json.dumps({"description": "Intento ajeno."}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_un_tercero_no_puede_leer_la_bitacora(self):
        self.client.force_login(self.outsider)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_editar_el_archivo_como_actor_queda_logueado(self):
        self.client.force_login(self.actor_user)
        response = self.client.post(
            reverse("scp_edit", args=[self.scp.id]),
            data=json.dumps({"section": "L1", "content": "Nuevos procedimientos."}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            SCPActorLog.objects.filter(
                scp=self.scp, action=SCPActorLog.Action.FILE_EDITED
            ).exists()
        )


class PermisosDeEdicionDeSCP(SCPBaseTestCase):
    """spec §3.3: quién redacta qué."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.scd_card = AccessCard.objects.create(
            name="ScD", level=AccessCard.Level.L3,
            card_type=AccessCard.CardType.SCIENTIFIC,
        )
        cls.o5_card = AccessCard.objects.create(
            name="O5", level=AccessCard.Level.L4,
            card_type=AccessCard.CardType.O5_COUNCIL,
        )
        cls.raisa_card = AccessCard.objects.create(
            name="RAISA-6", level=AccessCard.Level.L6,
            card_type=AccessCard.CardType.RAISA,
        )

    def user_with_card(self, roblox_id, username, card):
        user = User.objects.create(roblox_id=roblox_id, roblox_username=username)
        faction = Faction.objects.create(
            name=f"F-{username}",
            display_name=f"F-{username}",
            faction_type=Faction.Type.DEPARTMENT,
        )
        rank = FactionRank.objects.create(
            faction=faction, name="R", level=1, access_card=card
        )
        character = self.make_character(user, f"C-{username}")
        CharacterFactionMembership.objects.create(
            character=character, faction=faction, rank=rank, access_card=card
        )
        return user

    def test_scd_agrega_apendices_pero_no_edita_la_base(self):
        user = self.user_with_card(201, "cientifico", self.scd_card)
        self.assertFalse(self.scp.can_user_edit(user)[0])
        self.assertTrue(self.scp.can_user_add_appendix(user)[0])

    def test_o5_solo_redacta_hasta_su_nivel(self):
        user = self.user_with_card(202, "o5", self.o5_card)
        self.assertTrue(self.scp.can_user_edit_section(user, "L4")[0])
        self.assertFalse(self.scp.can_user_edit_section(user, "L5")[0])

    def test_raisa_redacta_cualquier_seccion(self):
        user = self.user_with_card(203, "raisa", self.raisa_card)
        self.assertTrue(self.scp.can_user_edit_section(user, "L6")[0])

    def test_el_actor_edita_solo_su_archivo(self):
        self.scp.actor_character = self.actor_character
        self.scp.save()
        otro = SCP.objects.create(scp_id="SCP-4000", title="Ajeno")

        self.assertTrue(self.scp.can_user_edit(self.actor_user)[0])
        self.assertFalse(otro.can_user_edit(self.actor_user)[0])

    def test_el_contenido_se_filtra_por_nivel(self):
        user = self.user_with_card(204, "basico", self.scd_card)
        data = self.scp.to_dict(user)
        self.assertIn("content_l1", data)
        self.assertNotIn("content_l5", data)
