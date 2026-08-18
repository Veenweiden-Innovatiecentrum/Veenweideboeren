# Veenweideboeren — werkinstructie voor Claude Code

Dit is de bronrepository van de Veenweideboerenvisie. De tekst staat als Markdown in `content/`; die wordt herzien volgens een vastgelegd stuurdossier in `richtlijnen/`.

## De waarheid: de website die het bestuur gelezen heeft

De geldige tekst is de website op `veenweideboeren-visie.vercel.app`, want dát is wat het bestuur op 1 juli las. Al het commentaar in `feedback/` gaat daarover.

Die website staat in `webapp/`. Op 18 augustus 2026 is zijn tekst teruggehaald naar `content/*.md` met `importeer.py`, verliesvrij: alle veertien hoofdstukken bouwen woordelijk terug naar wat er online staat.

**Daarmee zijn `content/` en de website weer één.** Bewaak dat:

- `bestuursversie/content-visie.js` is de bevroren tekst van 1 juli, rechtstreeks uit commit `aa559b5`. **Nooit bijwerken.** Dit is het ijkpunt.
- `python3 build.py site visie` vergelijkt `content/` met die bevroren versie en schrijft niets. Alles moet "gelijk" zijn, behalve de hoofdstukken die je zelf hebt herzien.
- Overschrijven van de lokale website vraagt `--schrijf`. Nooit blind doen. Let op: `webapp/site/content-visie.js` bevat ná de eerste `--schrijf` de herziening, dus vergelijk daar niet meer tegen — daarom bestaat `bestuursversie/`.
- Wijkt een hoofdstuk af dat jij niet hebt aangeraakt, dan is er buiten de repo om gewerkt. Stoppen en melden.

`dist/` en `origineel/` zijn géén waarheid. `dist/` is een bijproduct in een andere vormgeving dan het bestuur kent; `origineel/` is het aangeleverde v2-document van vóór de repo-conversie en inhoudelijk het oudst.

## Verplicht bij elke sessie, vóór elke wijziging

1. Lees `richtlijnen/redactiebrief.md` **volledig** — deel I is de toetslijst, deel II de toelichting.
2. Lees `richtlijnen/besluitenlog.md` **volledig** — besluiten die na de brief zijn gevallen.
3. Werk aan **één hoofdstuk per sessie**. Welk hoofdstuk, zegt de gebruiker; de volgorde staat in redactiebrief §16.6.

## Bij het hoofdstuk zelf

- **Nummer het hoofdstuk** met zijn nummer uit redactiebrief §15, en de subkoppen daarbinnen: `## 1 — Waar dit over gaat`, dan `### 1.1`, `### 1.2`. Dat gebeurt op het moment dat het hoofdstuk herzien wordt; de letters A tot H blijven tot dan staan.
- Raadpleeg `richtlijnen/bloktypen.md` voor de bestemming van elk accentkader in dit bestand.
- Noemt het hoofdstuk het VIC, de missie of de programma's: `richtlijnen/vic-missie-en-programmas.md`. Verzin daar niets bij — de statutaire missie en de programmafeiten staan er letterlijk in.
- Zet je een **aantal bedrijven** in de tekst: lees eerst `richtlijnen/scope-getallen-bedrijven.md`. Daar staat het te citeren getal met zijn afbakening, en vier getallen die circuleren en onbruikbaar zijn (waaronder één dat expliciet fictief is).
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

1. Draai `python3 verwijzingen.py`. Die doet twee dingen.
   - **Kruisverwijzingen** ("hoofdstuk 4", "bijlage 17", "sectie D", "zie 1.3") getoetst tegen `richtlijnen/hoofdstukregister.md`. "FOUT" moet leeg zijn; "NOG NIET OP TE VOLGEN" mag, dat zijn verwijzingen die kloppen op de eindstructuur maar waarvan het hoofdstuk zijn nummer nog niet draagt.
   - **Terugverwijzingen zonder antecedent**: abstracte woorden ("de fase", "de redenering", "de vraag") die met een bepaald lidwoord worden aangewezen zonder eerder genoemd te zijn. Dit is een kandidatenlijst met ruis, geen foutenlijst — ongeveer één op drie is echt. Loop hem langs en noem het ding bij naam waar dat nodig is.
