# -*- coding: utf-8 -*-
"""Stijlcheck: meet schrijfsporen in content/*.md tegen twee nulmetingen.

De hoofdstukken in content/ zijn zelf met AI geschreven. Ze meten tegen
elkaar zegt dus alleen of nieuwe tekst op de vorige AI lijkt. Daarom is de
eerste nulmeting mensentekst: de letterlijke citaten van Eugène, Anna, Erik,
Roelof, Niel, Simon en Henk uit feedback/ — Nederlands, zelfde onderwerp,
zelfde register, aantoonbaar door mensen getypt.

De tweede nulmeting is het document zelf. Nuttig om te zien of een herzien
hoofdstuk uit de toon valt, maar niet om te beoordelen of het menselijk klinkt.

Een uitslag is een signaal, geen oordeel. Niets wordt geblokkeerd.

Gebruik:
    python3 stijlcheck.py                 alle hoofdstukken
    python3 stijlcheck.py scope.md        één bestand, met de vindplaatsen
    python3 stijlcheck.py --nulmeting     de mensen-nulmeting opnieuw oogsten
"""
import os, re, sys, glob, statistics

CONTENT = 'content'
MENSCORPUS = 'richtlijnen/nulmeting-mens.txt'
BRONNEN = sorted(glob.glob('feedback/*.md')) + ['richtlijnen/commentaar-clusters.md']

SIGNAALWOORDEN = [
    'cruciaal', 'essentieel', 'fundamenteel', 'wezenlijk', 'onmiskenbaar',
    'robuust', 'naadloos', 'baanbrekend', 'toonaangevend', 'veelbelovend',
    'waardevol', 'impactvol', 'krachtig', 'concreet handvat',
    'verankeren', 'ontsluiten', 'faciliteren', 'borgen', 'versterken',
    'in het licht van', 'in een tijd waarin', 'in een wereld waarin',
    'het is belangrijk om', 'het is goed om', 'de sleutel tot',
    'bovendien', 'daarnaast', 'kortom', 'tot slot', 'al met al',
    'met andere woorden', 'sterker nog', 'niet in de laatste plaats',
    'een belangrijke stap', 'het speelveld',
]

NIET_MAAR = re.compile(r'\b(niet|geen)\b[^.!?;]{1,80}?\bmaar\b', re.I)
DRIESLAG = re.compile(r'\b\w+, \w+ en \w+\b')
EM_DASH = re.compile(r'—')

# Regels uit de feedbackbestanden die niet van de commentator zijn maar van de
# samenvatter: statusmarkeringen, ticketcodes, tabelrijen, kopjes.
REDACTIE = re.compile(r'[✅⏸◐→§|]|\b(ET|E|B)-?N?\d+\b|^\*\*|^#')


def oogst_mensentekst():
    """Haalt de letterlijke citaten uit feedback/ en zet ze in één bestand."""
    citaten = []
    for pad in BRONNEN:
        if not os.path.exists(pad):
            continue
        tekst = open(pad, encoding='utf-8').read()
        for m in re.finditer(r'^> ?(.*)$', tekst, re.M):
            citaten.append(m.group(1).strip())
        for m in re.finditer(r'"([^"]{40,})"', tekst):
            citaten.append(m.group(1).strip())
    schoon = []
    for c in dict.fromkeys(citaten):
        c = re.sub(r'^[-*]\s+', '', c)
        if len(c.split()) < 8 or REDACTIE.search(c):
            continue
        schoon.append(c)
    os.makedirs(os.path.dirname(MENSCORPUS), exist_ok=True)
    open(MENSCORPUS, 'w', encoding='utf-8').write(
        '# Nulmeting mensentekst — letterlijke citaten uit feedback/.\n'
        '# Gegenereerd door stijlcheck.py --nulmeting. Niet met de hand bewerken.\n\n'
        + '\n'.join(schoon) + '\n')
    return len(schoon), sum(len(c.split()) for c in schoon)


def platte_tekst_uit(ruw):
    ruw = re.sub(r'<!--.*?-->', ' ', ruw, flags=re.S)
    ruw = re.sub(r'style="[^"]*"', ' ', ruw)
    ruw = re.sub(r'<[^>]+>', ' ', ruw)
    ruw = re.sub(r'\{\{fiche:.*?\}\}|\{\{bron:.*?\}\}|\{\{partial:.*?\}\}', ' ', ruw)
    ruw = re.sub(r'\[\[.*?\]\]', ' ', ruw)
    ruw = re.sub(r'^#{1,4} .*$', ' ', ruw, flags=re.M)
    ruw = ruw.replace('&amp;', 'en').replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', ruw).strip()


