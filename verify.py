# -*- coding: utf-8 -*-
"""Verificatie: dist vs origineel.
1. Zichtbare tekst moet 100% identiek zijn (whitespace-genormaliseerd).
2. DOM-structuur van <body> moet identiek zijn (tags + attributen + tekst)."""
import re, sys, difflib
from bs4 import BeautifulSoup
from lxml import html as LH

ORIG = 'origineel/VIC_s_veenweideboeren_visie_v2.html'
DIST = "dist/VIC's veenweideboeren visie.html"

def visible_text(path):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'lxml')
    for t in soup(['script', 'style']):
        t.decompose()
    txt = soup.get_text(' ')
    txt = txt.replace('\xad', '').replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', txt).strip()

def dom_canon(path):
    tree = LH.parse(path)
    body = tree.find('body')
    def walk(el, out):
        out.append('<' + el.tag + ''.join(
            f' {k}={el.attrib[k]!r}' for k in sorted(el.attrib)) + '>')
        if el.text and el.text.strip():
            out.append('T:' + re.sub(r'\s+', ' ', el.text.replace('\xad','')).strip())
        for c in el:
            if isinstance(c.tag, str):
                walk(c, out)
            if c.tail and c.tail.strip():
                out.append('T:' + re.sub(r'\s+', ' ', c.tail.replace('\xad','')).strip())
        out.append('</' + el.tag + '>')
    out = []
    walk(body, out)
    return out

t1, t2 = visible_text(ORIG), visible_text(DIST)
print('1. Zichtbare tekst identiek:', 'JA \u2713' if t1 == t2 else 'NEE \u2717')
if t1 != t2:
    sm = difflib.SequenceMatcher(None, t1, t2)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != 'equal':
            print(f'  {op}: orig[{a1}:{a2}]={t1[a1:a2]!r:.120} dist[{b1}:{b2}]={t2[b1:b2]!r:.120}')

d1, d2 = dom_canon(ORIG), dom_canon(DIST)
print('2. DOM-structuur identiek: ', 'JA \u2713' if d1 == d2 else 'NEE \u2717')
if d1 != d2:
    n = 0
    for line in difflib.unified_diff(d1, d2, lineterm='', n=1):
        if line.startswith(('+','-')) and not line.startswith(('+++','---')):
            print('  ' + line[:160]); n += 1
            if n > 30: print('  ... (afgekapt)'); break
sys.exit(0 if (t1 == t2 and d1 == d2) else 1)
