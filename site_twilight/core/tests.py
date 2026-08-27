# -*- coding: utf-8 -*-
"""
AI de Consulta (spec §7).

Lo crítico acá es que el contexto que se le arma al modelo NUNCA contenga
material por encima de la tarjeta del consultante: es lo que hace que la
terminal sea inmune a que le pidan datos de niveles superiores.
"""

import json
from datetime import date

from django.test import TestCase
from django.urls import reverse

from characters.models import Character
from core.api.ai import RATE_LIMIT_QUERIES, _build_context
from core.models import AIQueryLog
from factions.models import (
    AccessCard,
    CharacterFactionMembership,
    Faction,
    FactionRank,
)
from scps.models import SCP, Document
from users.models import StaffRole, User


class AITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.scp = SCP.objects.create(
            scp_id="SCP-173",
            title="La Escultura",
            content_l1="Procedimiento de contención estándar.",
            content_l5="ANOMALIA-CRITICA-L5",
        )
        cls.scp.appendices = [
            {"title": "Incidente", "content": "APENDICE-L5", "level": "L5"},
            {"title": "Nota", "content": "APENDICE-L1", "level": "L1"},
        ]
        cls.scp.save()

        Document.objects.create(
            title="Protocolo Omega",
            slug="protocolo-omega",
            content="DOCUMENTO-L5",
            min_access_level="L5",
        )
        Document.objects.create(
            title="Manual de Ingreso",
            slug="manual-ingreso",
            content="DOCUMENTO-L1",
            min_access_level="L1",
        )

        cls.classified = Faction.objects.create(
            name="Beta-1",
            display_name="Beta-1",
            faction_type=Faction.Type.CLASSIFIED,
            is_classified=True,
            facade_name="Logistics Division",
        )

    @staticmethod
    def make_character(owner, codename):
        return Character.objects.create(
            owner=owner,
            codename=codename,
            first_name="Leo",
            last_name="Marin",
            country="España",
            birth_date=date(1991, 1, 1),
            morph="222",
        )

    def user_with_level(self, roblox_id, username, level):
        user = User.objects.create(roblox_id=roblox_id, roblox_username=username)
        card = AccessCard.objects.create(name=f"Card-{username}", level=level)
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


class ElContextoRespetaLaTarjeta(AITestCase):
    def test_un_l1_no_recibe_material_l5(self):
        user = self.user_with_level(1, "bajo", AccessCard.Level.L1)
        parts, accessible, level = _build_context(user)
        blob = "\n".join(parts)

        self.assertEqual(accessible, ["L1"])
        self.assertEqual(level, 1)
        self.assertIn("Procedimiento de contención estándar.", blob)
        self.assertNotIn("ANOMALIA-CRITICA-L5", blob)
        self.assertNotIn("APENDICE-L5", blob)
        self.assertNotIn("DOCUMENTO-L5", blob)

    def test_un_l5_si_recibe_el_material_l5(self):
        user = self.user_with_level(2, "alto", AccessCard.Level.L5)
        parts, _, _ = _build_context(user)
        blob = "\n".join(parts)

        self.assertIn("ANOMALIA-CRITICA-L5", blob)
        self.assertIn("APENDICE-L5", blob)
        self.assertIn("DOCUMENTO-L5", blob)

    def test_las_fachadas_llegan_aplicadas_al_contexto(self):
        user = self.user_with_level(3, "medio", AccessCard.Level.L2)
        parts, _, _ = _build_context(user)
        blob = "\n".join(parts)

        self.assertIn("Logistics Division", blob)
        self.assertNotIn("FACCIÓN Beta-1", blob)

    def test_un_superusuario_ve_todos_los_niveles(self):
        admin = User.objects.create(
            roblox_id=4, roblox_username="root", is_superuser=True
        )
        _, accessible, level = _build_context(admin)
        self.assertEqual(accessible, ["L1", "L2", "L3", "L4", "L5", "L6"])
        self.assertEqual(level, 6)


class ConsultasALaTerminal(AITestCase):
    def setUp(self):
        self.user = self.user_with_level(10, "consultante", AccessCard.Level.L1)
        self.url = reverse("api_ai_query")

    def query(self, text="contención", mode="rp"):
        return self.client.post(
            self.url,
            data=json.dumps({"query": text, "mode": mode}),
            content_type="application/json",
        )

    def test_anonimo_no_consulta(self):
        response = self.query()
        self.assertIn(response.status_code, (302, 401, 403))

    def test_toda_consulta_queda_logueada(self):
        self.client.force_login(self.user)
        self.query()
        log = AIQueryLog.objects.get(user=self.user)
        self.assertEqual(log.query, "contención")
        self.assertEqual(log.access_level, "L1")

    def test_consulta_vacia_es_rechazada(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            data=json.dumps({"query": "   "}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_el_modo_tecnico_se_degrada_para_no_staff(self):
        """spec §7: consulta Off-RP solo para roles autorizados."""
        self.client.force_login(self.user)
        response = self.query(mode="technical")
        self.assertEqual(response.json()["mode"], "rp")

    def test_el_staff_si_usa_el_modo_tecnico(self):
        mod = User.objects.create(roblox_id=11, roblox_username="mod")
        StaffRole.objects.create(user=mod, scope=StaffRole.Scope.MODERATION, level=1)
        self.client.force_login(mod)
        response = self.query(mode="technical")
        self.assertEqual(response.json()["mode"], "technical")

    def test_la_respuesta_sin_llm_no_filtra_niveles_superiores(self):
        self.client.force_login(self.user)
        response = self.query(text="ANOMALIA-CRITICA-L5")
        self.assertNotIn("ANOMALIA-CRITICA-L5", response.json()["response"])


class LimiteDeConsultas(AITestCase):
    """Cada consulta con LLM cuesta dinero: hay tope por usuario."""

    def setUp(self):
        self.user = self.user_with_level(20, "insistente", AccessCard.Level.L1)
        self.url = reverse("api_ai_query")
        self.client.force_login(self.user)

    def test_corta_al_superar_el_tope(self):
        for _ in range(RATE_LIMIT_QUERIES):
            response = self.client.post(
                self.url,
                data=json.dumps({"query": "hola"}),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            data=json.dumps({"query": "hola"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 429)
        self.assertGreater(response.json()["retry_after"], 0)

    def test_los_superusuarios_no_tienen_tope(self):
        admin = User.objects.create(
            roblox_id=21, roblox_username="root2", is_superuser=True
        )
        self.client.force_login(admin)
        for _ in range(RATE_LIMIT_QUERIES + 2):
            response = self.client.post(
                self.url,
                data=json.dumps({"query": "hola"}),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 200)
