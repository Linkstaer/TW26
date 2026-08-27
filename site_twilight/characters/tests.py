# -*- coding: utf-8 -*-
"""
Matriz de visibilidad de la Database de IDs (spec §4.2).

Esta es la lógica más delicada del sitio: decide qué datos de un personaje ve
cada usuario según su tarjeta. No tenía una sola prueba, así que cualquier
refactor de _serialize_character podía abrir una filtración en silencio.

Tabla del spec §4.2:
    Todos            -> solo personajes no clasificados
    L4 / ISD         -> ve L5, pero solo Codename + Facción
    L5               -> toda la info de L5, salvo archivos privados
    Comité de Ética  -> toda la info L5 con Codename
    L6 (RAISA/AO)    -> acceso completo
"""

from datetime import date

from django.test import TestCase

from characters.models import Character
from characters.views import _serialize_character, _viewer_access
from factions.models import (
    AccessCard,
    CharacterFactionMembership,
    Faction,
    FactionRank,
)
from users.models import User


def make_card(name, level, card_type=AccessCard.CardType.STANDARD):
    return AccessCard.objects.create(name=name, level=level, card_type=card_type)


class AccessMatrixTestCase(TestCase):
    """Base con un personaje L5 dentro de una facción clasificada."""

    @classmethod
    def setUpTestData(cls):
        cls.cards = {
            "L1": make_card("Basica", AccessCard.Level.L1),
            "L4": make_card("Nivel 4", AccessCard.Level.L4),
            "L5": make_card("Nivel 5", AccessCard.Level.L5),
            "L6": make_card("RAISA", AccessCard.Level.L6, AccessCard.CardType.RAISA),
            "ethics": make_card(
                "Comite", AccessCard.Level.L5, AccessCard.CardType.ETHICS_COMMITTEE
            ),
        }

        cls.faction = Faction.objects.create(
            name="Consejo O5",
            display_name="Consejo O5",
            faction_type=Faction.Type.COUNCIL,
            is_classified=True,
            facade_name="Site Direction",
        )
        cls.rank = FactionRank.objects.create(
            faction=cls.faction, name="O5-9", level=5, access_card=cls.cards["L5"]
        )

        cls.owner = cls.make_user(1001, "duenio")
        cls.target = cls.make_character(cls.owner, "SPECTRE")
        CharacterFactionMembership.objects.create(
            character=cls.target,
            faction=cls.faction,
            rank=cls.rank,
            access_card=cls.cards["L5"],
        )

    @staticmethod
    def make_user(roblox_id, username):
        return User.objects.create(roblox_id=roblox_id, roblox_username=username)

    @staticmethod
    def make_character(owner, codename, status=Character.Status.ACTIVE):
        return Character.objects.create(
            owner=owner,
            codename=codename,
            first_name="Jane",
            last_name="Doe",
            country="Argentina",
            birth_date=date(1990, 5, 1),
            photo_url="https://example.com/foto.png",
            lore="Historial clasificado.",
            morph="12345",
            status=status,
        )

    def viewer_with_card(self, roblox_id, username, card):
        """Usuario cuya tarjeta más alta es `card`, vía una facción neutra."""
        user = self.make_user(roblox_id, username)
        faction = Faction.objects.create(
            name=f"Dept {username}",
            display_name=f"Dept {username}",
            faction_type=Faction.Type.DEPARTMENT,
        )
        rank = FactionRank.objects.create(
            faction=faction, name="Miembro", level=1, access_card=card
        )
        character = self.make_character(user, f"CN-{username}")
        CharacterFactionMembership.objects.create(
            character=character, faction=faction, rank=rank, access_card=card
        )
        return user

    def serialize_target_for(self, viewer):
        membership = CharacterFactionMembership.objects.select_related(
            "faction", "rank", "access_card"
        ).get(character=self.target)
        return _serialize_character(
            self.target, viewer, _viewer_access(viewer), membership=membership
        )


