# -*- coding: utf-8 -*-
"""Stijlcheck: meet schrijfsporen in content/*.md tegen de bestaande tekst.

Niet: een lijst verboden woorden. De redactiebrief zit zelf vol em-dashes —
dat is de stem van dit document, geen fout. Wel: de hoofdstukken die er al
lagen vormen de nulmeting, en nieuwe of herziene tekst wordt daartegen
afgezet. Wat sterk afwijkt klinkt niet als de rest van het document.

Een uitslag is een signaal, geen oordeel. Niets wordt geblokkeerd.

Gebruik:
    python3 stijlcheck.py                 alle bestanden tegen de nulmeting
    python3 stijlcheck.py scope.md        één bestand, met de vindplaatsen
"""
import os, re, sys, glob, statistics

CONTENT = 'content'

# Woorden en wendingen die in Nederlandse AI-tekst opvallend vaak opduiken.
# Geen verbodslijst: sommige horen thuis in een beleidsstuk. Het gaat om
# de dichtheid ten opzichte van de rest van dit document.
SIGNAALWOORDEN = [
    'cruciaal', 'essentieel', 'fundamenteel', 'wezenlijk', 'onmiskenbaar',
    'robuust', 'naadloos', 'baanbrekend', 'toonaangevend', 'veelbelovend',
    'waardevol', 'impactvol', 'krachtig', 'helder', 'concreet handvat',
    'verankeren', 'ontsluiten', 'faciliteren', 'borgen', 'versterken',
    'in het licht van', 'in een tijd waarin', 'in een wereld waarin',
    'het is belangrijk om', 'het is goed om', 'de sleutel tot',
    'bovendien', 'daarnaast', 'kortom', 'tot slot', 'al met al',
    'met andere woorden', 'sterker nog', 'niet in de laatste plaats',
    'een belangrijke stap', 'de komende jaren zal', 'het speelveld',
]

NIET_MAAR = re.compile(r'\b(niet|geen)\b[^.!?;]{1,80}?\bmaar\b', re.I)
DRIESLAG = re.compile(r'\b\w+, \w+ en \w+\b')
EM_DASH = re.compile(r'—')


def platte_tekst(pad):
    """De leesbare tekst uit een content-bestand: HTML-blokken en markup eruit."""
    ruw = open(pad, encoding='utf-8').read()
    ruw = re.sub(r'<!--.*?-->', ' ', ruw, flags=re.S)
    ruw = re.sub(r'style="[^"]*"', ' ', ruw)
    ruw = re.sub(r'<[^>]+>', ' ', ruw)
    ruw = re.sub(r'\{\{fiche:.*?\}\}|\{\{bron:.*?\}\}|\{\{partial:.*?\}\}', ' ', ruw)
    ruw = re.sub(r'\[\[.*?\]\]', ' ', ruw)
    ruw = re.sub(r'^#{2,4} .*$', ' ', ruw, flags=re.M)
    ruw = ruw.replace('&amp;', 'en').replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', ruw).strip()


def zinnen(tekst):
    delen = re.split(r'(?<=[.!?])\s+(?=[A-Z"„])', tekst)
    return [z for z in delen if len(z.split()) >= 3]


def meet(pad):
    tekst = platte_tekst(pad)
    woorden = tekst.split()
    n = len(woorden)
    if n < 120:
        return None
    zs = zinnen(tekst)
    lengtes = [len(z.split()) for z in zs]
    per1000 = lambda k: round(k * 1000 / n, 1)
    signalen = sum(len(re.findall(r'\b' + re.escape(w), tekst, re.I))
                   for w in SIGNAALWOORDEN)
    return {
        'bestand': os.path.basename(pad),
        'woorden': n,
        'em-dash': per1000(len(EM_DASH.findall(tekst))),
        'niet-maar': per1000(len(NIET_MAAR.findall(tekst))),
        'drieslag': per1000(len(DRIESLAG.findall(tekst))),
        'signaalwoord': per1000(signalen),
        'zinslengte': round(statistics.mean(lengtes), 1) if lengtes else 0,
        'spreiding': round(statistics.pstdev(lengtes), 1) if len(lengtes) > 1 else 0,
    }


MAATSTAVEN = ['em-dash', 'niet-maar', 'drieslag', 'signaalwoord',
              'zinslengte', 'spreiding']


def toon_tabel(metingen, nulmeting):
    kop = f'{"bestand":<22}{"woorden":>8}' + ''.join(f'{m:>14}' for m in MAATSTAVEN)
    print(kop)
    print('-' * len(kop))
    for m in metingen:
        rij = f'{m["bestand"]:<22}{m["woorden"]:>8}'
        for maat in MAATSTAVEN:
            waarde = m[maat]
            basis = nulmeting[maat]
            merk = ' '
            if basis > 0:
                verhouding = waarde / basis
                if verhouding >= 1.75 or verhouding <= 0.5:
                    merk = '*'
            rij += f'{waarde:>13}{merk}'
        print(rij)
    print('-' * len(kop))
    rij = f'{"NULMETING (bestaand)":<22}{nulmeting["woorden"]:>8}'
    for maat in MAATSTAVEN:
        rij += f'{nulmeting[maat]:>14}'
    print(rij)
    print('\nAlles per 1000 woorden, behalve zinslengte en spreiding (in woorden).')
    print('Een * betekent: meer dan 1,75x of minder dan 0,5x de nulmeting.')
    print('Dat is een signaal om naar te kijken, geen fout.')


def toon_vindplaatsen(pad):
    print(f'\nVindplaatsen in {os.path.basename(pad)}\n')
    for nr, regel in enumerate(open(pad, encoding='utf-8'), 1):
        schoon = re.sub(r'style="[^"]*"', ' ', regel)
        schoon = re.sub(r'<[^>]+>', ' ', schoon)
        for naam, patroon in (('niet-maar', NIET_MAAR), ('drieslag', DRIESLAG)):
            for tref in patroon.finditer(schoon):
                fragment = ' '.join(tref.group(0).split())
                print(f'  r{nr:<4} {naam:<12} {fragment[:76]}')
        for w in SIGNAALWOORDEN:
            if re.search(r'\b' + re.escape(w), schoon, re.I):
                print(f'  r{nr:<4} {"signaalwoord":<12} {w}')


if __name__ == '__main__':
    doelen = sys.argv[1:]
    alle = sorted(glob.glob(f'{CONTENT}/*.md'))
    if not alle:
        sys.exit('FOUT: geen bestanden in content/')

    # De nulmeting is alles wat níet als doel is opgegeven: de bestaande tekst.
    basisbestanden = [p for p in alle if os.path.basename(p) not in doelen]
    basis_tekst = ' '.join(platte_tekst(p) for p in basisbestanden)
    tijdelijk = os.path.join(CONTENT, '.nulmeting')
    open(tijdelijk, 'w', encoding='utf-8').write(basis_tekst)
    nulmeting = meet(tijdelijk)
    os.remove(tijdelijk)
    if nulmeting is None:
        sys.exit('FOUT: te weinig bestaande tekst voor een nulmeting')

    if doelen:
        metingen = [m for m in (meet(f'{CONTENT}/{d}') for d in doelen) if m]
    else:
        metingen = [m for m in (meet(p) for p in alle) if m]
    toon_tabel(metingen, nulmeting)

    for d in doelen:
        toon_vindplaatsen(f'{CONTENT}/{d}')
