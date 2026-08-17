# -*- coding: utf-8 -*-
"""Build: assembleert dist/<uiting> uit content/ + partials/ + templates/.
Gebruik: python3 build.py document"""
import os, sys, re, shutil, datetime, urllib.parse
import lib_render as R

VERGELIJK = 'dist/vergelijk'
HUIDIGE = f'{VERGELIJK}/1 — huidige visie (bevroren).html'
HERZIENE = f'{VERGELIJK}/2 — herziene visie (groeit mee).html'

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
    # De herziene versie in dist/vergelijk/ groeit hiermee mee, zodat een
    # geopend browserwindow altijd de laatste stand toont na verversen.
    os.makedirs(VERGELIJK, exist_ok=True)
    open(HERZIENE, 'w', encoding='utf-8').write(out)
    schrijf_vergelijk_index()
    print(f'Bijgewerkt: {HERZIENE}')


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


def schrijf_vergelijk_index():
    """Startpagina van de vergelijkmap. Zegt welke van de twee meegroeit."""
    tijd = datetime.datetime.now().strftime('%d-%m-%Y om %H:%M')
    def rij(pad, nr, titel, wat, live):
        if not os.path.exists(pad):
            return ''
        label = ('<span class="tag live">groeit mee</span>' if live
                 else '<span class="tag vast">bevroren</span>')
        return (f'<li><a href="{urllib.parse.quote(os.path.basename(pad))}">'
                f'<span class="nr">{nr}</span><span class="wat">'
                f'<strong>{titel}</strong><span class="sub">{wat}</span></span></a>{label}</li>')
    rijen = [
        rij(HUIDIGE, '1', 'Huidige visie',
            'Zoals die op main staat. Wordt nooit opnieuw gebouwd', False),
        rij(HERZIENE, '2', 'Herziene visie',
            f'Laatst bijgewerkt {tijd}. Verversen toont de nieuwste stand', True),
    ]
    html = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Veenweideboeren — vergelijken</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#F7F5F0;color:#2A2824;font-family:'Roboto',-apple-system,sans-serif;
font-size:15px;line-height:1.7;padding:3rem 1.5rem}}
main{{max-width:660px;margin:0 auto}}
h1{{font-family:'Playfair Display',Georgia,serif;font-size:32px;line-height:1.2;margin-bottom:.5rem}}
p.uitleg{{color:#5C5A54;margin-bottom:2rem;max-width:560px}}
ul{{list-style:none}}
li{{display:flex;align-items:center;gap:1rem;border-top:1px solid rgba(0,0,0,.08)}}
li:last-child{{border-bottom:1px solid rgba(0,0,0,.08)}}
a{{flex:1;display:flex;align-items:flex-start;gap:1.25rem;padding:1rem 0;
text-decoration:none;color:inherit}}
a:hover strong{{color:#2d6a23}}
.nr{{font-family:'JetBrains Mono',monospace;font-size:20px;color:#8A877F;
min-width:1.5rem;line-height:1.4}}
.wat strong{{display:block;font-size:16px;font-weight:600}}
.wat .sub{{display:block;font-size:13px;color:#5C5A54;line-height:1.5}}
.tag{{font-size:10px;text-transform:uppercase;letter-spacing:.08em;
padding:3px 9px;border-radius:3px;white-space:nowrap;font-weight:500}}
.tag.live{{background:#3ea635;color:#fff}}
.tag.vast{{background:#EDEAE3;color:#5C5A54}}
</style>
</head>
<body>
<main>
<h1>Veenweideboeren — vergelijken</h1>
<p class="uitleg">Open beide in een eigen browserwindow en zet ze naast elkaar.
Links de visie zoals die nu is, rechts de herziening. Alleen de rechter verandert;
verversen laat de laatste stand zien.</p>
<ul>
{chr(10).join(r for r in rijen if r)}
</ul>
</main>
</body>
</html>
'''
    open(f'{VERGELIJK}/index.html', 'w', encoding='utf-8').write(html)


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
    else:
        sys.exit(f'Onbekende uiting: {target} (beschikbaar: document, toolbox, '
                 'programmavoorstel, tekst, hoofdstuk <id>)')