def platte_tekst(pad):
    return platte_tekst_uit(open(pad, encoding='utf-8').read())


def zinnen(tekst):
    delen = re.split(r'(?<=[.!?])\s+(?=[A-Z"„])', tekst)
    return [z for z in delen if len(z.split()) >= 3]


def meet_tekst(naam, tekst):
    woorden = tekst.split()
    n = len(woorden)
    if n < 120:
        return None
    lengtes = [len(z.split()) for z in zinnen(tekst)]
    per1000 = lambda k: round(k * 1000 / n, 1)
    signalen = sum(len(re.findall(r'\b' + re.escape(w), tekst, re.I))
                   for w in SIGNAALWOORDEN)
    return {
        'bestand': naam,
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


def toon_tabel(metingen, mens, doc):
    kop = f'{"bestand":<22}{"woorden":>8}' + ''.join(f'{m:>14}' for m in MAATSTAVEN)
    print(kop)
    print('-' * len(kop))
    for m in metingen:
        rij = f'{m["bestand"]:<22}{m["woorden"]:>8}'
        for maat in MAATSTAVEN:
            waarde, basis = m[maat], mens[maat]
            merk = ' '
            if basis > 0:
                v = waarde / basis
                merk = '*' if (v >= 1.75 or v <= 0.5) else ' '
            rij += f'{waarde:>13}{merk}'
        print(rij)
    print('-' * len(kop))
    for label, meting in (('NULMETING mensentekst', mens),
                          ('nulmeting document (AI)', doc)):
        rij = f'{label:<22}{meting["woorden"]:>8}'
        for maat in MAATSTAVEN:
            rij += f'{meting[maat]:>14}'
        print(rij)
    print('\nAlles per 1000 woorden, behalve zinslengte en spreiding (in woorden).')
    print('Een * wijkt meer dan 1,75x af van de MENSENTEKST, of minder dan 0,5x.')
    print('De tweede nulmeting is het document zelf — ook AI-geschreven, dus')
    print('alleen bruikbaar om te zien of een hoofdstuk uit de toon valt.')


def toon_vindplaatsen(pad):
    print(f'\nVindplaatsen in {os.path.basename(pad)}\n')
    for nr, regel in enumerate(open(pad, encoding='utf-8'), 1):
        schoon = re.sub(r'style="[^"]*"', ' ', regel)
        schoon = re.sub(r'<[^>]+>', ' ', schoon)
        for naam, patroon in (('niet-maar', NIET_MAAR), ('drieslag', DRIESLAG)):
            for tref in patroon.finditer(schoon):
                print(f'  r{nr:<4} {naam:<12} {" ".join(tref.group(0).split())[:74]}')
        for w in SIGNAALWOORDEN:
            if re.search(r'\b' + re.escape(w), schoon, re.I):
                print(f'  r{nr:<4} {"signaalwoord":<12} {w}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--nulmeting' in args or not os.path.exists(MENSCORPUS):
        aantal, woorden = oogst_mensentekst()
        print(f'Nulmeting geoogst: {aantal} citaten, {woorden} woorden → {MENSCORPUS}\n')
        if '--nulmeting' in args:
            sys.exit(0)

    doelen = [a for a in args if not a.startswith('--')]
    alle = sorted(glob.glob(f'{CONTENT}/*.md'))
    if not alle:
        sys.exit('FOUT: geen bestanden in content/')

    mens = meet_tekst('mensentekst', platte_tekst_uit(
        '\n'.join(r for r in open(MENSCORPUS, encoding='utf-8')
                  if not r.startswith('#'))))
    doc = meet_tekst('document', ' '.join(platte_tekst(p) for p in alle))
    if mens is None:
        sys.exit(f'FOUT: te weinig mensentekst in {MENSCORPUS}')

    if doelen:
        metingen = [m for m in (meet_tekst(d, platte_tekst(f'{CONTENT}/{d}'))
                                for d in doelen) if m]
    else:
        metingen = [m for m in (meet_tekst(os.path.basename(p), platte_tekst(p))
                                for p in alle) if m]
    toon_tabel(metingen, mens, doc)

    for d in doelen:
        toon_vindplaatsen(f'{CONTENT}/{d}')
