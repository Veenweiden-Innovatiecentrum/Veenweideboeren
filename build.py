# -*- coding: utf-8 -*-
"""Build: assembleert dist/<uiting> uit content/ + partials/ + templates/.
Gebruik: python3 build.py document"""
import os, sys, re, json, shutil, datetime, urllib.parse
import lib_render as R


def build_document():
    order = [l.strip() for l in open('volgorde.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    parts = []
    for sid in order:
        md_path = f'content/{sid}.md'
        pt_path = f'partials/{sid}.html'
        if os.path.exists(md_path):
            body = R.render_md(open(md_path, encoding='utf-8').read())
        elif os.path.exists(pt_path):
            body = open(pt_path, encoding='utf-8').read()
        else:
            sys.exit(f'FOUT: geen bron voor sectie "{sid}" (content/ noch partials/)')
        parts.append(f'<section id="{sid}">\n{body}\n</section>')
    template = open('templates/document/template.html', encoding='utf-8').read()
    out = template.replace('{{SECTIONS}}', '\n\n'.join(parts))
    os.makedirs('dist', exist_ok=True)
    dest = "dist/VIC's Veenweideboeren visie.html"
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'Gebouwd: {dest} ({len(out)//1000}k tekens)')


def build_programmavoorstel():
    order = [l.strip() for l in open('volgorde-programmavoorstel.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    parts = []
    for sid in order:
        md_path = f'content/{sid}.md'
        pt_path = f'partials/{sid}.html'
        if os.path.exists(md_path):
            body = R.render_md(open(md_path, encoding='utf-8').read())
        elif os.path.exists(pt_path):
            body = open(pt_path, encoding='utf-8').read()
        else:
            sys.exit(f'FOUT: geen bron voor sectie "{sid}"')
        parts.append(f'<section id="{sid}">\n{body}\n</section>')
    template = open('templates/programmavoorstel/template.html', encoding='utf-8').read()
    out = template.replace('{{SECTIONS}}', '\n\n'.join(parts))
    os.makedirs('dist', exist_ok=True)
    dest = "dist/VIC's Veenweideboeren programmavoorstel.html"
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'Gebouwd: {dest} ({len(out)//1000}k tekens)')


def build_toolbox():
    order = [l.strip() for l in open('volgorde-toolbox.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    parts = []
    for sid in order:
        md_path = f'content/{sid}.md'
        pt_path = f'partials/{sid}.html'
        if os.path.exists(md_path):
            body = R.render_md(open(md_path, encoding='utf-8').read())
        elif os.path.exists(pt_path):
            body = open(pt_path, encoding='utf-8').read()
        else:
            sys.exit(f'FOUT: geen bron voor sectie "{sid}"')
        parts.append(f'<section id="{sid}">\n{body}\n</section>')
    template = open('templates/toolbox/template.html', encoding='utf-8').read()
    out = template.replace('{{SECTIONS}}', '\n\n'.join(parts))
    os.makedirs('dist', exist_ok=True)
    dest = "dist/VIC's Veenweideboeren toolbox.html"
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'Gebouwd: {dest} ({len(out)//1000}k tekens)')


def sectie_html(sid):
    """De opgemaakte HTML van één sectie, uit content/ of partials/."""
    md_path = f'content/{sid}.md'
    pt_path = f'partials/{sid}.html'
    if os.path.exists(md_path):
        return R.render_md(open(md_path, encoding='utf-8').read())
    if os.path.exists(pt_path):
        return open(pt_path, encoding='utf-8').read()
    sys.exit(f'FOUT: geen bron voor sectie "{sid}" (content/ noch partials/)')


def ontleed_sectie(sid):
    """Zet één sectie om naar wat de website ervan verwacht:
    een naam, een letter, een titel, een openingszin en de opgemaakte tekst.
    Letter en titel komen uit de eerste kop, de openingszin uit de eerste alinea."""
    html = '\n' + sectie_html(sid) + '\n'
    letter, titel = None, ''
    kop = re.search(r'<h2>(.*?)</h2>', html, re.S)
    if kop:
        tekst = re.sub(r'<[^>]+>', '', kop.group(1)).strip()
        deel = re.split(r'\s+—\s+', tekst, maxsplit=1)
        if len(deel) == 2 and len(deel[0]) <= 3:
            letter, titel = deel[0], deel[1]
        else:
            titel = tekst
    intro = ''
    for m in re.finditer(r'<p>(.*?)</p>', html, re.S):
        kaal = re.sub(r'<[^>]+>', '', m.group(1))
        kaal = ' '.join(kaal.split())
        if len(kaal.split()) >= 8:
            intro = kaal
            break
    return {'id': sid, 'letter': letter, 'titel': titel, 'intro': intro, 'html': html}


def vergelijk_site(uiting, secties, dest):
    """Zegt per hoofdstuk of de zichtbare tekst van de repo afwijkt van wat er
    nu in de website staat. Zonder --schrijf gebeurt er verder niets."""
    if not os.path.exists(dest):
        print(f'{dest} bestaat nog niet — alles zou nieuw zijn.')
        return
    t = open(dest, encoding='utf-8').read()
    huidig = {d['id']: d for d in json.loads(t[t.find('['):t.rfind(']') + 1])}

    def zichtbaar(h):
        h = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', h, flags=re.S)
        return ' '.join(re.sub(r'<[^>]+>', ' ', h).split())

    afwijkend = []
    print(f'\n{"hoofdstuk":<20}{"zichtbare tekst":<20}website  repo')
    print('-' * 60)
    for s in secties:
        oud = huidig.get(s['id'])
        if oud is None:
            print(f'{s["id"]:<20}{"NIEUW":<20}{"—":>7}{len(zichtbaar(s["html"]).split()):>6}')
            afwijkend.append(s['id'])
            continue
        a, b = zichtbaar(s['html']), zichtbaar(oud['html'])
        if a == b:
            print(f'{s["id"]:<20}{"gelijk":<20}{len(b.split()):>7}{len(a.split()):>6}')
        else:
            print(f'{s["id"]:<20}{"WIJKT AF":<20}{len(b.split()):>7}{len(a.split()):>6}')
            afwijkend.append(s['id'])
    print('-' * 60)
    if afwijkend:
        print(f'\n{len(afwijkend)} hoofdstuk(ken) wijken af: {", ".join(afwijkend)}')
        print('De website bevat tekst die niet uit content/ komt. Schrijven zou')
        print('die overschrijven. Kijk eerst wat er verloren gaat.')
    print(f'\nNiets geschreven. Wil je dat wel: python3 build.py site {uiting} --schrijf')


def build_site(uiting='visie', schrijf=False):
    """Zet de hoofdstukken om naar het bestand dat de website inleest.
    Dit is de ontbrekende schakel tussen content/ en webapp/.
    Zonder schrijf=True wordt alleen vergeleken — nooit stilzwijgend overschrijven."""
    bronnen = {
        'visie': ('volgorde.txt', 'VISIE_CONTENT', 'content-visie.js'),
        'programma': ('volgorde-programmavoorstel.txt', 'PROGRAMMA_CONTENT',
                      'content-programma.js'),
        'toolbox': ('volgorde-toolbox.txt', 'TOOLBOX_CONTENT', 'content-toolbox.js'),
    }
    if uiting not in bronnen:
        sys.exit(f'FOUT: onbekende uiting "{uiting}" (visie, programma, toolbox)')
    volgorde, variabele, bestand = bronnen[uiting]
    order = [l.strip() for l in open(volgorde, encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    secties = [ontleed_sectie(sid) for sid in order]
    dest = f'webapp/site/{bestand}'
    if not os.path.isdir('webapp/site'):
        sys.exit('FOUT: webapp/site ontbreekt — staat de website wel in de repo?')
    if not schrijf:
        vergelijk_site(uiting, secties, dest)
        return
    open(dest, 'w', encoding='utf-8').write(
        f'window.{variabele} = ' +
        json.dumps(secties, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(f'Gebouwd: {dest} ({len(secties)} secties, {os.path.getsize(dest)//1024}k)')


def template_hoofd():
    """De <head> van het document: lettertypen en de volledige huisstijl-CSS.
    Hergebruiken in plaats van namaken, zodat alles wat wij bouwen er
    hetzelfde uitziet als de visie zelf."""
    t = open('templates/document/template.html', encoding='utf-8').read()
    return t.split('</head>')[0] + '</head>'


def vic_logo():
    """Het VIC-logo zoals het in de zijbalk van het document staat."""
    t = open('templates/document/template.html', encoding='utf-8').read()
    m = re.search(r'<div class="vic-logo">.*?</div>', t, re.S)
    return m.group(0) if m else ''



def build_hoofdstuk(sid):
    """Eén hoofdstuk als losse HTML ter beoordeling — zelfde opmaak als het
    document, zonder navigatie. Leesversie, geen publicatie."""
    md_path = f'content/{sid}.md'
    pt_path = f'partials/{sid}.html'
    if os.path.exists(md_path):
        body = R.render_md(open(md_path, encoding='utf-8').read())
    elif os.path.exists(pt_path):
        body = open(pt_path, encoding='utf-8').read()
    else:
        sys.exit(f'FOUT: geen bron voor sectie "{sid}" (content/ noch partials/)')
    kop = (
        '<div style="border-bottom:1px solid rgba(0,0,0,.08);background:var(--bg2)">'
        '<div style="max-width:820px;margin:0 auto;padding:1.25rem 3rem;'
        'display:flex;align-items:center;gap:1.25rem">'
        f'<div style="width:130px;flex:none">{vic_logo()}</div>'
        '<div><div style="font-family:var(--font-display);font-size:16px;'
        'font-weight:700">Veenweideboeren</div>'
        '<div style="font-size:12px;color:var(--text2)">Los hoofdstuk ter '
        'beoordeling — geen publicatie</div></div></div></div>')
    out = (f'{template_hoofd()}\n<body>\n{kop}\n<main>\n<section id="{sid}">\n{body}\n'
           f'</section>\n</main>\n</body>\n</html>\n')
    os.makedirs('dist/hoofdstukken', exist_ok=True)
    dest = f'dist/hoofdstukken/{sid}.html'
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'Gebouwd: {dest} ({len(out)//1000}k tekens)')


def build_tekst():
    """Alle content-MD samenvoegen tot één leesbestand (alleen ter inzage —
    bewerken gebeurt in de losse bestanden in content/)."""
    order = [l.strip() for l in open('volgorde.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    parts = ['<!-- GEGENEREERD OVERZICHT — niet bewerken; bron: content/*.md -->']
    for sid in order:
        md_path = f'content/{sid}.md'
        if not os.path.exists(md_path):
            parts.append(f'*[sectie `{sid}`: partial, geen tekstbestand]*')
            continue
        parts.append(f'<!-- ======== bestand: content/{sid}.md ======== -->')
        parts.append(open(md_path, encoding='utf-8').read().rstrip('\n'))
    os.makedirs('dist', exist_ok=True)
    dest = 'dist/alles.md'
    open(dest, 'w', encoding='utf-8').write('\n\n---\n\n'.join(parts) + '\n')
    print(f'Gebouwd: {dest}')

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'document'
    if target == 'document':
        build_document()
    elif target == 'toolbox':
        build_toolbox()
    elif target == 'programmavoorstel':
        build_programmavoorstel()
    elif target == 'tekst':
        build_tekst()
    elif target == 'site':
        losse = [a for a in sys.argv[2:] if not a.startswith('--')]
        build_site(losse[0] if losse else 'visie', '--schrijf' in sys.argv)
    elif target == 'hoofdstuk':
        if len(sys.argv) < 3:
            sys.exit('FOUT: geef het hoofdstuk mee, bv. python3 build.py hoofdstuk c-omslag')
        build_hoofdstuk(sys.argv[2])
    else:
        sys.exit(f'Onbekende uiting: {target} (beschikbaar: document, toolbox, '
                 'programmavoorstel, tekst, hoofdstuk <id>)')
