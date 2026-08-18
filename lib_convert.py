# -*- coding: utf-8 -*-
"""Omzetlogica HTML -> Markdown, met terugreken-controle per blok.

Uit convert.py gehaald zodat convert.py (eenmalige splitser van het v2-origineel)
en importeer.py (haalt de gepubliceerde website terug naar content/) dezelfde
bewezen route delen. Een blok wordt alleen Markdown als het teruggerenderd
exact dezelfde DOM oplevert; anders blijft het onaangeroerde HTML.
"""
import re, os, sys
from bs4 import BeautifulSoup
from lxml import etree
import lib_render as R

# ---------- hulpfuncties ----------
TAG = re.compile(r'<!--.*?-->|<[^>]*>', re.S)

def norm_dom(fragment):
    """Parse fragment en geef canonieke string met genormaliseerde whitespace."""
    try:
        root = etree.fromstring(f'<root>{fragment}</root>',
                                parser=etree.XMLParser(recover=True))
    except Exception:
        return None
    def walk(el):
        parts = [f'<{etree.QName(el).localname}']
        for k in sorted(el.attrib):
            parts.append(f' {k}="{el.attrib[k]}"')
        parts.append('>')
        if el.text:
            parts.append(re.sub(r'\s+', ' ', el.text))
        for c in el:
            if isinstance(c.tag, str):
                parts.append(walk(c))
            if c.tail:
                parts.append(re.sub(r'\s+', ' ', c.tail))
        parts.append(f'</{etree.QName(el).localname}>')
        return ''.join(parts)
    return walk(root)

def top_level_chunks(inner):
    """Splits sectie-inner-HTML in top-level chunks (exacte bronslices)."""
    chunks, pos, depth, start = [], 0, 0, None
    for m in TAG.finditer(inner):
        tok = m.group(0)
        if depth == 0:
            txt = inner[pos:m.start()]
            if txt.strip():
                chunks.append(('text', txt))
            if tok.startswith('<!--'):
                chunks.append(('comment', tok)); pos = m.end(); continue
            start = m.start()
        if tok.startswith('<!--'):
            pass
        elif tok.startswith('</'):
            depth -= 1
            if depth == 0:
                chunks.append(('el', inner[start:m.end()])); pos = m.end()
        elif tok.endswith('/>'):
            if depth == 0:
                chunks.append(('el', tok)); pos = m.end()
        else:
            name = re.match(r'<([a-zA-Z][\w-]*)', tok)
            if name and name.group(1).lower() in R.VOID:
                if depth == 0:
                    chunks.append(('el', tok)); pos = m.end()
            else:
                depth += 1
        if depth == 0 and not tok.startswith('<!--'):
            pos = max(pos, m.end())
    return chunks

ESC = {'\\':'\\\\','*':'\\*','[':'\\[',']':'\\]','{':'\\{','#':'\\#'}
def md_escape(s):
    s = ''.join(ESC.get(c, c) for c in s)
    s = s.replace('\xad','&shy;').replace('\xa0','&nbsp;')
    return s

def inline_to_md(node):
    """bs4-node (p/h/li) -> MD-inline string, of None als niet converteerbaar."""
    out = []
    for c in node.children:
        if isinstance(c, str):
            out.append(md_escape(str(c)))
        elif c.name == 'strong':
            if c.find(): return None
            out.append('**' + md_escape(c.get_text()) + '**')
        elif c.name == 'em':
            if c.find(): return None
            out.append('*' + md_escape(c.get_text()) + '*')
        elif c.name == 'a':
            if c.find() or set(c.attrs) - {'href'}: return None
            out.append(f'[{md_escape(c.get_text())}]({c["href"]})')
        elif c.name == 'span' and 'fiche-wrap' in (c.get('class') or []):
            lab = c.select_one('.fiche-label')
            src = c.select_one('.fiche-source')
            note = c.select_one('.fiche-note')
            if not (lab and src): return None
            parts = [lab.get_text(), src.get_text()]
            if note: parts.append(note.get_text())
            if any('|' in p or '}}' in p for p in parts): return None
            out.append('{{fiche:' + '|'.join(p.replace('\xad','&shy;') for p in parts) + '}}')
        else:
            return None
    s = ' '.join(''.join(out).split())
    return s or None

def chunk_to_md(src):
    """Probeer één chunk naar MD; return md-string of None (=raw houden)."""
    soup = BeautifulSoup(src, 'lxml')
    el = soup.find()
    while el and el.name in ('html','body'):
        el = el.find()
    if el is None: return None
    if el.get('style') or el.get('class') or el.get('id'):
        return None
    if el.name in ('h2','h3','h4'):
        inner = inline_to_md(el)
        return None if inner is None else '#'*int(el.name[1]) + ' ' + inner
    if el.name == 'p':
        inner = inline_to_md(el)
        return None if inner is None else inner
    if el.name in ('ul','ol') and el.name == 'ul':
        items = []
        for li in el.find_all('li', recursive=False):
            if li.get('style') or li.get('class'): return None
            inner = inline_to_md(li)
            if inner is None: return None
            items.append('- ' + inner)
        if len(items) != len([c for c in el.children if getattr(c,'name',None)]):
            return None
        return '\n'.join(items)
    return None

def verified_md(src):
    """MD-conversie mét round-trip-DOM-check."""
    md = chunk_to_md(src)
    if md is None: return None
    back = R.render_block('md', md, 'partials')
    if norm_dom(back) != norm_dom(src):
        return None
    return md
