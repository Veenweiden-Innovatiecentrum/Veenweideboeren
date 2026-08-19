# Hoofdstukregister

*De enige plek waar staat welk nummer een hoofdstuk krijgt en hoe ver het is. Afgeleid van redactiebrief §15 (hoofdstukvolgorde) en §16.6 (rondes).*

**Twee dingen leunen hierop, dus houd het bij:**

- `python3 verwijzingen.py` controleert of elke verwijzing in de tekst — "hoofdstuk 4", "bijlage 17", "sectie D", "1.3" — klopt en al opgelost kan worden.
- `python3 build.py site` schrijft de werkstandregel onder elke hoofdstukkop uit dit register. Niet meer met de hand in `v4-visie.jsx`.

> **Let op, 19-8:** de nummers in dit register en in de tekst zijn de **oude** nummering. Het skelet (`skelet.md`) draagt de nieuwe: hoofdstuk 3 (Begrippen) is vervallen en C staat vóór de aktes, dus alles vanaf 4 schuift op. Dit register gaat per hoofdstuk om op het moment dat dat hoofdstuk herzien wordt; de omzettabel staat in redactiebrief §15.

**Bijwerken op twee momenten:** als een hoofdstuk zijn nummer krijgt (kolom `nummer` gaat van leeg naar het getal, en de `##`-kop in `content/` mee), en als een hoofdstuk herzien is (kolom `stand`).

De volgorde in dit register is de volgorde van `volgorde.txt`. Hoofdstukken die nog niet bestaan staan onderaan, zonder id.

| id | nummer | ronde | stand |
|---|---|---|---|
| samenvatting | — | 6 | laag 1, wordt als laatste gemaakt uit het afgeronde verhaal |
| walkthrough | — | — | leeshulp van de website, geen hoofdstuk |
| scope | 1 | 1 | herzien |
| aannames | 2 | 1 | herzien; 1 markering open (onderbouwing 70-80%) |
| intro | — | — | wachtkamer, hoort leeg te raken |
| a-klem | 4 | 2 | nog de bestuursversie |
| b-opgaves | 5 | 2 | nog de bestuursversie |
| c-omslag | 8 | 1 | herzien; 4 markeringen open (koolstofvoorraad, vindplaats verdringingsreeks, I&W-uitgangspunt, aangevoerd water) |
| d-concept | 10 | 3 | nog de bestuursversie |
| e-aktes | 6, 7, 9 | 2 en 1 | nog de bestuursversie, wordt in drieën gesplitst |
| f-ondernemer | 11 | 3 | nog de bestuursversie |
| f-overheid | 12 | 3 | nog de bestuursversie |
| f3-bedrijfsleven | 13 | 3 | nog de bestuursversie, groeit naar een volwaardig hoofdstuk |
| g-perspectief | 14 | 3 | nog de bestuursversie |
| h-risicos | 15 | 4 | nog de bestuursversie |
| slot | 16 | 4 | nog de bestuursversie, wordt herschreven |
| bijlage-driesporen | 17 | 5 | in aanbouw, 1 van de 9 blokken verhuisd |

## Nog te maken

| nummer | hoofdstuk | ronde | herkomst |
|---|---|---|---|
| 3 | Begrippen | 4 | het begrippenkader uit de wachtkamer |

## Buiten de visie

| id | Waarom |
|---|---|
| i-vic-rol | Verhuisd naar het programmavoorstel (redactiebrief §14: "blijft daar"). Staat niet in `volgorde.txt`. Een verwijzing naar "sectie I" in de visie is dus altijd fout |
| pv-opening, pv-programmalijnen | Horen bij het programmavoorstel, niet bij de visie |
