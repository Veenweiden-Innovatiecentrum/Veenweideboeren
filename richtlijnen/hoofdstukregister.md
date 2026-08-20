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
| scenario-1 | 6 | 2 | **áf op 20-8, vier secties**: 6.1 wat dit scenario is (250) · 6.2 er wordt gestuurd op middelen (226) · 6.3 waarom dit geen stabiele toestand is (288, de drie termijnen in één alinea) · 6.4 de motor (290). 1.120 woorden leesregel. Uit de kaartvorm, met de scenariotabel en de illustratie in 6.1. Eén markering open: het areaal dat de middengroep beheert. De dimensielijst staat onderaan en gaat naar hoofdstuk 9 |
| scenario-2 | 7 | 2 | **áf op 20-8, vier secties**: 7.1 wat dit scenario is (286) · 7.2 de maatregelen kloppen, er ligt alleen niets onder (369, met 2 fiches) · 7.3 waarom de verbetering niet standhoudt (238) · 7.4 de motor (245). 1.072 woorden leesregel tegen 1.616 aan het begin van 20-8. Geen markering open. De vier driesporenkaders zijn 20-8 naar bijlage 17 verhuisd, waarmee het hoofdstuk van 1.616 naar 1.237 woorden ging; de dimensielijst gaat nog naar hoofdstuk 9 |
| scenario-3 | 8 | 1 | **áf op 20-8, vier secties**: 8.1 wat dit scenario is (189) · 8.2 de omslag, mét de twee geldstromen (381) · 8.3 waarom het dan wél standhoudt (209) · 8.4 de motor (249). 1.028 woorden leesregel. De sectie "wat dat betekent per opgave" is opgeheven; de dimensielijst en het ontwikkelbeeld staan onderaan, klaar voor hoofdstuk 9. Open punt in de beeldlijst: tweede pijl voor de markt in het kernbeeld |
| scenario-vergelijking | 9 | 2 | **in de steigers (20-8)**: 9.1 dezelfde tien dimensies drie keer, met de tabel uit de gesplitste partial · 9.2 wie de rekening betaalt en wanneer, met het kostendiagram en de drie alinea's van de auteurs · 9.3 wat de drie samen laten zien, nog te schrijven. De partial `e-aktes-dimensie-ontwikkeling` is in twee gesplitst en hing tot 20-8 achteraan hoofdstuk 8 |
| d-concept | 10 | 3 | bestuursversie, met één nieuwe sectie vooraan: "veenweideboer is een schaal, geen categorie" (19-8) |
| f-ondernemer | 11 | 3 | nog de bestuursversie |
| f-overheid | 12 | 3 | nog de bestuursversie |
| f3-bedrijfsleven | 13 | 3 | nog de bestuursversie, groeit naar een volwaardig hoofdstuk |
| g-perspectief | 14 | 3 | bestuursversie, met de routes omgebouwd naar drie (19-8) |
| h-risicos | 15 | 4 | nog de bestuursversie |
| slot | 16 | 4 | nog de bestuursversie, wordt herschreven |
| bijlage-driesporen | 17 | 5 | in aanbouw, **7 van de 9 blokken verhuisd** (vier erbij op 20-8 uit hoofdstuk 7). Nog buiten: `f-overheid` en het stikstofblok in `intro`. De interne nummering loopt nog niet gelijk met het skelet, dus de verhuisde blokken dragen ongenummerde tussenkoppen |

## Nog te maken

*Leeg: hoofdstuk 9 staat sinds 20-8 in de hoofdtabel.*

*Het begrippenhoofdstuk is 19-8 vervallen: de begrippen gaan naar bijlage 17 en de scenario-introductie naar hoofdstuk 6.*

> **20-8: de nummering is één opgeschoven vanaf 9.** Hoofdstuk 9 tot 16 zijn 10 tot 17 geworden om plaats te maken voor het vergelijkingshoofdstuk. Doorgevoerd in `content/`, het skelet, de redactiebrief en de richtlijnen. **Het besluitenlog van vóór 20-8 draagt de oude nummering** en is bewust niet herschreven: een logboek dat je achteraf bijstelt, is geen logboek meer.

## Buiten de visie

| id | Waarom |
|---|---|
| i-vic-rol | Verhuisd naar het programmavoorstel (redactiebrief §14: "blijft daar"). Staat niet in `volgorde.txt`. Een verwijzing naar "sectie I" in de visie is dus altijd fout |
| pv-opening, pv-programmalijnen | Horen bij het programmavoorstel, niet bij de visie |
