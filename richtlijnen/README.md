# Richtlijnen — herziening Veenweideboerenvisie

Deze map is het complete stuurdossier voor de herziening. Hij hoort in de repo naast de bestaande `terminologie.md`, en is zelfstandig leesbaar: een verse sessie heeft aan deze map plus het te bewerken `content/`-bestand genoeg.

## De zeven documenten

| Bestand | Wat het is | Wanneer lezen |
|---|---|---|
| `redactiebrief.md` | **Het hoofddocument.** Deel I: toetslijst van 35 regels. Deel II: zeventien toelichtingen, inclusief structuurvoorstel (§15), werkwijze (§16) en bloktypen-regel (§17) | Volledig, vóór elke schrijfsessie |
| `besluitenlog.md` | Besluiten die ná de brief vallen — vijftien bij de start, groeit tijdens het schrijven | Volledig, vóór elke schrijfsessie |
| `bloktypen.md` | Alle dertig accentkaders met bestemming: lopende tekst, fiche of bijlage | Bij elk hoofdstuk dat kaders bevat |
| `correctielijst.md` | Feitcorrecties per bestand, afvinkbaar | Bij elk hoofdstuk; na het schrijven afvinken |
| `commentaar-clusters.md` | De ~120 reviewopmerkingen, geclusterd naar oorzaak | Alleen bij twijfel over de herkomst van een besluit |
| `terminologie.md` | Harde begripsregels (bestaand; wordt bijgewerkt conform redactiebrief 28a/28b en §13) | Doorlopend |
| `vic-missie-en-programmas.md` | Afschrift uit het strategiedossier: de statutaire missie, de ambitie 2026–2032, en wat programma A en B zijn | Zodra een hoofdstuk het VIC, de missie of de programma's noemt |
| `doorwerking-programmas.md` | Wat uit de visiediscussie doorwerkt naar programma A en B | **Niet** tijdens het schrijven — bij de programmavoorstellen |

## Werkwijze in het kort

1. Eén hoofdstuk, één verse sessie.
2. Lees `redactiebrief.md` en `besluitenlog.md` volledig.
3. Wijzig het bestand in `content/`. Geen nieuwe tekst — de diff moet exact tonen wat veranderde.
4. Draai de machinale checks (`verify.py`, uit te breiden conform redactiebrief §16.2).
5. Doe de leescheck (§16.3).
6. Noteer nieuwe besluiten in `besluitenlog.md`.

Volgorde van de rondes: redactiebrief §16.6. Ontbreekt een getal, bron of feit: markering (`[[CIJFER:…]]`, `[[BRON:…]]`, `[[CHECK DOUWE:…]]`, `[[KEUZE:…]]`), nooit een plausibel cijfer.

## Wat níet in deze map hoort

Twee werkdocumenten leven buiten de repo, bij Tim:

- `dossier-vic-strategie.md` — het strategiedossier voor het bestuur (2 september). Daar hoort de visie bij als appendix, niet andersom. **Let op:** omdat de visie een appendix is, moet zij naar de missie en de ambitie uit dat dossier kunnen verwijzen. Die zijn daarom als afschrift in `vic-missie-en-programmas.md` gezet. Zonder dat afschrift kan een verse sessie de missie niet kennen, en dat is op 18-8 precies misgegaan.
- `uitvraag-scope-getallen.md` — de onderzoeksuitvraag voor de scope-cijfers; is uitgevoerd, resultaat verwerkt in redactiebrief §5 en de correctielijst. **Let op, zelfde valkuil als hierboven:** de getallen in §5 zijn daar nagetrokken, maar een sessie kan dat niet controleren. Wat is nagetrokken is het gétal; of de definitie erachter klopt met hoe de visie het gebruikt, is een aparte vraag. Bij twijfel een `[[BRON]]` plaatsen en niet aannemen dat §5 sluitend is. Zie de markering bij de 10.000 ha in `content/scope.md`.
