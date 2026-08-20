# -*- coding: utf-8 -*-
"""Build: assembleert dist/<uiting> uit content/ + partials/ + templates/.
Gebruik: python3 build.py document"""
import os, sys, re, json, shutil, datetime, urllib.parse
import lib_render as R


def deel_html(titel):
    """Deelkop tussen de secties van het document. Het deel komt uit
    richtlijnen/skelet.md, dus hier niets bijhouden."""
    nummer, _, naam = titel.replace('Deel ', '').partition(' — ')
    return (f'<p style="margin:3.5rem 0 -0.5rem;padding-top:1.25rem;'
            f'border-top:2px solid var(--accent2);font-family:var(--font-sans);'
            f'font-size:12px;text-transform:uppercase;letter-spacing:.12em;'
            f'color:var(--accent2);font-weight:700">Deel {nummer} '
            f'<span style="color:var(--text2);letter-spacing:.06em">· {naam}</span></p>')


def build_document():
    order = [l.strip() for l in open('volgorde.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    skelet = lees_skelet()
    deel_van = {}
    for n in sorted(skelet, key=int):
        b = skelet[n]
        if b.get('bron') and b.get('deel'):
            deel_van.setdefault(b['bron'], b['deel'])
    vorig_deel = None
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
        deel = deel_van.get(sid)
        if deel and deel != vorig_deel:
            parts.append(deel_html(deel))
            vorig_deel = deel
        parts.append(f'<section id="{sid}">\n{body}\n</section>')
    template = open('templates/document/template.html', encoding='utf-8').read()
    out = template.replace('{{SECTIONS}}', '\n\n'.join(parts))
    os.makedirs('dist', exist_ok=True)
    kopieer_assets()
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


def lees_register():
    """id -> {nummer, ronde, stand} uit richtlijnen/hoofdstukregister.md.
    Eén bron voor het nummer dat een hoofdstuk krijgt en hoe ver het is; de
    website leest het hieruit in plaats van het in de lezer te herhalen."""
    pad = 'richtlijnen/hoofdstukregister.md'
    if not os.path.exists(pad):
        return {}
    reg, in_tabel = {}, False
    for regel in open(pad, encoding='utf-8'):
        if regel.startswith('## '):
            in_tabel = False
            continue
        if not regel.startswith('|'):
            continue
        kolom = [k.strip() for k in regel.strip().strip('|').split('|')]
        if kolom[0] == 'id':
            in_tabel = True
            continue
        if not in_tabel or len(kolom) < 4 or set(kolom[0]) <= {'-'}:
            continue
        reg[kolom[0]] = {'nummer': kolom[1], 'ronde': kolom[2], 'stand': kolom[3]}
    return reg


def lees_skelet():
    """nummer -> {titel, stand, secties} uit richtlijnen/skelet.md.

    Het skelet is de grote lijn vóór de woorden: per sectie maximaal drie
    elementen, met de vorm en de herkomst erbij. De lezer toont het boven de
    tekst van het hoofdstuk, zodat de koppeling tussen plan en tekst zichtbaar
    blijft. Eén bron, dus hier niets herhalen (afspraak met Tim, 19-8)."""
    pad = 'richtlijnen/skelet.md'
    if not os.path.exists(pad):
        return {}
    skelet, nu, sectie, deel = {}, None, None, ''
    for regel in open(pad, encoding='utf-8'):
        r = regel.rstrip()
        m = re.match(r'# (Deel .+)$', r)
        if m:
            deel = m.group(1)
            continue
        m = re.match(r'## (\d+) — (.+?)(?: · bron: (\S+))?(?: · (.+))?$', r)
        if m:
            nu = {'nummer': m.group(1), 'titel': m.group(2), 'bron': m.group(3) or '',
                  'stand': m.group(4) or '', 'deel': deel, 'kern': '',
                  'secties': [], 'noot': ''}
            skelet[m.group(1)] = nu
            sectie = None
            continue
        if nu is None:
            continue
        if r.startswith('> ') and not nu['secties']:
            nu['kern'] = (nu['kern'] + ' ' + r[2:]).strip()
            continue
        m = re.match(r'### (.+)$', r)
        if m:
            sectie = {'kop': m.group(1), 'elementen': []}
            nu['secties'].append(sectie)
            continue
        m = re.match(r'- (.*?)\s*`\[(.*?)\]`\s*(.*)$', r)
        if m and sectie is not None:
            vorm = [d.strip() for d in m.group(2).split('·')]
            sectie['elementen'].append({
                't': m.group(1).strip(),
                'v': vorm[0],
                'h': vorm[1] if len(vorm) > 1 else '',
                'n': m.group(3).strip(),
            })
            continue
        m = re.match(r'\*(.+)\*$', r)
        if m and not r.startswith('**'):
            nu['noot'] = m.group(1)
    return skelet


def ontleed_sectie(sid, register=None, skelet=None):
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
    uit = {'id': sid, 'letter': letter, 'titel': titel, 'intro': intro, 'html': html}
    w = (register or {}).get(sid)
    if w:
        uit['werkstand'] = w
    if skelet:
        # Koppelen op bronbestand, niet op nummer: dan kan het skelet omnummeren
        # zonder dat het register en de tekst mee hoeven (afspraak 19-8). Eén
        # bestand kan meer hoofdstukken dragen: e-aktes wordt 6, 7 en 8.
        blokken = [skelet[n] for n in sorted(skelet, key=int)
                   if skelet[n].get('bron') == sid]
        if not blokken and w:
            blokken = [skelet[n] for n in re.findall(r'\d+', w.get('nummer', ''))
                       if n in skelet and not skelet[n].get('bron')]
        if blokken:
            uit['skelet'] = blokken
            uit['deel'] = blokken[0].get('deel', '')
    return uit


def kopieer_assets():
    """Beelden uit content/ verwijzen relatief naar assets/. In webapp/ staat die
    map naast index.html; in dist/ bestond zij niet, dus daar bleef een <img>
    leeg. Hier gekopieerd in plaats van als data-URI ingebed: de drie
    scenario-illustraties zijn samen ruim 2 MB en dat hoort niet in content/."""
    for doel in ('dist', 'dist/hoofdstukken'):
        bron = 'webapp/assets/illustraties'
        if not os.path.isdir(bron):
            continue
        naar = f'{doel}/assets/illustraties'
        os.makedirs(naar, exist_ok=True)
        for naam in os.listdir(bron):
            shutil.copy2(f'{bron}/{naam}', f'{naar}/{naam}')


def vergelijk_site(uiting, secties, dest):
    """Zegt per hoofdstuk of de zichtbare tekst van de repo afwijkt van de
    bestuursversie. Zonder --schrijf gebeurt er verder niets.

    Vergelijken doet hij tegen `bestuursversie/`, niet tegen `webapp/site/`.
    Dat is het hele punt: zodra we de herziening naar webapp/ schrijven, zou een
    vergelijking met webapp/ alleen nog onze eigen laatste schrijfactie meten en
    altijd "gelijk" zeggen. De bevroren bestuursversie is wat het bestuur op
    1 juli las en verandert nooit."""
    bevroren = f'bestuursversie/{os.path.basename(dest)}'
    ijkpunt = bevroren if os.path.exists(bevroren) else dest
    if not os.path.exists(ijkpunt):
        print(f'{ijkpunt} bestaat nog niet — alles zou nieuw zijn.')
        return
    t = open(ijkpunt, encoding='utf-8').read()
    huidig = {d['id']: d for d in json.loads(t[t.find('['):t.rfind(']') + 1])}
    if ijkpunt == bevroren:
        print(f'\nIjkpunt: {bevroren} (de bevroren bestuursversie van 1 juli)')
    else:
        print(f'\nLET OP — geen bevroren bestuursversie gevonden. Ijkpunt is '
              f'{dest}, en dat is de herziening zelf. Deze uitslag bewijst niets.')

    def zichtbaar(h):
        h = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', h, flags=re.S)
        return ' '.join(re.sub(r'<[^>]+>', ' ', h).split())

    afwijkend = []
    print(f'\n{"hoofdstuk":<20}{"zichtbare tekst":<20}bestuur  repo')
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
        print(f'\n{len(afwijkend)} hoofdstuk(ken) wijken af van de bestuursversie: '
              f'{", ".join(afwijkend)}')
        print('Herzien werk hoort hier te staan. Staat er een hoofdstuk bij dat je')
        print('niet zelf hebt aangeraakt, dan is er iets buiten de repo om gebeurd.')
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
    register = lees_register()
    skelet = lees_skelet() if uiting == 'visie' else {}
    secties = [ontleed_sectie(sid, register, skelet) for sid in order]
    if skelet:
        # Een hoofdstuk uit het skelet zonder bronbestand zou onzichtbaar blijven.
        # Hang het achter het hoogste hoofdstuk dat er wél is en ervoor komt,
        # zodat de grote lijn in de lezer heel blijft.
        geclaimd = {}
        for s in secties:
            for b in s.get('skelet', []):
                geclaimd[int(b['nummer'])] = s
        for n in sorted(int(k) for k in skelet):
            if n in geclaimd:
                continue
            eerder = [m for m in geclaimd if m < n]
            if eerder:
                geclaimd[max(eerder)].setdefault('skelet', []).append(skelet[str(n)])
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
    kopieer_assets()
    os.makedirs('dist/hoofdstukken', exist_ok=True)
    dest = f'dist/hoofdstukken/{sid}.html'
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'Gebouwd: {dest} ({len(out)//1000}k tekens)')


def build_tekst():
    """Alle hoofdstuktekst in één bestand: `visie-tekst.md` in de repo-wortel.

    Dit is het deelbestand. Een sessie of persoon zonder toegang tot deze map
    kan er de hele actuele tekst in één keer lezen, op één vast adres. Daarom
    staat het in de wortel en niet in dist/: het is geen bijproduct om te
    controleren maar een uitgifte om te delen.

    Ingebedde afbeeldingen gaan eruit. Eén data-URI van een logo is 32 kB en
    dat is meer dan alle tekst van een hoofdstuk; voor wie dit leest is het ruis.
    Bewerken gebeurt nooit hier, altijd in de losse bestanden in content/."""
    order = [l.strip() for l in open('volgorde.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#')]
    kop = ('<!-- GEGENEREERD, NIET BEWERKEN. Bron: content/*.md, in de volgorde van '
           'volgorde.txt. Opnieuw maken met `python3 build.py tekst`. Ingebedde '
           'afbeeldingen zijn vervangen door een aanduiding. -->')
    parts = [kop]
    for sid in order:
        md_path = f'content/{sid}.md'
        if not os.path.exists(md_path):
            parts.append(f'*[sectie `{sid}`: partial, geen tekstbestand]*')
            continue
        tekst = open(md_path, encoding='utf-8').read().rstrip('\n')
        tekst = re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=\s]+',
                       '[ingebedde afbeelding, hier weggelaten]', tekst)
        parts.append(f'<!-- ======== bestand: content/{sid}.md ======== -->')
        parts.append(tekst)
    dest = 'visie-tekst.md'
    open(dest, 'w', encoding='utf-8').write('\n\n---\n\n'.join(parts) + '\n')
    print(f'Gebouwd: {dest} ({os.path.getsize(dest) // 1024} kB)')

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
