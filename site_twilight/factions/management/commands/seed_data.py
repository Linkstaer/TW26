from django.core.management.base import BaseCommand
from factions.models import AccessCard, Faction, FactionRank


class Command(BaseCommand):
    help = "Seed default access cards and factions"

    def handle(self, *args, **options):
        self.stdout.write("Creating access cards...")
        self.create_access_cards()

        self.stdout.write("Creating default factions...")
        self.create_factions()

        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))

    def create_access_cards(self):
        cards_data = [
            {
                "level": "L1",
                "card_type": AccessCard.CardType.STANDARD,
                "display_name": "Nivel 1 - Básico",
                "description": "Acceso básico al sitio. Puede ver información pública.",
                "can_view_l1": True,
                "can_view_l2": False,
                "can_view_l3": False,
                "can_view_l4": False,
                "can_view_l5": False,
                "can_view_l6": False,
            },
            {
                "level": "L2",
                "card_type": AccessCard.CardType.STANDARD,
                "display_name": "Nivel 2 - Standard",
                "description": "Acceso standard. Puede ver información L2.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": False,
                "can_view_l4": False,
                "can_view_l5": False,
                "can_view_l6": False,
            },
            {
                "level": "L3",
                "card_type": AccessCard.CardType.STANDARD,
                "display_name": "Nivel 3 - Intermedio",
                "description": "Acceso intermedio. Puede ver información L3.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": False,
                "can_view_l5": False,
                "can_view_l6": False,
            },
            {
                "level": "L4",
                "card_type": AccessCard.CardType.STANDARD,
                "display_name": "Nivel 4 - Alto",
                "description": "Acceso alto. Restricted Information Section Department.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": False,
                "can_view_l6": False,
            },
            {
                "level": "L5",
                "card_type": AccessCard.CardType.STANDARD,
                "display_name": "Nivel 5 - Máximo Secreto",
                "description": "Acceso máximo secreto. Solo para personal autorizado.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": True,
                "can_view_l6": False,
            },
            {
                "level": "L5",
                "card_type": AccessCard.CardType.ETHICS_COMMITTEE,
                "display_name": "Comité de Ética",
                "description": "Acceso L5 del Comité de Ética. Información limitada.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": True,
                "can_view_l6": False,
            },
            {
                "level": "L6",
                "card_type": AccessCard.CardType.O5_COUNCIL,
                "display_name": "O5 - Miembro del Consejo",
                "description": "Acceso completo al Consejo O5.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": True,
                "can_view_l6": True,
                "can_edit_any": True,
            },
            {
                "level": "L6",
                "card_type": AccessCard.CardType.RAISA,
                "display_name": "RAISA",
                "description": "RAISA - Restricted Access Information & Security Agency.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": True,
                "can_view_l6": True,
                "can_edit_any": True,
                "is_classified": True,
            },
            {
                "level": "L6",
                "card_type": AccessCard.CardType.ADMIN_OFFICE,
                "display_name": "Administración",
                "description": "Oficina Administrativa del Sitio.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": True,
                "can_view_l6": True,
                "can_edit_any": True,
                "is_classified": True,
            },
            {
                "level": "L6",
                "card_type": AccessCard.CardType.BETA_1,
                "display_name": "Beta-1",
                "description": "Unidad Beta-1 de Respuesta Rápida.",
                "can_view_l1": True,
                "can_view_l2": True,
                "can_view_l3": True,
                "can_view_l4": True,
                "can_view_l5": True,
                "can_view_l6": True,
                "can_edit_any": True,
                "is_classified": True,
            },
        ]

        for card_data in cards_data:
            AccessCard.objects.update_or_create(
                level=card_data["level"],
                card_type=card_data["card_type"],
                defaults=card_data,
            )

        self.stdout.write(f"  Created {len(cards_data)} access cards")

    def create_factions(self):
        l1_card = AccessCard.objects.get(level="L1")
        l2_card = AccessCard.objects.get(level="L2")
        l3_card = AccessCard.objects.get(level="L3")
        l4_card = AccessCard.objects.get(level="L4")

        factions_data = [
            {
                "name": "security_department",
                "display_name": "Department of Security",
                "faction_type": Faction.Type.DEPARTMENT,
                "description": "Departamento encargado de la seguridad del sitio.",
                "icon": "🛡️",
                "color": "#2ecc71",
                "ranks": [
                    {"name": "Recluta", "level": 1, "access_card": l1_card},
                    {"name": "Guardia", "level": 2, "access_card": l1_card},
                    {"name": "Guardia Senior", "level": 3, "access_card": l2_card},
                    {"name": "Supervisor", "level": 4, "access_card": l3_card},
                    {"name": "Jefe de Seguridad", "level": 5, "access_card": l4_card},
                ],
            },
            {
                "name": "scientific_department",
                "display_name": "Scientific Department",
                "faction_type": Faction.Type.DEPARTMENT,
                "description": "Departamento de investigación y contención.",
                "icon": "🔬",
                "color": "#3498db",
                "ranks": [
                    {"name": "Investigador Junior", "level": 1, "access_card": l1_card},
                    {"name": "Investigador", "level": 2, "access_card": l2_card},
                    {"name": "Investigador Senior", "level": 3, "access_card": l3_card},
                    {
                        "name": "Director de Investigación",
                        "level": 4,
                        "access_card": l4_card,
                    },
                ],
            },
            {
                "name": "mobile_task_force",
                "display_name": "Mobile Task Force",
                "faction_type": Faction.Type.SPECIAL_FORCE,
                "description": "Fuerzas de respuesta rápida especializadas.",
                "icon": "⚔️",
                "color": "#e74c3c",
                "ranks": [
                    {"name": "Operador", "level": 1, "access_card": l2_card},
                    {"name": "Operador Senior", "level": 2, "access_card": l3_card},
                    {"name": "Líder de Equipo", "level": 3, "access_card": l4_card},
                    {"name": "Comandante MTF", "level": 4, "access_card": l4_card},
                ],
            },
            {
                "name": "ethics_committee",
                "display_name": "Administrative Department",
                "faction_type": Faction.Type.COUNCIL,
                "description": "Departamento Administrativo (Fachada)",
                "icon": "📋",
                "color": "#9b59b6",
                "is_classified": True,
                "facade_name": "Administrative Department",
                "ranks": [
                    {"name": "Miembro", "level": 1, "access_card": l3_card},
                    {"name": "Subdirector", "level": 2, "access_card": l4_card},
                    {"name": "Director", "level": 3, "access_card": l4_card},
                ],
            },
            {
                "name": "o5_council",
                "display_name": "O5 Council",
                "faction_type": Faction.Type.COUNCIL,
                "description": "Consejo O5 - Máxima autoridad.",
                "icon": "👁️",
                "color": "#f1c40f",
                "is_classified": True,
                "facade_name": "Site Direction",
                "ranks": [
                    {"name": "O5-9 a O5-13", "level": 1, "access_card": l4_card},
                    {"name": "O5-7 a O5-8", "level": 2, "access_card": l4_card},
                    {"name": "O5-1 a O5-6", "level": 3, "access_card": l4_card},
                ],
            },
            {
                "name": "raisa",
                "display_name": "RAISA",
                "faction_type": Faction.Type.CLASSIFIED,
                "description": "Restricted Access Information & Security Agency.",
                "icon": "🔒",
                "color": "#1a1a2e",
                "is_classified": True,
                "facade_name": "Intelligence Agency",
                "ranks": [
                    {"name": "Agente", "level": 1, "access_card": l4_card},
                    {"name": "Agente Senior", "level": 2, "access_card": l4_card},
                    {"name": "Director RAISA", "level": 3, "access_card": l4_card},
                ],
            },
        ]

        for faction_data in factions_data:
            ranks_data = faction_data.pop("ranks", [])

            faction, created = Faction.objects.update_or_create(
                name=faction_data["name"], defaults=faction_data
            )

            for rank_data in ranks_data:
                FactionRank.objects.update_or_create(
                    faction=faction,
                    name=rank_data["name"],
                    defaults={
                        "level": rank_data["level"],
                        "access_card": rank_data["access_card"],
                    },
                )

        self.stdout.write(f"  Created {len(factions_data)} factions")
