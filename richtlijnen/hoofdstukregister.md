# Hoofdstukregister

*De enige plek waar staat welk nummer een hoofdstuk krijgt en hoe ver het is. Afgeleid van redactiebrief §15 (hoofdstukvolgorde) en §16.6 (rondes).*

**Twee dingen leunen hierop, dus houd het bij:**

- `python3 verwijzingen.py` controleert of elke verwijzing in de tekst — "hoofdstuk 4", "bijlage 17", "sectie D", "1.3" — klopt en al opgelost kan worden.
- `python3 build.py site` schrijft de werkstandregel onder elke hoofdstukkop uit dit register. Niet meer met de hand in `v4-visie.jsx`.

> **19-8: het skelet is leidend.** `richtlijnen/skelet.md` bepaalt de nummers en de titels, en dit register volgt. De omzetting van de oude naar de nieuwe nummering staat in redactiebrief §15. De `##`-koppen in `content/` dragen de nieuwe nummers zodra een hoofdstuk herzien is; de nog niet herziene hoofdstukken dragen hun letter.

**Bijwerken op twee momenten:** als een hoofdstuk zijn nummer krijgt (kolom `nummer` gaat van leeg naar het getal, en de `##`-kop in `content/` mee), en als een hoofdstuk herzien is (kolom `stand`).

De volgorde in dit register is de volgorde van `volgorde.txt`. Hoofdstukken die nog niet bestaan staan onderaan, zonder id.

| id | nummer | ronde | stand |
|---|---|---|---|
| samenvatting | — | 6 | laag 1, wordt als laatste gemaakt uit het afgeronde verhaal |
| walkthrough | — | — | leeshulp van de website, geen hoofdstuk |
| scope | 1 | 1 | herzien |
| aannames | 2 | 1 | herzien; 1 markering open (onderbouwing 70-80%) |
| intro | — | — | wachtkamer, hoort leeg te raken; nog 2 blokken (stikstofdossier → ronde 4, begrippen → bijlage 16.4). Routering in de correctielijst |
| a-klem | 3 | 2 | **herzien**; 77% van de woorden van de auteurs. Eén open punt: het cijfer voor het inkomensgat (JUMP) |
| b-opgaves | 4 | 2 | nog de bestuursversie |
| c-omslag | 5 | 1 | herzien; **markeringen 19-8 uit de tekst gehaald, drie bronnen en één getal nog toe te voegen** — de lijst staat in `correctielijst.md` onder c-omslag |
| e-aktes | 6, 7 | 2 | nog de bestuursversie; akte III is 19-8 eruit gehaald naar `akte-3.md` |
| akte-3 | 8 | 1 | herzien; open punt in de correctielijst: tweede pijl voor de markt in het kernbeeld, beeldwerk |
| d-concept | 9 | 3 | bestuursversie, met één nieuwe sectie vooraan: "veenweideboer is een schaal, geen categorie" (19-8) |
| f-ondernemer | 10 | 3 | nog de bestuursversie |
| f-overheid | 11 | 3 | nog de bestuursversie |
| f3-bedrijfsleven | 12 | 3 | nog de bestuursversie, groeit naar een volwaardig hoofdstuk |
| g-perspectief | 13 | 3 | bestuursversie, met de routes omgebouwd naar drie (19-8) |
| h-risicos | 14 | 4 | nog de bestuursversie |
| slot | 15 | 4 | nog de bestuursversie, wordt herschreven |
| bijlage-driesporen | 16 | 5 | in aanbouw, 3 van de 9 blokken verhuisd |

## Nog te maken

*Leeg. Het begrippenhoofdstuk is 19-8 vervallen: de begrippen gaan naar bijlage 16 en de akte-introductie naar hoofdstuk 6.*

## Buiten de visie

| id | Waarom |
|---|---|
| i-vic-rol | Verhuisd naar het programmavoorstel (redactiebrief §14: "blijft daar"). Staat niet in `volgorde.txt`. Een verwijzing naar "sectie I" in de visie is dus altijd fout |
| pv-opening, pv-programmalijnen | Horen bij het programmavoorstel, niet bij de visie |
