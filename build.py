# -*- coding: utf-8 -*-
"""Build: assembleert dist/<uiting> uit content/ + partials/ + templates/.
Gebruik: python3 build.py document"""
import os, sys, re, shutil, datetime, urllib.parse
import lib_render as R

VERSIEMAP = 'dist/versies'
ORIGINEEL = 'origineel/VIC_s_veenweideboeren_visie_v2.html'

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

def versies_op_schijf():
    """De vastgelegde versies, als lijst van (nummer, bestandsnaam), oplopend."""
    if not os.path.isdir(VERSIEMAP):
        return []
    gevonden = []
    for naam in os.listdir(VERSIEMAP):
        m = re.match(r'v(\d+) ', naam)
        if m and naam.endswith('.html'):
            gevonden.append((int(m.group(1)), naam))
    return sorted(gevonden)


def leg_origineel_vast():
    """Zet het onbewerkte v2-document eenmalig in het archief, zodat de reeks
    begint bij wat er was voordat de herziening startte."""
    if any(nr == 2 for nr, _ in versies_op_schijf()):
        return
    if not os.path.exists(ORIGINEEL):
        sys.exit(f'FOUT: {ORIGINEEL} ontbreekt — het archief kan niet beginnen')
    shutil.copyfile(ORIGINEEL, f'{VERSIEMAP}/v2 — origineel, voor de herziening.html')


def schrijf_versie_index():
    versies = versies_op_schijf()
    rijen = []
    for nr, naam in reversed(versies):
        m = re.match(r'v\d+ — (.*)\.html$', naam)
        omschrijving = m.group(1) if m else naam
        laatste = ' <span class="laatste">nieuwste</span>' if nr == versies[-1][0] else ''
        rijen.append(
            f'<li><a href="{urllib.parse.quote(naam)}"><span class="nr">v{nr}</span>'
            f'<span class="wat">{omschrijving}</span></a>{laatste}</li>')
    html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Veenweideboeren — versies</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#F7F5F0;color:#2A2824;font-family:'Roboto',-apple-system,sans-serif;
font-size:15px;line-height:1.7;padding:3rem 1.5rem}}
main{{max-width:640px;margin:0 auto}}
h1{{font-family:'Playfair Display',Georgia,serif;font-size:32px;line-height:1.2;margin-bottom:.5rem}}
p.uitleg{{color:#5C5A54;margin-bottom:2rem;max-width:520px}}
ul{{list-style:none}}
li{{display:flex;align-items:center;gap:.75rem;border-top:1px solid rgba(0,0,0,.08)}}
li:last-child{{border-bottom:1px solid rgba(0,0,0,.08)}}
a{{flex:1;display:flex;align-items:baseline;gap:1rem;padding:.9rem 0;
text-decoration:none;color:inherit}}
a:hover .wat{{color:#2d6a23}}
.nr{{font-family:'JetBrains Mono',monospace;font-size:13px;color:#8A877F;min-width:2.5rem}}
.wat{{font-weight:500}}
.laatste{{font-size:10px;text-transform:uppercase;letter-spacing:.08em;
background:#3ea635;color:#fff;padding:2px 8px;border-radius:3px}}
</style>
</head>
<body>
<main>
<h1>Veenweideboeren — versies</h1>
<p class="uitleg">Elke afgeronde ronde wordt hier vastgelegd. Wat eenmaal in deze
lijst staat verandert niet meer, ook niet als het document verder wordt herzien.</p>
<ul>
{chr(10).join(rijen)}
</ul>
</main>
</body>
</html>
'''
    open(f'{VERSIEMAP}/index.html', 'w', encoding='utf-8').write(html)


def build_versie(label):
    """Bouwt het document en legt het vast als onveranderlijke versie.
    Eerdere versies blijven staan; een bestaande versie wordt nooit overschreven."""
    build_document()
    os.makedirs(VERSIEMAP, exist_ok=True)
    leg_origineel_vast()
    nummers = [nr for nr, _ in versies_op_schijf()]
    nr = max(nummers, default=1) + 1
    dest = f'{VERSIEMAP}/v{nr} — {label}, {datetime.date.today().isoformat()}.html'
    if os.path.exists(dest):
        sys.exit(f'FOUT: {dest} bestaat al — vastgelegde versies worden niet overschreven')
    shutil.copyfile("dist/VIC's Veenweideboeren visie.html", dest)
    schrijf_versie_index()
    print(f'Vastgelegd: {dest}')
    print(f'Archief:    {VERSIEMAP}/index.html ({len(versies_op_schijf())} versies)')


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
    template = open('templates/document/template.html', encoding='utf-8').read()
    head = template.split('</head>')[0] + '</head>'
    out = (f'{head}\n<body>\n<main>\n<section id="{sid}">\n{body}\n</section>\n'
           f'</main>\n</body>\n</html>\n')
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
    elif target == 'hoofdstuk':
        if len(sys.argv) < 3:
            sys.exit('FOUT: geef het hoofdstuk mee, bv. python3 build.py hoofdstuk c-omslag')
        build_hoofdstuk(sys.argv[2])
    elif target == 'versie':
        if len(sys.argv) < 3:
            sys.exit('FOUT: geef een omschrijving mee, bv. python3 build.py versie "na ronde 1"')
        build_versie(sys.argv[2])
    else:
        sys.exit(f'Onbekende uiting: {target} (beschikbaar: document, toolbox, '
                 'programmavoorstel, tekst, hoofdstuk <id>, versie "<omschrijving>")')
