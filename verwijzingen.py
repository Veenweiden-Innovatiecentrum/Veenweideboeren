# -*- coding: utf-8 -*-
"""Controleert elke kruisverwijzing in de tekst tegen het hoofdstukregister.

Gebruik: python3 verwijzingen.py

Waarom dit bestaat: een verwijzing als "de analyse van hoofdstuk 4" of "staat in
bijlage 17" is waar of niet waar, maar niets merkt het als ze onwaar wordt. De
hoofdstukken worden genummerd terwijl ze herzien worden, dus een verwijzing kan
kloppen op de eindstructuur en toch nog niet op te volgen zijn voor de lezer.
Dat onderscheid maakt dit script:

  KLOPT       de verwijzing wijst naar een hoofdstuk dat dat nummer nu draagt
  NOG NIET    het hoofdstuk krijgt dat nummer, maar draagt het nog niet
  FOUT        er is geen hoofdstuk met dat nummer, of het staat niet in de visie

Bron van de nummers: richtlijnen/hoofdstukregister.md. Bron van wat een hoofdstuk
nu draagt: de eerste ##-kop van het bestand zelf.
"""
import os
import re
import sys

REGISTER = 'richtlijnen/hoofdstukregister.md'
VOLGORDE = 'volgorde.txt'
CONTENT = 'content'

# Een verwijzing naar een subkop moet aangekondigd worden ("zie 1.3", "in 1.3").
# Zonder die eis wordt elk getal met een punt een kandidaat, en dan slaat de
# controle aan op hectares (200.000) en op CSS (line-height:1.65).
CUE = re.compile(r'\b(in|zie|volgens|paragraaf|onderdeel|punt)\s+$', re.I)
# Statuten en Kamerstukken zijn vindplaatsen buiten dit document.
GEEN_VERWIJZING = re.compile(r'(artikel|nr\.|§|versie|kamerstuk)\s*$', re.I)
# Getal met een eenheid erachter is een hoeveelheid, geen subkop.
EENHEID = re.compile(r'^\s*(ha|hectare|mln|miljard|%|cm|km|jaar)\b', re.I)


def zichtbaar(tekst):
    """Alleen de tekst die de lezer ziet. Rauwe HTML en CSS eruit, anders slaat
    de controle aan op stijlwaarden in plaats van op verwijzingen."""
    tekst = re.sub(r'<!--.*?-->', ' ', tekst, flags=re.S)
    tekst = re.sub(r'<(script|style)\b.*?</\1>', ' ', tekst, flags=re.S)
    tekst = re.sub(r'<[^>]+>', ' ', tekst)
    return tekst


def lees_register():
    """id -> lijst van nummers die het hoofdstuk moet gaan dragen."""
    if not os.path.exists(REGISTER):
        sys.exit(f'FOUT: {REGISTER} ontbreekt. Zonder register valt niets te toetsen.')
    doel, buiten = {}, set()
    sectie = 'hoofdstukken'
    for regel in open(REGISTER, encoding='utf-8'):
        if regel.startswith('## '):
            kop = regel[3:].strip().lower()
            sectie = 'buiten' if 'buiten' in kop else 'te maken' if 'maken' in kop else 'hoofdstukken'
            continue
        if not regel.startswith('|'):
            continue
        kolom = [k.strip() for k in regel.strip().strip('|').split('|')]
        if len(kolom) < 2 or kolom[0] in ('id', 'nummer', '---') or set(kolom[0]) <= {'-'}:
            continue
        if sectie == 'buiten':
            buiten.add(kolom[0])
            continue
        if sectie == 'te maken':
            # kolom 0 is hier het nummer, het hoofdstuk bestaat nog niet
            for n in re.findall(r'\d+', kolom[0]):
                doel.setdefault('(nog te maken)', []).append(n)
            continue
        nummers = re.findall(r'\d+', kolom[1]) if len(kolom) > 1 else []
        doel[kolom[0]] = nummers
    return doel, buiten


