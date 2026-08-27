# -*- coding: utf-8 -*-
"""
Fachadas de facciones clasificadas (spec §2.1 / §2.4) y flujo de solicitudes
(spec §2.2).

La regla de fachada vivía duplicada en dos sitios con criterios distintos;
ahora es una sola (Faction.can_user_see_real_identity) y estas pruebas la
fijan.
"""

from datetime import date

from django.test import TestCase

from characters.models import Character
from factions.models import (
    AccessCard,
    CharacterFactionMembership,
    Faction,
    FactionRank,
)
from users.models import StaffRole, User


class FactionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.classified = Faction.objects.create(
            name="Administrators Office",
            display_name="Administrators Office",
            faction_type=Faction.Type.CLASSIFIED,
            is_classified=True,
            facade_name="Administrative Department",
        )
        cls.public = Faction.objects.create(
            name="Security Department",
            display_name="Security Department",
            faction_type=Faction.Type.DEPARTMENT,
        )

    @staticmethod
    def make_character(owner, codename):
        return Character.objects.create(
            owner=owner,
            codename=codename,
            first_name="Sam",
            last_name="Vega",
            country="Perú",
            birth_date=date(1992, 7, 7),
            morph="111",
        )

    def user_with_card(self, roblox_id, username, card=None, faction=None):
        user = User.objects.create(roblox_id=roblox_id, roblox_username=username)
        if card is None:
            return user
        faction = faction or Faction.objects.create(
            name=f"F-{username}",
            display_name=f"F-{username}",
            faction_type=Faction.Type.DEPARTMENT,
        )
        rank = FactionRank.objects.create(
            faction=faction, name="Rango", level=1, access_card=card
        )
        character = self.make_character(user, f"C-{username}")
        CharacterFactionMembership.objects.create(
            character=character, faction=faction, rank=rank, access_card=card
        )
        return user


class ReglaUnicaDeFachada(FactionTestCase):
    def setUp(self):
        self.l1 = AccessCard.objects.create(name="C1", level=AccessCard.Level.L1)
        self.l4 = AccessCard.objects.create(name="C4", level=AccessCard.Level.L4)
        self.l5 = AccessCard.objects.create(name="C5", level=AccessCard.Level.L5)
        self.ethics = AccessCard.objects.create(
            name="Etica",
            level=AccessCard.Level.L4,
            card_type=AccessCard.CardType.ETHICS_COMMITTEE,
        )

    def test_anonimo_ve_la_fachada(self):
        self.assertEqual(
            self.classified.get_visible_name(None), "Administrative Department"
        )

    def test_l4_ve_la_fachada(self):
        user = self.user_with_card(1, "cuatro", self.l4)
        self.assertEqual(
            self.classified.get_visible_name(user), "Administrative Department"
        )

    def test_l5_ve_el_nombre_real(self):
        user = self.user_with_card(2, "cinco", self.l5)
        self.assertEqual(
            self.classified.get_visible_name(user), "Administrators Office"
        )

    def test_comite_de_etica_ve_el_nombre_real_aunque_sea_l4(self):
        """El criterio antiguo (level >= L5) dejaba al Comité fuera."""
        user = self.user_with_card(3, "etica", self.ethics)
        self.assertEqual(
            self.classified.get_visible_name(user), "Administrators Office"
        )

    def test_un_miembro_ve_su_propia_faccion(self):
        user = self.user_with_card(4, "interno", self.l1, faction=self.classified)
        self.assertEqual(
            self.classified.get_visible_name(user), "Administrators Office"
        )

    def test_el_director_de_facciones_atraviesa_la_fachada(self):
        director = User.objects.create(roblox_id=5, roblox_username="lead")
        StaffRole.objects.create(
            user=director, scope=StaffRole.Scope.RP_FACTION, level=2
        )
        self.assertEqual(
            self.classified.get_visible_name(director), "Administrators Office"
        )

    def test_superusuario_ve_todo(self):
        admin = User.objects.create(
            roblox_id=6, roblox_username="admin", is_superuser=True
        )
        self.assertEqual(
            self.classified.get_visible_name(admin), "Administrators Office"
        )

    def test_una_faccion_no_clasificada_nunca_se_enmascara(self):
        user = self.user_with_card(7, "cualquiera", self.l1)
        self.assertEqual(self.public.get_visible_name(user), "Security Department")


class TarjetaPorDefecto(FactionTestCase):
    def test_no_escribe_en_la_db_si_ya_existe(self):
        primera = AccessCard.get_default_card()
        with self.assertNumQueries(1):
            segunda = AccessCard.get_default_card()
        self.assertEqual(primera.id, segunda.id)

    def test_la_crea_si_no_existe(self):
        self.assertFalse(
            AccessCard.objects.filter(name=AccessCard.DEFAULT_CARD_NAME).exists()
        )
        card = AccessCard.get_default_card()
        self.assertEqual(card.level, "L1")


class InvitacionesSinPersonaje(FactionTestCase):
    def test_str_no_revienta_con_character_nulo(self):
        """character quedó nullable: __str__ lo asumía presente."""
        from factions.models import FactionInvitation

        user = User.objects.create(roblox_id=10, roblox_username="invitado")
        invitation = FactionInvitation.objects.create(
            faction=self.public, user=user, invited_by=user
        )
        self.assertIn("invitado", str(invitation))

    def test_str_usa_el_codename_si_hay_personaje(self):
        from factions.models import FactionInvitation

        user = User.objects.create(roblox_id=11, roblox_username="invitado2")
        character = self.make_character(user, "DELTA")
        invitation = FactionInvitation.objects.create(
            faction=self.public, character=character, invited_by=user
        )
        self.assertIn("DELTA", str(invitation))


class SolicitudesDeIngreso(FactionTestCase):
    """spec §2.2: una solicitud activa por personaje."""

    def setUp(self):
        from factions.models import FactionApplication

        self.FactionApplication = FactionApplication
        self.user = User.objects.create(roblox_id=20, roblox_username="postulante")
        self.character = self.make_character(self.user, "ECHO")

    def test_no_se_permiten_dos_solicitudes_activas(self):
        from django.core.exceptions import ValidationError

        self.FactionApplication.objects.create(
            character=self.character, faction=self.public
        )
        duplicada = self.FactionApplication(
            character=self.character, faction=self.classified
        )
        with self.assertRaises(ValidationError):
            duplicada.clean()

    def test_no_se_solicita_con_membresia_activa(self):
        from django.core.exceptions import ValidationError

        card = AccessCard.objects.create(name="X", level=AccessCard.Level.L1)
        rank = FactionRank.objects.create(
            faction=self.public, name="R", level=1, access_card=card
        )
        CharacterFactionMembership.objects.create(
            character=self.character, faction=self.public, rank=rank, access_card=card
        )
        nueva = self.FactionApplication(
            character=self.character, faction=self.classified
        )
        with self.assertRaises(ValidationError):
            nueva.clean()
