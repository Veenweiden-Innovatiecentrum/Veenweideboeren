# -*- coding: utf-8 -*-
"""Build: assembleert dist/<uiting> uit content/ + partials/ + templates/.
Gebruik: python3 build.py document"""
import os, sys
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
    dest = "dist/VIC's veenweideboeren visie.html"
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
    dest = "dist/VIC programmavoorstel veenweideboeren.html"
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
    dest = "dist/VIC toolbox veenweideboer.html"
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
    else:
        sys.exit(f'Onbekende uiting: {target} (beschikbaar: document, tekst)')
