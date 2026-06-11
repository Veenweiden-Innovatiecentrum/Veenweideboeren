# Veenweideboeren — bronrepository

E�n bron, meerdere uitingsvormen (HTML-document, website, infographic, Word).

## Structuur

| Map | Inhoud |
|---|---|
| `content/` | **De basistekst** — alle tekst als Markdown. Dit is de enige plek waar inhoud wordt geredigeerd. |
| `richtlijnen/` | Tone of voice en terminologie (harde redactieregels). |
| `design/` | Design-tokens (kleuren, typografie), logo's, huisstijl-assets. |
| `partials/` | Interactieve/visuele blokken: SVG-diagrammen, walkthrough-slides, toggles. |
| `templates/` | Eén template per uitingsvorm (`document/`, later `website/`, `infographic/`, `docx/`). |
| `dist/` | Gegenereerde output. **Nooit handmatig bewerken.** |
| `origineel/` | Referentie: de oorspronkelijke v2-HTML waartegen de build wordt geverifieerd. |

## Werkwijze

1. Tekst wijzigen in `content/*.md`
2. `python build.py document` draaien
3. Output in `dist/` controleren
4. Committen — de diff toont exact en alleen wat veranderde