class TodosVenSoloNoClasificados(AccessMatrixTestCase):
    """Todos: solo personajes no clasificados (spec §4.2)."""

    def test_l1_no_ve_personaje_l5(self):
        viewer = self.viewer_with_card(2001, "novato", self.cards["L1"])
        self.assertIsNone(self.serialize_target_for(viewer))

    def test_l1_no_ve_personaje_clasificado(self):
        viewer = self.viewer_with_card(2002, "novato2", self.cards["L1"])
        otro_duenio = self.make_user(2003, "otro")
        clasificado = self.make_character(
            otro_duenio, "GHOST", status=Character.Status.CLASSIFIED
        )
        data = _serialize_character(clasificado, viewer, _viewer_access(viewer))
        self.assertIsNone(data)

    def test_l1_ve_personaje_normal_pero_sin_archivos_privados(self):
        viewer = self.viewer_with_card(2004, "novato3", self.cards["L1"])
        otro_duenio = self.make_user(2005, "civil")
        normal = self.make_character(otro_duenio, "ALPHA")
        data = _serialize_character(normal, viewer, _viewer_access(viewer))
        self.assertIsNotNone(data)
        self.assertEqual(data["codename"], "ALPHA")
        # Sin membresía el personaje es L1, así que un L1 sí lee su ficha.
        self.assertEqual(data["first_name"], "Jane")
        # Los morphs son archivo privado: nunca para terceros.
        self.assertIn("morph", data["redacted"])
        self.assertNotIn("morph_command", data)


class L4VeSoloCodenameYFaccion(AccessMatrixTestCase):
    """L5 visto por un L4: solo Codename + Facción (spec §4.2)."""

    def setUp(self):
        self.viewer = self.viewer_with_card(3001, "isd", self.cards["L4"])
        self.data = self.serialize_target_for(self.viewer)

    def test_el_personaje_es_visible(self):
        self.assertIsNotNone(self.data)
        self.assertEqual(self.data["codename"], "SPECTRE")

    def test_nombre_real_y_lore_van_expurgados(self):
        for field in ("first_name", "last_name", "country", "birth_date", "lore"):
            self.assertIsNone(self.data[field], field)
            self.assertIn(field, self.data["redacted"])

    def test_la_foto_sigue_a_la_identidad(self):
        self.assertIsNone(self.data["photo_url"])
        self.assertIn("photo_url", self.data["redacted"])

    def test_ve_la_faccion_pero_con_fachada(self):
        self.assertEqual(self.data["faction"], "Site Direction")

    def test_no_ve_el_rango_detras_de_la_fachada(self):
        # "O5-9" delataría al Consejo O5 aunque la facción salga como fachada.
        self.assertIsNone(self.data["faction_data"]["rank"])


class L5VeTodoMenosArchivosPrivados(AccessMatrixTestCase):
    """L5: toda la info de L5, salvo archivos privados (spec §4.2)."""

    def setUp(self):
        self.viewer = self.viewer_with_card(4001, "consejero", self.cards["L5"])
        self.data = self.serialize_target_for(self.viewer)

    def test_ve_la_identidad_completa(self):
        self.assertEqual(self.data["first_name"], "Jane")
        self.assertEqual(self.data["country"], "Argentina")
        self.assertEqual(self.data["lore"], "Historial clasificado.")

    def test_no_ve_los_morphs(self):
        self.assertIn("morph", self.data["redacted"])
        self.assertNotIn("morph_command", self.data)

    def test_ve_el_nombre_real_de_la_faccion(self):
        self.assertEqual(self.data["faction"], "Consejo O5")


class ComiteDeEticaVeL5ConCodename(AccessMatrixTestCase):
    """Comité de Ética: toda info L5 con Codename (spec §4.2)."""

    def setUp(self):
        self.viewer = self.viewer_with_card(5001, "etica", self.cards["ethics"])
        self.data = self.serialize_target_for(self.viewer)

    def test_ve_identidad_completa_y_codename(self):
        self.assertEqual(self.data["codename"], "SPECTRE")
        self.assertEqual(self.data["first_name"], "Jane")

    def test_la_tarjeta_de_etica_se_identifica_explicitamente(self):
        # spec §2.4: el resto de las L5 se enmascaran como L4/L5.
        self.assertEqual(self.cards["ethics"].display_name, "L4/L5 - Comité de Ética")
        self.assertEqual(self.cards["L5"].display_name, "L4/L5 - Nivel 5")


