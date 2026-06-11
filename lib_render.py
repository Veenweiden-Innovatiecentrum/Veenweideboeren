# -*- coding: utf-8 -*-
"""Deterministische renderer: MD-subset -> HTML.
Ondersteunt: ## koppen, alinea's, - lijsten, **vet**, *cursief*, [tekst](url),
{{fiche:label|bron|note}}, {{partial:naam}}, raw HTML-blokken (passthrough),
> [!callout Titel] notatie voor nieuwe callouts.
"""
import re, html as _html

VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'source','track','wbr'}

ENT = re.compile(r'&(?:[a-zA-Z][a-zA-Z0-9]*|#\d+|#x[0-9a-fA-F]+);')

def esc_text(s):
    """HTML-escape, maar laat bestaande entiteiten (&shy; etc.) intact."""
    out, i = [], 0
    for m in ENT.finditer(s):
        out.append(s[i:m.start()].replace('&','&amp;'))
        out.append(m.group(0))
        i = m.end()
    out.append(s[i:].replace('&','&amp;'))
    s = ''.join(out)
    return s.replace('<','&lt;').replace('>','&gt;')

def fiche_html(label, source, note=''):
    aria = 'Bron tonen' if label.startswith('Bron') else 'Toelichting tonen'
    h = (f'<span class="fiche-wrap"><button class="fiche-btn" type="button" '
         f'aria-label="{aria}">\u24d8</button><span class="fiche-popup">'
         f'<span class="fiche-label">{esc_text(label)}</span>'
         f'<span class="fiche-source">{esc_text(source)}</span>')
    if note:
        h += f'<span class="fiche-note">{esc_text(note)}</span>'
    return h + '</span></span>'

def render_inline(s, partials=None):
    # placeholders eerst beschermen
    toks = []
    def stash(html_frag):
        toks.append(html_frag); return f'\x00{len(toks)-1}\x00'
    # fiches
    def _fiche(m):
        parts = m.group(1).split('|')
        label = parts[0] if len(parts) > 1 else 'Bron'
        src   = parts[1] if len(parts) > 1 else parts[0]
        note  = parts[2] if len(parts) > 2 else ''
        return stash(fiche_html(label, src, note))
    s = re.sub(r'\{\{fiche:(.+?)\}\}', _fiche, s)
    s = re.sub(r'\{\{bron:(.+?)\}\}', lambda m: stash(fiche_html('Bron', m.group(1))), s)
    # links
    s = re.sub(r'(?<!\\)\[(.+?)\]\((.+?)\)',
               lambda m: stash(f'<a href="{m.group(2)}">{esc_text(m.group(1))}</a>'), s)
    # backslash-escapes tijdelijk wegzetten
    s = re.sub(r'\\([\\*\[\]{#>-])', lambda m: stash_esc(m, toks), s)
    # vet / cursief
    s = re.sub(r'\*\*(.+?)\*\*', lambda m: stash(f'<strong>{esc_text(m.group(1))}</strong>'), s)
    s = re.sub(r'\*(.+?)\*',     lambda m: stash(f'<em>{esc_text(m.group(1))}</em>'), s)
    # rest escapen en placeholders terugzetten
    s = esc_text(s)
    s = re.sub(r'\x00(\d+)\x00', lambda m: toks[int(m.group(1))], s)
    return s

def stash_esc(m, toks):
    toks.append(esc_text(m.group(1)))
    return f'\x00{len(toks)-1}\x00'

def split_blocks(md):
    """Splits MD in blokken. Raw-HTML-blokken (beginnend met '<') lopen door
    tot de tag-balans sluit, óók over lege regels heen."""
    lines = md.split('\n')
    blocks, cur, i = [], [], 0
    TAG = re.compile(r'<!--.*?-->|<[^>]*>', re.S)
    while i < len(lines):
        line = lines[i]
        if not cur and line.lstrip().startswith('<'):
            # raw blok: verzamel tot balans 0
            depth, raw = 0, []
            while i < len(lines):
                raw.append(lines[i])
                for t in TAG.finditer(lines[i]):
                    tok = t.group(0)
                    if tok.startswith('<!--'): continue
                    if tok.startswith('</'): depth -= 1
                    elif tok.endswith('/>'): pass
                    else:
                        name = re.match(r'<([a-zA-Z][\w-]*)', tok)
                        if name and name.group(1).lower() not in VOID:
                            depth += 1
                i += 1
                if depth <= 0:
                    break
            blocks.append(('raw', '\n'.join(raw)))
            continue
        if line.strip() == '':
            if cur: blocks.append(('md', '\n'.join(cur))); cur = []
        else:
            cur.append(line)
        i += 1
    if cur: blocks.append(('md', '\n'.join(cur)))
    return blocks

def render_block(kind, text, partials_dir):
    if kind == 'raw':
        return text
    t = text.strip()
    m = re.match(r'\{\{partial:([\w.-]+)\}\}$', t)
    if m:
        import os
        with open(os.path.join(partials_dir, m.group(1) + '.html'), encoding='utf-8') as f:
            return f.read().rstrip('\n')
    m = re.match(r'(#{2,4})\s+(.*)$', t, re.S)
    if m:
        lvl = len(m.group(1))
        inner = ' '.join(m.group(2).split('\n'))
        return f'<h{lvl}>{render_inline(inner)}</h{lvl}>'
    if all(l.lstrip().startswith('- ') for l in t.split('\n')):
        items = ''.join(f'<li>{render_inline(l.lstrip()[2:])}</li>'
                        for l in t.split('\n'))
        return f'<ul>{items}</ul>'
    if t.startswith('> [!callout'):
        m = re.match(r'> \[!callout\s*([^\]]*)\]\s*(.*)$', t, re.S)
        title = m.group(1).strip()
        body = ' '.join(l.lstrip('> ').strip() for l in m.group(2).split('\n'))
        h = '<div class="callout">'
        if title: h += f'<p class="callout-title">{render_inline(title)}</p>'
        return h + f'<p>{render_inline(body)}</p></div>'
    para = ' '.join(l.strip() for l in t.split('\n'))
    return f'<p>{render_inline(para)}</p>'

def render_md(md, partials_dir='partials'):
    out = []
    for kind, text in split_blocks(md):
        out.append(render_block(kind, text, partials_dir))
    return '\n\n'.join(out)
