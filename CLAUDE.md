# Veenweideboeren — werkinstructie voor Claude Code

Dit is de bronrepository van de Veenweideboerenvisie. De tekst staat als Markdown in `content/`; die wordt herzien volgens een vastgelegd stuurdossier in `richtlijnen/`.

## Verplicht bij elke sessie, vóór elke wijziging

1. Lees `richtlijnen/redactiebrief.md` **volledig** — deel I is de toetslijst, deel II de toelichting.
2. Lees `richtlijnen/besluitenlog.md` **volledig** — besluiten die na de brief zijn gevallen.
3. Werk aan **één hoofdstuk per sessie**. Welk hoofdstuk, zegt de gebruiker; de volgorde staat in redactiebrief §16.6.

## Bij het hoofdstuk zelf

- Raadpleeg `richtlijnen/bloktypen.md` voor de bestemming van elk accentkader in dit bestand.
- Raadpleeg `richtlijnen/correctielijst.md` voor de feitcorrecties van dit bestand; vink af wat verwerkt is.
- `richtlijnen/terminologie.md` geldt doorlopend.
- `richtlijnen/commentaar-clusters.md` is historisch — alleen lezen bij twijfel over de herkomst van een besluit.
- `richtlijnen/doorwerking-programmas.md` is voor de programmavoorstellen, **niet** voor de visie.

## Harde regels

- **Wijzig bestaande bestanden in `content/`** — schrijf niet opnieuw. De diff moet exact en alleen tonen wat veranderde.
- **Geen besluit nemen dat niet in de redactiebrief of het besluitenlog staat.** Kom je zo'n keuze tegen: markering plaatsen, doorgaan, aan het eind van de sessie voorleggen aan de gebruiker.
- **Spreekt de brontekst een besluit tegen: stoppen en melden.** Dat is een reden om het besluit te herzien, geen redactiekwestie.
- **Ontbreekt een getal, bron of feit: markering, nooit een plausibel cijfer.** Vormen: `[[CIJFER: wat]]`, `[[BRON: waarvoor]]`, `[[CHECK DOUWE: wat]]`, `[[KEUZE: opties]]`.
- Nieuwe besluiten die de gebruiker tijdens de sessie neemt: **direct noteren in `richtlijnen/besluitenlog.md`**, met datum, hoofdstuk en reden.

## Na het schrijven, vóór het afronden

1. Draai `python verify.py` (checks conform redactiebrief §16.2 — nog uit te breiden; staat een check er nog niet in, voer hem dan handmatig uit met grep).
2. Doe de leescheck: de zes vragen in redactiebrief §16.3.
3. Vink de verwerkte punten af in `richtlijnen/correctielijst.md`.
4. Vat voor de gebruiker samen: wat is gewijzigd, welke markeringen staan open, welke checks faalden en waarom dat terecht of onterecht is.

## Bouwen

Na tekstwijzigingen: `python build.py document` en de output in `dist/` controleren. `dist/` nooit handmatig bewerken.

Om één hoofdstuk aan de gebruiker voor te leggen: `python build.py hoofdstuk <sectie-id>` → `dist/hoofdstukken/<sectie-id>.html`. Zelfde opmaak als het document, zonder navigatie. Leesversie ter beoordeling, geen publicatie.

## Twee documenten naast elkaar — dit is hoe de gebruiker meekijkt

In `dist/vergelijk/` staan twee complete documenten. De gebruiker houdt ze in twee browserwindows naast elkaar open terwijl de herziening vordert.

| Bestand | Wat het is |
|---|---|
| `1 — huidige visie (bevroren).html` | De visie zoals die op `main` staat. **Nooit aanraken, nooit opnieuw bouwen, nooit hernoemen.** Dit is het vergelijkingspunt |
| `2 — herziene visie (groeit mee).html` | De herziening. `build.py document` werkt deze bij; de gebruiker ververst zijn browser en ziet de nieuwe stand |

`build.py document` schrijft bestand 2 en de index automatisch — er is geen apart commando voor. Bestand 1 wordt door geen enkel buildpad geschreven.

Meld na elke wijziging dat bestand 2 is bijgewerkt, zodat de gebruiker weet dat verversen zin heeft.

De map `origineel/` is iets anders: dat is het aangeleverde v2-document van vóór de repo-conversie, inhoudelijk ouder dan `main`. Gebruik dat niet als vergelijkingspunt.

## Context

De herziening dient een bestuursvergadering op 2 september 2026. De toon is het belangrijkste: handreiking aan het huidige beleid, geen tegenstelling — toetsregel 1 tot en met 6 gaan boven alles.
