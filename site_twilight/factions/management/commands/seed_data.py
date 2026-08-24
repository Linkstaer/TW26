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
                "name": "Nivel 1 - Básico",
                "level": AccessCard.Level.L1,
                "card_type": AccessCard.CardType.STANDARD,
                "description": "Acceso básico al sitio. Puede ver información pública.",
            },
            {
                "name": "Nivel 2 - Restringido",
                "level": AccessCard.Level.L2,
                "card_type": AccessCard.CardType.STANDARD,
                "description": "Acceso a información restringida de nivel 2.",
            },
            {
                "name": "Nivel 3 - Confidencial",
                "level": AccessCard.Level.L3,
                "card_type": AccessCard.CardType.STANDARD,
                "description": "Acceso a información confidencial de nivel 3.",
            },
            {
                "name": "Nivel 4 - Secreto",
                "level": AccessCard.Level.L4,
                "card_type": AccessCard.CardType.STANDARD,
                "description": "Acceso a información secreta. Ve L5 solo como Codename + Facción.",
            },
            {
                "name": "Nivel 5 - Top Secret",
                "level": AccessCard.Level.L5,
                "card_type": AccessCard.CardType.STANDARD,
                "description": "Toda la información de L5, salvo archivos privados. Se muestra como L4/L5 combinada.",
            },
            {
                "name": "Comité de Ética",
                "level": AccessCard.Level.L5,
                "card_type": AccessCard.CardType.ETHICS_COMMITTEE,
                "description": "Toda la información L5 con Codename.",
                "is_classified": True,
            },
            {
                "name": "Scientific Department",
                "level": AccessCard.Level.L3,
                "card_type": AccessCard.CardType.SCIENTIFIC,
                "description": "Puede agregar apéndices y comentarios a archivos SCP.",
            },
            {
                "name": "Consejo O5",
                "level": AccessCard.Level.L6,
                "card_type": AccessCard.CardType.O5_COUNCIL,
                "description": "Redacta secciones SCP por nivel de acceso.",
                "is_classified": True,
            },
            {
                "name": "RAISA",
                "level": AccessCard.Level.L6,
                "card_type": AccessCard.CardType.RAISA,
                "description": "Redacta cualquier documento SCP o documentación.",
                "is_classified": True,
            },
            {
                "name": "Administración",
                "level": AccessCard.Level.L6,
                "card_type": AccessCard.CardType.ADMIN_OFFICE,
                "description": "Oficina Administrativa del Sitio. Acceso completo.",
                "is_classified": True,
            },
            {
                "name": "Beta-1",
                "level": AccessCard.Level.L6,
                "card_type": AccessCard.CardType.BETA_1,
                "description": "Unidad Beta-1 de Respuesta Rápida. Acceso completo.",
                "is_classified": True,
            },
        ]

        for card_data in cards_data:
            AccessCard.objects.update_or_create(
                name=card_data["name"], defaults=card_data
            )

        self.stdout.write(f"  Created {len(cards_data)} access cards")

    def create_factions(self):
        l1_card = AccessCard.objects.get(name="Nivel 1 - Básico")
        l2_card = AccessCard.objects.get(name="Nivel 2 - Restringido")
        l3_card = AccessCard.objects.get(name="Nivel 3 - Confidencial")
        l4_card = AccessCard.objects.get(name="Nivel 4 - Secreto")
        scd_card = AccessCard.objects.get(name="Scientific Department")
        ethics_card = AccessCard.objects.get(name="Comité de Ética")
        o5_card = AccessCard.objects.get(name="Consejo O5")
        raisa_card = AccessCard.objects.get(name="RAISA")

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
                    {"name": "Investigador Senior", "level": 3, "access_card": scd_card},
                    {
                        "name": "Director de Investigación",
                        "level": 4,
                        "access_card": scd_card,
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
                "display_name": "Ethics Committee",
                "faction_type": Faction.Type.COUNCIL,
                "description": "Gestión administrativa y supervisión interna del sitio.",
                "icon": "📋",
                "color": "#9b59b6",
                "is_classified": True,
                "facade_name": "Administrative Department",
                "ranks": [
                    {"name": "Miembro", "level": 1, "access_card": ethics_card},
                    {"name": "Subdirector", "level": 2, "access_card": ethics_card},
                    {"name": "Director", "level": 3, "access_card": ethics_card},
                ],
            },
            {
                "name": "o5_council",
                "display_name": "O5 Council",
                "faction_type": Faction.Type.COUNCIL,
                "description": "Dirección general del sitio.",
                "icon": "👁️",
                "color": "#f1c40f",
                "is_classified": True,
                "facade_name": "Site Direction",
                "ranks": [
                    {"name": "O5-9 a O5-13", "level": 1, "access_card": o5_card},
                    {"name": "O5-7 a O5-8", "level": 2, "access_card": o5_card},
                    {"name": "O5-1 a O5-6", "level": 3, "access_card": o5_card},
                ],
            },
            {
                "name": "raisa",
                "display_name": "RAISA",
                "faction_type": Faction.Type.CLASSIFIED,
                "description": "Agencia de inteligencia y seguridad de la información.",
                "icon": "🔒",
                "color": "#1a1a2e",
                "is_classified": True,
                "facade_name": "Intelligence Agency",
                "ranks": [
                    {"name": "Agente", "level": 1, "access_card": raisa_card},
                    {"name": "Agente Senior", "level": 2, "access_card": raisa_card},
                    {"name": "Director RAISA", "level": 3, "access_card": raisa_card},
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
