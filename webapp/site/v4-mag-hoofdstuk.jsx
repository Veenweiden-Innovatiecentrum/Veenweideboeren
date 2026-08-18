/* Magazine-opmaak voor ALLE hoofdstukken — met exact dezelfde inhoud.
   De tekst wordt nooit overgetypt: magVerwerk() transformeert de bron-HTML
   in het geheugen (titel naar de opener, eerste alinea als lead, kaders
   gemarkeerd als editoriale callouts). Elk woord blijft staan. */

const MAG_TOON = {
  'var(--blue-light)': 'blauw',
  'var(--amber-light)': 'amber',
  'var(--red-light)': 'rood',
  'var(--accent-light)': 'groen',
  'var(--bg2)': 'neutraal',
};

function magVerwerk(html) {
  const d = document.createElement('div');
  d.innerHTML = html;

  // hoofdstuktitel verhuist naar de opener
  const h2 = d.querySelector(':scope > h2');
  if (h2 && h2 === d.firstElementChild) h2.remove();

  // kaders worden editoriale callouts (kleurtoon wisselt af)
  let beurt = 0;
  for (const div of [...d.children]) {
    if (div.tagName !== 'DIV') continue;
    const st = div.getAttribute('style') || '';
    const m = st.match(/background:\s*(var\(--[a-z0-9-]+\))/);
    if (!m) continue;
    let toon = MAG_TOON[m[1]];
    if (m[1] === 'var(--bg3)') { toon = beurt % 2 === 0 ? 'groen' : 'blauw'; beurt++; }
    if (!toon) continue;
    div.classList.add('magh-callout', 'magh-callout--' + toon);
  }

  // eerste alinea wordt de lead (alleen als die ook echt vooraan staat)
  let lead = null, dropcap = false;
  const eerste = d.firstElementChild;
  if (eerste && eerste.tagName === 'P') {
    lead = eerste.outerHTML;
    dropcap = /^[A-Za-z\u00C0-\u017E]/.test((eerste.textContent || '').trim());
    eerste.remove();
  }
  return { lead, dropcap, rest: d.innerHTML };
}

/* drie opener-varianten — afgewisseld voor magazineritme */
function MagOpener({ h, foto, variant }) {
  const kicker = h.letter ? 'Hoofdstuk ' + h.letter : null;
  if (variant === 'typo' || !foto) {
    return (
      <header className="magh-opener-typo">
        {kicker && <span className="magc-kicker">{kicker}</span>}
        <h1 className="magh-titel-donker">{h.titel}</h1>
      </header>
    );
  }
  if (variant === 'split') {
    return (
      <header className="magh-opener-split">
        <div>
          {kicker && <span className="magc-kicker">{kicker}</span>}
          <h1 className="magh-titel-donker">{h.titel}</h1>
        </div>
        <img className="magh-split-foto" src={foto} alt="" />
      </header>
    );
  }
  return (
    <header className="magc-opener magh-opener-vol">
      <img src={foto} alt="" className="magc-opener-img" />
      <div className="magc-opener-veil"></div>
      <div className="magc-opener-tekst">
        {kicker && <span className="magc-kicker magc-kicker--licht">{kicker}</span>}
        <h1 className="magh-vol-titel">{h.titel}</h1>
      </div>
    </header>
  );
}

function MagHoofdstuk({ h, index, foto, quote, vooraf, naBody }) {
  const v = React.useMemo(() => magVerwerk(h.html), [h.id]);
  const variant = (!foto || h.id === 'intro' || h.id === 'slot')
    ? 'typo'
    : (index % 2 === 1 ? 'vol' : 'split');
  return (
    <section id={'mag-' + h.id} className={'magh' + (index === 0 ? ' magh--eerste' : '')}>
      <MagOpener h={h} foto={foto} variant={variant}></MagOpener>
      {v.lead && (
        <div className={'magh-lead' + (v.dropcap ? ' magh-heeft-dropcap' : '')}>
          <Html html={v.lead}></Html>
        </div>
      )}
      {quote && <blockquote className="magh-pq">“{quote}”</blockquote>}
      {vooraf}
      <article className="v4-doc v4-mag magh-body">
        <Html html={v.rest}></Html>
      </article>
      {naBody}
      {h.id === 'slot' && foto && <img src={foto} alt="" className="magh-slotfoto" />}
    </section>
  );
}

Object.assign(window, { MagHoofdstuk });