2. Draai `python verify.py` (checks conform redactiebrief §16.2 — nog uit te breiden; staat een check er nog niet in, voer hem dan handmatig uit met grep). **Let op:** dat script vergelijkt `dist/` met `origineel/` en is sinds de conversie achterhaald; het faalt op hoofdstukken die je niet hebt aangeraakt.
3. Draai `python3 stijlcheck.py <bestand>.md`. Dat meet schrijfsporen — em-dashes, "niet X maar Y", drieslagen, signaalwoorden, zinsritme — tegen de letterlijke citaten van de commentatoren in `feedback/`. **De hoofdstukken in `content/` zijn zelf met AI geschreven en zijn dus geen norm.** Streef naar de mensen-nulmeting, niet naar het documentgemiddelde. Meld de uitslag in de samenvatting. Het blokkeert niets en is geen verbodslijst.
4. Doe de leescheck: de zes vragen in redactiebrief §16.3.
5. Vink de verwerkte punten af in `richtlijnen/correctielijst.md`.
6. Vat voor de gebruiker samen: wat is gewijzigd, welke markeringen staan open, welke checks faalden en waarom dat terecht of onterecht is.
7. **Lever een verantwoording per hoofdstuk, en opnieuw na elke verbeteringsslag** op datzelfde hoofdstuk. Drie delen, in deze volgorde:
   - **Wat er beter is geworden** — je eigen oordeel, met wat het hoofdstuk eerst deed en nu doet. Ook wat er níet beter van werd.
   - **Volgens de redactie** — welke toetsregels en besluiten uit `redactiebrief.md` en `besluitenlog.md` zijn geland, per regelnummer. En welke van toepassing waren maar niet gehaald.
   - **Volgens de correcties** — loop het cluster in `commentaar-clusters.md` langs dat over dít hoofdstuk gaat, opmerking voor opmerking, met de naam van de commentator. Zeg per opmerking: verwerkt, deels, of niet. `correctielijst.md` dekt alleen cluster 8 (feiten), dus de andere clusters hebben geen afvinklijst en vallen anders stil. Wat je daar vindt en niet ter plekke kunt oplossen, zet je als open punt in `correctielijst.md` onder dat bestand.

## Delen met andere sessies — na elke wijziging, niet aan het eind

`visie-tekst.md` in de wortel is **het deelbestand**: alle hoofdstuktekst uit `content/` in één bestand, in de volgorde van `volgorde.txt`, met ingebedde afbeeldingen eruit. Een Claude-sessie of persoon zonder toegang tot deze map leest daar de hele actuele tekst op één vast adres:

```
https://raw.githubusercontent.com/Veenweiden-Innovatiecentrum/Veenweideboeren/ronde-1/visie-tekst.md
```

**Dat adres is alleen zo actueel als de laatste push.** Dus hoort bij het afronden van elke wijziging, ook een kleine:

```
python3 build.py tekst        # visie-tekst.md opnieuw maken
git add -A && git commit && git push
```

Lukt het ophalen aan de andere kant niet, dan is dat een rate limit op het IP van de fetcher en niet een verkeerd pad; de tarball van `codeload.github.com` werkt dan wel. Nooit een tweede versie van deze tekst ergens anders neerzetten: dan zijn er twee waarheden en dat is precies de fout die deze repo al een keer drie dagen heeft gekost.

Voor de sessie die aan programma A werkt is er daarnaast `richtlijnen/handoff-programma-a.md`, zelfstandig leesbaar. Werk die bij als er iets verandert dat A raakt.

## Bouwen

Na tekstwijzigingen: `python build.py document` en de output in `dist/` controleren. `dist/` nooit handmatig bewerken.

Om één hoofdstuk aan de gebruiker voor te leggen: `python build.py hoofdstuk <sectie-id>` → `dist/hoofdstukken/<sectie-id>.html`. Zelfde opmaak als het document, zonder navigatie. Leesversie ter beoordeling, geen publicatie.

## Twee versies naast elkaar — dit is hoe de gebruiker meekijkt

De gebruiker houdt twee browservensters naast elkaar open, allebei in de vormgeving die het bestuur kent:

| Venster | Wat het is |
|---|---|
| **de bestuursversie** | `veenweideboeren-visie.vercel.app` — onaangeroerd online. Dit is het vergelijkingspunt |
| **de herziening** | de webapp lokaal geserveerd, met de bijgewerkte tekst |

Serveren gaat met `python3 serveer.py` (poort 18620). Gebruik **niet** `python3 -m http.server`: die stuurt geen cache-regels mee en dan blijft de browser de oude tekst tonen na een herbouw. Bijwerken van de lokale versie is `python3 build.py site visie --schrijf`, altijd ná de vergelijking zonder `--schrijf`.

Onder elke hoofdstukkop staat lokaal een werkstandregel met bronbestand, hoofdstuknummer, ronde en stand. Die komt uit **`richtlijnen/hoofdstukregister.md`** en wordt door `build.py site` meegeschreven; houd dus dát register bij, niet de lezer. Zet `WERKSTAND_ZICHTBAAR` in `webapp/site/v4-visie.jsx` op `false` vóór publicatie.

Het register is ook de bron voor `verwijzingen.py`. Krijgt een hoofdstuk zijn nummer, dan gaan drie dingen tegelijk mee: de `##`-kop in `content/`, de kolom `nummer` in het register, en de verwijzingen die daarnaar wijzen worden opeens wél op te volgen.

Meld na elke wijziging dat de herziening is bijgewerkt, zodat de gebruiker weet dat verversen zin heeft.

## Context

De herziening dient een bestuursvergadering op 2 september 2026. De toon is het belangrijkste: handreiking aan het huidige beleid, geen tegenstelling — toetsregel 1 tot en met 6 gaan boven alles.