class L6TieneAccesoCompleto(AccessMatrixTestCase):
    """L6 (RAISA / Admin Office): acceso completo (spec §4.2)."""

    def setUp(self):
        self.viewer = self.viewer_with_card(6001, "raisa", self.cards["L6"])
        self.data = self.serialize_target_for(self.viewer)

    def test_ve_todo_incluidos_los_morphs(self):
        self.assertEqual(self.data["first_name"], "Jane")
        self.assertEqual(self.data["morph"], "12345")
        self.assertIn("morph_command", self.data)
        self.assertEqual(self.data["redacted"], [])

    def test_ve_el_nombre_real_de_la_faccion_clasificada(self):
        self.assertEqual(self.data["faction"], "Consejo O5")


class ElDuenioVeSuPropioPersonaje(AccessMatrixTestCase):
    def test_el_duenio_ve_todo_sin_fachada(self):
        data = self.serialize_target_for(self.owner)
        self.assertEqual(data["first_name"], "Jane")
        self.assertEqual(data["morph"], "12345")
        # A su propia facción la ve por su nombre real.
        self.assertEqual(data["faction"], "Consejo O5")

    def test_personaje_eliminado_solo_para_el_duenio(self):
        eliminado = self.make_character(self.owner, "BORRADO")
        eliminado.status = Character.Status.DELETED
        eliminado.save()

        ajeno = self.viewer_with_card(7001, "ajeno", self.cards["L1"])
        self.assertIsNone(_serialize_character(eliminado, ajeno, _viewer_access(ajeno)))
        self.assertIsNotNone(
            _serialize_character(eliminado, self.owner, _viewer_access(self.owner))
        )


class CensuraDelDuenio(AccessMatrixTestCase):
    """El dueño tapa partes de su lore con [[...]]."""

    def setUp(self):
        self.target.lore = "Nacida en Praga. [[Trabajó para el GOC.]] Reclutada en 2011."
        self.target.save()

    def test_un_tercero_ve_bloques(self):
        viewer = self.viewer_with_card(8001, "curioso", self.cards["L5"])
        data = self.serialize_target_for(viewer)
        self.assertNotIn("GOC", data["lore"])
        self.assertIn("█", data["lore"])
        self.assertTrue(data["lore_censored_by_owner"])

    def test_l6_atraviesa_la_censura(self):
        viewer = self.viewer_with_card(8002, "raisa2", self.cards["L6"])
        data = self.serialize_target_for(viewer)
        self.assertIn("GOC", data["lore"])
        self.assertTrue(data["lore_censorship_revealed"])

    def test_el_duenio_conserva_las_marcas_para_editarlas(self):
        data = self.serialize_target_for(self.owner)
        self.assertIn("[[Trabajó para el GOC.]]", data["lore"])


class HerenciaDeTarjeta(AccessMatrixTestCase):
    """El usuario hereda la tarjeta más alta de sus personajes (spec §2.4)."""

    def test_toma_la_mas_alta_entre_varios_personajes(self):
        user = self.viewer_with_card(9001, "multi", self.cards["L1"])
        segundo = self.make_character(user, "SEGUNDO")
        faction = Faction.objects.create(
            name="Beta-1",
            display_name="Beta-1",
            faction_type=Faction.Type.SPECIAL_FORCE,
        )
        rank = FactionRank.objects.create(
            faction=faction, name="Operador", level=1, access_card=self.cards["L5"]
        )
        CharacterFactionMembership.objects.create(
            character=segundo, faction=faction, rank=rank, access_card=self.cards["L5"]
        )

        self.assertEqual(user.get_highest_access_card().level, "L5")

    def test_sin_membresias_cae_a_l1(self):
        user = self.make_user(9002, "sin_faccion")
        self.assertEqual(user.get_highest_access_card().level, "L1")

    def test_niveles_accesibles_son_acumulativos(self):
        user = self.viewer_with_card(9003, "acumulado", self.cards["L4"])
        self.assertEqual(user.get_accessible_levels(), ["L1", "L2", "L3", "L4"])