def lees_gedragen():
    """id -> wat de ##-kop nu als nummer of letter draagt, plus de subkoppen."""
    order = [l.strip() for l in open(VOLGORDE, encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    gedragen, subkoppen = {}, set()
    for sid in order:
        pad = f'{CONTENT}/{sid}.md'
        if not os.path.exists(pad):
            gedragen[sid] = None
            continue
        tekst = open(pad, encoding='utf-8').read()
        kop = re.search(r'^##\s+(.*)$', tekst, re.M)
        merk = None
        if kop:
            deel = re.split(r'\s+—\s+', kop.group(1).strip(), maxsplit=1)
            if len(deel) == 2 and len(deel[0]) <= 3:
                merk = deel[0]
        gedragen[sid] = merk
        for sub in re.findall(r'^###\s+(\d+\.\d+)', tekst, re.M):
            subkoppen.add(sub)
    return order, gedragen, subkoppen


def vind_verwijzingen(tekst):
    """(soort, doel, fragment) per verwijzing in één bestand."""
    uit = []
    # koppen zijn definities, geen verwijzingen
    schoon = zichtbaar(re.sub(r'^#{2,4}\s+.*$', '', tekst, flags=re.M))
    for m in re.finditer(r'\b(hoofdstuk|hoofdstukken|bijlage|sectie)\s+'
                         r'([0-9]+(?:\s*(?:,|en)\s*[0-9]+)*|[A-H]|F[123])\b', schoon, re.I):
        soort = 'sectie' if m.group(1).lower() == 'sectie' else m.group(1).lower()
        for d in re.findall(r'[0-9]+|[A-H]|F[123]', m.group(2)):
            uit.append((soort, d, m.group(0)))
    for m in re.finditer(r'\b(\d{1,2}\.\d{1,2})\b', schoon):
        voor = schoon[max(0, m.start() - 14):m.start()]
        if GEEN_VERWIJZING.search(voor) or not CUE.search(voor):
            continue
        if EENHEID.match(schoon[m.end():m.end() + 10]):
            continue
        uit.append(('subkop', m.group(1), schoon[max(0, m.start() - 40):m.end() + 10]))
    return uit


# ---------------------------------------------------------------------------
# Tweede controle: terugverwijzingen zonder antecedent.
#
# Op 18 augustus vond Tim vier keer dezelfde fout: "deze fase", "hij niet
# wacht", "de redenering", "de vraag". Alle vier grammaticaal correct en
# feitelijk waar, en alle vier onvindbaar voor wie de structuur niet al in zijn
# hoofd heeft. Geen enkele bestaande check ziet ze, want ze zoeken op verboden
# termen en op ontbrekende bronnen.
#
# Dit is een kandidatenlijst, geen foutenlijst: het zijn abstracte woorden die
# alleen betekenis hebben als het document ze eerder heeft ingevoerd. Staat het
# woord niet eerder in hetzelfde hoofdstuk, dan is dat een signaal om te kijken.
STRUCTUURWOORDEN = [
    'fase', 'ronde', 'redenering', 'gedachte', 'vraag', 'omkering', 'kern',
    'claim', 'typologie', 'stapeling', 'logica', 'mechanisme', 'propositie',
    'afbakening', 'splitsing', 'verschuiving', 'beweging', 'leesbril',
]
LIDWOORD = r'\b(?:de|het|die|dat|deze|dit|dié)\s+$'
# "in de kern", "naar de kern": bijwoordelijk, geen verwijzing.
BIJWOORDELIJK = r'\b(?:in|naar|tot|met|op|uit)\s+(?:de|het)\s+$'
# Wordt het woord in dezelfde adem gedefinieerd, dan hoeft er geen antecedent
# te zijn: "de stapeling die het model onhoudbaar maakt", "de vraag is niet of".
DEFINIEERT_ZICH = (r'^\s*(?::'                       # let op: geen \b na de dubbele punt,
                   r'|(?:is|was|luidt|die|dat'       # daar zit geen woordgrens
                   r'|waarmee|waarin|waarop|waarvan)\b)')


def vind_losse_verwijzingen(tekst):
    """(woord, fragment) voor elk structuurwoord dat met een bepaald lidwoord
    wordt aangewezen zonder dat het eerder in dit hoofdstuk voorkwam en zonder
    dat het ter plekke wordt uitgelegd. Kandidaten, geen fouten."""
    kaal = re.sub(r'\[\[.*?\]\]', ' ', zichtbaar(tekst), flags=re.S)
    uit = []
    for woord in STRUCTUURWOORDEN:
        stam = woord[:6]  # "stapeling" en "stapelen" delen dezelfde stam
        for m in re.finditer(r'\b' + woord + r'\w{0,3}\b', kaal, re.I):
            voor = kaal[max(0, m.start() - 16):m.start()]
            na = kaal[m.end():m.end() + 24]
            if re.search(r'\b' + stam + r'\w*\b', kaal[:m.start()], re.I):
                break  # eerder ingevoerd, verwijzen mag
            if not re.search(LIDWOORD, voor, re.I):
                break  # geen bepaald lidwoord, dus geen terugverwijzing
            if re.search(BIJWOORDELIJK, voor, re.I) or re.search(DEFINIEERT_ZICH, na, re.I):
                break
            # "Diensten als product naast voedsel: die redenering geldt dus" —
            # een dubbele punt vlak ervoor noemt het ding bij naam.
            if ':' in kaal[max(0, m.start() - 24):m.start()]:
                break
            uit.append((woord, ' '.join(kaal[max(0, m.start() - 60):m.end() + 45].split())))
            break
    return uit


def main():
    doel, buiten = lees_register()
    order, gedragen, subkoppen = lees_gedragen()

    # nummer -> id, uit het register; en wat nu gedragen wordt
    van_nummer = {n: sid for sid, ns in doel.items() for n in ns}
    nu_gedragen = {v: k for k, v in gedragen.items() if v}

    fout, nogniet, klopt = [], [], 0
    for sid in order:
        pad = f'{CONTENT}/{sid}.md'
        if not os.path.exists(pad):
            continue
        for soort, d, frag in vind_verwijzingen(open(pad, encoding='utf-8').read()):
            frag = ' '.join(frag.split())
            if soort == 'subkop':
                if d in subkoppen:
                    klopt += 1
                elif d.split('.')[0] in van_nummer:
                    nogniet.append((sid, frag, f'hoofdstuk {d.split(".")[0]} bestaat nog niet, '
                                               f'dus subkop {d} ook niet'))
                else:
                    fout.append((sid, frag, f'geen subkop {d} in de tekst'))
                continue
            if d in buiten or (soort == 'sectie' and d == 'I'):
                fout.append((sid, frag, 'wijst buiten de visie'))
                continue
            eigenaar = van_nummer.get(d) or nu_gedragen.get(d.upper())
            if eigenaar is None:
                fout.append((sid, frag, f'geen hoofdstuk met {soort} {d} in het register'))
            elif eigenaar == '(nog te maken)':
                nogniet.append((sid, frag, f'hoofdstuk {d} is nog niet geschreven'))
            elif gedragen.get(eigenaar) == d or (gedragen.get(eigenaar) or '').upper() == d.upper():
                klopt += 1
            else:
                nogniet.append((sid, frag,
                                f'{eigenaar} wordt hoofdstuk {d}, maar draagt nu '
                                f'"{gedragen.get(eigenaar) or "geen nummer"}"'))

    print(f'\n{klopt} verwijzing(en) kloppen.\n')
    if nogniet:
        print(f'NOG NIET OP TE VOLGEN ({len(nogniet)}) — klopt op de eindstructuur, '
              f'maar de lezer kan er nu niet heen:')
        for sid, frag, waarom in nogniet:
            print(f'  {sid:<20} {frag[:52]:<54} {waarom}')
        print()
    if fout:
        print(f'FOUT ({len(fout)}):')
        for sid, frag, waarom in fout:
            print(f'  {sid:<20} {frag[:52]:<54} {waarom}')
        print()
    if not nogniet and not fout:
        print('Alle verwijzingen kloppen en zijn op te volgen.\n')

    los = []
    for sid in order:
        pad = f'{CONTENT}/{sid}.md'
        if not os.path.exists(pad):
            continue
        for woord, frag in vind_losse_verwijzingen(open(pad, encoding='utf-8').read()):
            los.append((sid, woord, frag))
    print('-' * 74)
    if los:
        print(f'TERUGVERWIJZING ZONDER ANTECEDENT — {len(los)} kandidaat(en).')
        print('Een bepaald lidwoord wijst een abstract woord aan dat eerder in het')
        print('hoofdstuk niet voorkomt. Kijk of het terecht is; zo ja, noem het bij naam.\n')
        for sid, woord, frag in los:
            print(f'  {sid:<20} "{woord}"')
            print(f'  {"":<20} …{frag}…')
    else:
        print('Geen losse terugverwijzingen gevonden.')
    print()
    sys.exit(1 if fout else 0)


if __name__ == '__main__':
    main()
