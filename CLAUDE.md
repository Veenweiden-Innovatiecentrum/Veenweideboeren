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

## Context

De herziening dient een bestuursvergadering op 2 september 2026. De toon is het belangrijkste: handreiking aan het huidige beleid, geen tegenstelling — toetsregel 1 tot en met 6 gaan boven alles.
