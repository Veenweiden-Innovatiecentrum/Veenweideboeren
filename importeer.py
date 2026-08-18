# -*- coding: utf-8 -*-
"""Haalt de gepubliceerde website terug naar content/.

De website is de versie die het bestuur gelezen heeft en daarmee de enige
geldige tekst. Dit script leest webapp/site/content-*.js en schrijft de
hoofdstukken terug naar content/*.md, partials/*.html en volgorde.txt.

Per blok geldt dezelfde regel als bij de oorspronkelijke splitsing: alleen
omzetten naar Markdown als het teruggerenderd exact dezelfde DOM oplevert.
Lukt dat niet, dan blijft het onaangeroerde HTML. Er gaat dus geen letter
verloren; hooguit blijft een blok wat minder mooi leesbaar.

Gebruik:
    .venv/bin/python importeer.py            kijken wat er zou gebeuren
    .venv/bin/python importeer.py --schrijf  daadwerkelijk overschrijven
"""
import json, os, re, sys
import lib_convert as C

BRONNEN = {
    'visie': ('webapp/site/content-visie.js', 'volgorde.txt'),
    'programma': ('webapp/site/content-programma.js', 'volgorde-programmavoorstel.txt'),
    'toolbox': ('webapp/site/content-toolbox.js', 'volgorde-toolbox.txt'),
}


def lees_secties(pad):
    t = open(pad, encoding='utf-8').read()
    return json.loads(t[t.find('['):t.rfind(']') + 1])


def naar_markdown(sid, inner):
    """Eén hoofdstuk omzetten. Geeft (markdown, partials, telling) terug."""
    regels, partials = [], {}
    telling = {'md': 0, 'raw': 0, 'svg': 0}
    hangend_commentaar, svg_n = None, 0
    for soort, bron in C.top_level_chunks(inner):
        if soort == 'comment':
            hangend_commentaar = bron
            regels.append(bron)
            continue
        if soort == 'text':
            regels.append(bron.strip())
            telling['raw'] += 1
            continue
        if '<svg' in bron:
            svg_n += 1
            slug = None
            if hangend_commentaar:
                s = re.sub(r'[^a-z0-9]+', '-', hangend_commentaar.lower()).strip('-')
                s = re.sub(r'^-*|-*$', '', s.replace('svg', '').strip('-'))
                slug = s[:30].strip('-') or None
            naam = f"{sid}-{slug or 'visual-' + str(svg_n)}"
            partials[naam] = bron
            regels.append('{{partial:' + naam + '}}')
            telling['svg'] += 1
            hangend_commentaar = None
            continue
        hangend_commentaar = None
        md = C.verified_md(bron)
        if md is not None:
            regels.append(md)
            telling['md'] += 1
        else:
            regels.append(bron)
            telling['raw'] += 1
    return '\n\n'.join(regels) + '\n', partials, telling


def importeer(uiting, schrijf):
    bron, volgordebestand = BRONNEN[uiting]
    if not os.path.exists(bron):
        print(f'{bron} bestaat niet — overgeslagen.')
        return
    secties = lees_secties(bron)
    print(f'\n=== {uiting}: {len(secties)} hoofdstukken uit {bron} ===')
    print(f'{"hoofdstuk":<20}{"blokken":>9}{"waarvan MD":>12}{"raw":>6}{"svg":>6}  verandert?')
    print('-' * 68)
    resultaat, volgorde = {}, []
    for s in secties:
        sid = s['id']
        volgorde.append(sid)
        md, partials, t = naar_markdown(sid, s['html'])
        bestaand = ''
        pad = f'content/{sid}.md'
        if os.path.exists(pad):
            bestaand = open(pad, encoding='utf-8').read()
        staat = 'nieuw' if not bestaand else ('gelijk' if bestaand == md else 'WIJZIGT')
        totaal = t['md'] + t['raw'] + t['svg']
        print(f'{sid:<20}{totaal:>9}{t["md"]:>12}{t["raw"]:>6}{t["svg"]:>6}  {staat}')
        resultaat[sid] = (md, partials)
    print('-' * 68)

    verdwijnt = [f[:-3] for f in sorted(os.listdir('content'))
                 if f.endswith('.md') and f[:-3] not in volgorde]
    if verdwijnt:
        print(f'\nStaat niet in de website: {", ".join(verdwijnt)}')
        print('Die bestanden laat ik staan; ze horen niet bij deze uiting.')

    if not schrijf:
        print(f'\nNiets geschreven. Doorvoeren: .venv/bin/python importeer.py --schrijf')
        return

    for sid, (md, partials) in resultaat.items():
        open(f'content/{sid}.md', 'w', encoding='utf-8').write(md)
        for naam, inhoud in partials.items():
            open(f'partials/{naam}.html', 'w', encoding='utf-8').write(inhoud)
    open(volgordebestand, 'w', encoding='utf-8').write('\n'.join(volgorde) + '\n')
    print(f'\nGeschreven: {len(resultaat)} bestanden in content/ en {volgordebestand}')


if __name__ == '__main__':
    schrijf = '--schrijf' in sys.argv
    doelen = [a for a in sys.argv[1:] if not a.startswith('--')] or ['visie']
    for uiting in doelen:
        if uiting not in BRONNEN:
            sys.exit(f'FOUT: onbekende uiting "{uiting}" ({", ".join(BRONNEN)})')
        importeer(uiting, schrijf)
