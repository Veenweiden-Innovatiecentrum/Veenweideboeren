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
| intro | — | — | wachtkamer, hoort leeg te raken; nog 2 blokken (stikstofdossier → ronde 4, begrippen → bijlage 17.4). Routering in de correctielijst |
| a-klem | 3 | 2 | **herzien**, met de eindredactieslag van 20-8 (em-dashes, holle verwijzingen, AI-sporen). 1.068 woorden en 864 leesregel. Eén open punt: het cijfer voor het inkomensgat (JUMP) |
| b-opgaves | 4 | 2 | **herzien (20-8): drie secties, geordend naar dwang** — 4.1 wat er moet · 4.2 welk dossier nu het hardst duwt · 4.3 wat er ook gevraagd wordt zonder dat het moet. **Herzien 20-8.** De tien dimensies staan **drie hard en zeven zacht** (klimaat-bedrijf is 20-8 zacht geworden: geen norm per bedrijf voor methaan); de weidevogel is naar hoofdstuk 5 verhuisd. 820 woorden tegen 832; het budget van 650 haalt het niet omdat 316 woorden tabelcel van de auteurs zijn en die alleen verhuizen. Geen markering open |
| c-omslag | 5 | 1 | **herzien (20-8): vier secties** — 5.1 wat hier al gebeurt en wie het betaalt · **5.2 de kans zit waar de klem het strakst is** (nieuw scharnier) · 5.3 waar deze opgaven een product kunnen worden, met het weidevogelbeheer als grensgeval en de drie horden ingekort · **5.4 en daarom een ondernemende boer**, met de marge-omkering vooraan. 2.138 woorden totaal en 1.838 leesregel tegen 2.025; nul tabellen. 5.2 heet 'De ruimte die vrijkomt'; 5.3 heeft vier routes uit de JUMP-concepten (5b, 4a, 8a, 6b); 5.4 sluit op de synthese dat de investeerder liefst de blijvende boer is. Open: de tegenstrijdige cijfers over de watervraag (30-40% versus factor 1,5-3). Nog toe te voegen: twee bronnen en één getal, de lijst staat in `correctielijst.md` |
| scenario-1 | 6 | 2 | **6.1 geschreven (20-8)**; 6.2 en 6.3 dragen hun nummer en skelettitel maar staan er nog als bestuursversie. Uit de kaartvorm, 905 woorden leesregel waarvan 84 procent woordelijk van de auteurs. De dimensielijst staat er nog en gaat naar hoofdstuk 9. Start bij `richtlijnen/handoff-deel-3-scenarios.md` |
| scenario-2 | 7 | 2 | **nu aan de beurt**; nog de bestuursversie, maar uit de kaartvorm en met de koppen 7.1, 7.2 en 7.3 op hun plek. De vier driesporenkaders staan er nog en gaan naar bijlage 17; de dimensielijst gaat naar hoofdstuk 9 |
| scenario-3 | 8 | 1 | herzien; open punt in de correctielijst: tweede pijl voor de markt in het kernbeeld, beeldwerk |
| d-concept | 10 | 3 | bestuursversie, met één nieuwe sectie vooraan: "veenweideboer is een schaal, geen categorie" (19-8) |
| f-ondernemer | 11 | 3 | nog de bestuursversie |
| f-overheid | 12 | 3 | nog de bestuursversie |
| f3-bedrijfsleven | 13 | 3 | nog de bestuursversie, groeit naar een volwaardig hoofdstuk |
| g-perspectief | 14 | 3 | bestuursversie, met de routes omgebouwd naar drie (19-8) |
| h-risicos | 15 | 4 | nog de bestuursversie |
| slot | 16 | 4 | nog de bestuursversie, wordt herschreven |
| bijlage-driesporen | 17 | 5 | in aanbouw, 4 van de 9 blokken verhuisd |

## Nog te maken

| id | nummer | ronde | stand |
|---|---|---|---|
| *nog geen bestand* | 9 | 2 | **Wat de drie scenario's naast elkaar opleveren** — nieuw op 20-8 (Tim). Drie secties: 9.1 dezelfde tien dimensies drie keer · 9.2 wie de rekening betaalt en wanneer · 9.3 het ontwikkelbeeld. De inhoud komt uit 6.3, 7.3 en 8.3, die daarmee vervallen. Skelet staat er; het bestand nog niet, dus ook nog niet in `volgorde.txt` |

*Het begrippenhoofdstuk is 19-8 vervallen: de begrippen gaan naar bijlage 17 en de scenario-introductie naar hoofdstuk 6.*

> **20-8: de nummering is één opgeschoven vanaf 9.** Hoofdstuk 9 tot 16 zijn 10 tot 17 geworden om plaats te maken voor het vergelijkingshoofdstuk. Doorgevoerd in `content/`, het skelet, de redactiebrief en de richtlijnen. **Het besluitenlog van vóór 20-8 draagt de oude nummering** en is bewust niet herschreven: een logboek dat je achteraf bijstelt, is geen logboek meer.

## Buiten de visie

| id | Waarom |
|---|---|
| i-vic-rol | Verhuisd naar het programmavoorstel (redactiebrief §14: "blijft daar"). Staat niet in `volgorde.txt`. Een verwijzing naar "sectie I" in de visie is dus altijd fout |
| pv-opening, pv-programmalijnen | Horen bij het programmavoorstel, niet bij de visie |
