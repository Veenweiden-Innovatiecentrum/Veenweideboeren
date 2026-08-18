# Veenweideboeren — werkinstructie voor Claude Code

Dit is de bronrepository van de Veenweideboerenvisie. De tekst staat als Markdown in `content/`; die wordt herzien volgens een vastgelegd stuurdossier in `richtlijnen/`.

## De waarheid: de website die het bestuur gelezen heeft

De geldige tekst is de website op `veenweideboeren-visie.vercel.app`, want dát is wat het bestuur op 1 juli las. Al het commentaar in `feedback/` gaat daarover.

Die website staat in `webapp/`. Op 18 augustus 2026 is zijn tekst teruggehaald naar `content/*.md` met `importeer.py`, verliesvrij: alle veertien hoofdstukken bouwen woordelijk terug naar wat er online staat.

**Daarmee zijn `content/` en de website weer één.** Bewaak dat:

- `python3 build.py site visie` vergelijkt de twee en schrijft niets. Alles moet "gelijk" zijn, behalve waar je zelf net iets hebt gewijzigd.
- Overschrijven van de website vraagt `--schrijf`. Nooit blind doen.
- Loopt het uiteen zonder dat jij het veroorzaakte, dan is er buiten de repo om aan de site gewerkt. Stoppen en melden.

`dist/` en `origineel/` zijn géén waarheid. `dist/` is een bijproduct in een andere vormgeving dan het bestuur kent; `origineel/` is het aangeleverde v2-document van vóór de repo-conversie en inhoudelijk het oudst.

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
2. Draai `python3 stijlcheck.py <bestand>.md`. Dat meet schrijfsporen — em-dashes, "niet X maar Y", drieslagen, signaalwoorden, zinsritme — tegen de letterlijke citaten van de commentatoren in `feedback/`. **De hoofdstukken in `content/` zijn zelf met AI geschreven en zijn dus geen norm.** Streef naar de mensen-nulmeting, niet naar het documentgemiddelde. Meld de uitslag in de samenvatting. Het blokkeert niets en is geen verbodslijst.
3. Doe de leescheck: de zes vragen in redactiebrief §16.3.
4. Vink de verwerkte punten af in `richtlijnen/correctielijst.md`.
5. Vat voor de gebruiker samen: wat is gewijzigd, welke markeringen staan open, welke checks faalden en waarom dat terecht of onterecht is.

## Bouwen

Na tekstwijzigingen: `python build.py document` en de output in `dist/` controleren. `dist/` nooit handmatig bewerken.

Om één hoofdstuk aan de gebruiker voor te leggen: `python build.py hoofdstuk <sectie-id>` → `dist/hoofdstukken/<sectie-id>.html`. Zelfde opmaak als het document, zonder navigatie. Leesversie ter beoordeling, geen publicatie.

## Twee versies naast elkaar — dit is hoe de gebruiker meekijkt

De gebruiker houdt twee browservensters naast elkaar open, allebei in de vormgeving die het bestuur kent:

| Venster | Wat het is |
|---|---|
| **de bestuursversie** | `veenweideboeren-visie.vercel.app` — onaangeroerd online. Dit is het vergelijkingspunt |
| **de herziening** | de webapp lokaal geserveerd, met de bijgewerkte tekst |

Meld na elke wijziging dat de herziening is bijgewerkt, zodat de gebruiker weet dat verversen zin heeft.

## Context

De herziening dient een bestuursvergadering op 2 september 2026. De toon is het belangrijkste: handreiking aan het huidige beleid, geen tegenstelling — toetsregel 1 tot en met 6 gaan boven alles.
