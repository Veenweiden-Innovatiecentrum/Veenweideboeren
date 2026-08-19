/* v4 visie-lezer — documentvorm (inklapbaar) en magazinevorm (één lange vertelling) */

const VISIE = window.VISIE_CONTENT;
const visieByid = Object.fromEntries(VISIE.map((s) => [s.id, s]));

/* De lezer volgt de volgorde van het document zelf (volgorde.txt), min laag 1 en de
   walkthrough. Zo verschijnt een nieuw hoofdstuk automatisch, ook als het nog geen
   letter of nummer heeft — en dat zijn er vijf in de eindstructuur. */
const BUITEN_DE_LEZER = new Set(['samenvatting', 'walkthrough']);
const HOOFDSTUKKEN = VISIE.filter((s) => !BUITEN_DE_LEZER.has(s.id));

/* ---- werkstand: hulpmiddel tijdens de herziening, geen onderdeel van de publicatie ----
   Zet WERKSTAND_ZICHTBAAR op false voordat dit live gaat.
   De inhoud komt uit richtlijnen/hoofdstukregister.md en wordt door
   `build.py site` meegeschreven. Hier dus niets bijhouden. */
const WERKSTAND_ZICHTBAAR = true;

function Werkstand({ h }) {
  const w = h.werkstand;
  if (!WERKSTAND_ZICHTBAAR || !w) return null;
  const nummer = w.nummer && w.nummer !== '—' ? ' · wordt hoofdstuk ' + w.nummer : '';
  const ronde = w.ronde && w.ronde !== '—' ? ' · ronde ' + w.ronde : '';
  return (
    <p style={{ fontFamily: 'var(--font-mono, monospace)', fontSize: 11, color: 'var(--text3)',
                margin: '-6px 0 14px', letterSpacing: '.01em' }}>
      content/{h.id}.md{nummer}{ronde} · {w.stand}
    </p>
  );
}

/* ---- skelet: de grote lijn vóór de woorden ----
   Komt uit richtlijnen/skelet.md en wordt door `build.py site` meegeschreven.
   Staat boven de tekst zodat de koppeling tussen plan en tekst zichtbaar is.
   Verdwijnt met dezelfde schakelaar als de werkstandregel. */
const VORM_KLEUR = {
  tekst: 'var(--text3)', tabel: 'var(--blue, #3a5a9b)', lijst: 'var(--blue, #3a5a9b)',
  kaarten: 'var(--blue, #3a5a9b)', fiche: 'var(--accent2)', kader: 'var(--amber, #b8860b)',
  beeld: 'var(--accent2)', '—': 'var(--text3)',
};

function Skelet({ h }) {
  const blokken = h.skelet;
  if (!WERKSTAND_ZICHTBAAR || !blokken || !blokken.length) return null;
  return (
    <div style={{ margin: '0 0 22px', padding: '14px 16px', background: 'var(--bg3)',
                  border: '1px solid rgba(0,0,0,.06)', borderLeft: '3px solid var(--accent2)',
                  borderRadius: 'var(--radius)' }}>
      {blokken.map((b) => (
        <div key={b.nummer} style={{ marginBottom: 10 }}>
          <p style={{ margin: '0 0 8px', fontFamily: 'var(--font-sans)', fontSize: 11,
                      textTransform: 'uppercase', letterSpacing: '.07em', color: 'var(--accent2)',
                      fontWeight: 600 }}>
            skelet · {b.deel ? b.deel + ' · ' : ''}{b.nummer} — {b.titel}{b.stand ? ' · ' + b.stand : ''}
          </p>
          {b.kern && (
            <p style={{ margin: '0 0 10px', fontSize: 13, lineHeight: 1.6, color: 'var(--text)' }}>
              {b.kern}
            </p>
          )}
          {b.secties.map((s) => (
            <div key={s.kop} style={{ margin: '0 0 8px' }}>
              <p style={{ margin: '0 0 2px', fontSize: 12.5, fontWeight: 600 }}>{s.kop}</p>
              {s.elementen.map((e, i) => (
                <p key={i} style={{ margin: '0 0 1px', paddingLeft: 12, fontSize: 12.5,
                                    lineHeight: 1.5, color: 'var(--text2)' }}>
                  · {e.t}
                  <span style={{ fontFamily: 'var(--font-mono, monospace)', fontSize: 10.5,
                                 color: VORM_KLEUR[e.v] || 'var(--text3)', marginLeft: 6 }}>
                    [{e.v}{e.h ? ' · ' + e.h : ''}]
                  </span>
                  {e.n && <span style={{ fontSize: 11, color: 'var(--text3)' }}> {e.n}</span>}
                </p>
              ))}
            </div>
          ))}
          {b.noot && <p style={{ margin: '4px 0 0', fontSize: 11.5, fontStyle: 'italic',
                                 color: 'var(--text3)' }}>{b.noot}</p>}
        </div>
      ))}
    </div>
  );
}

/* ---- delen: Deel I tot V boven de hoofdstukken ----
   Het deel komt uit richtlijnen/skelet.md via `build.py site`. Een deelkop
   verschijnt bij het eerste hoofdstuk van dat deel, in de inhoudsopgave en
   in de tekst. Hoofdstukken zonder deel (de wachtkamer) slaan hem over. */
const EERSTE_VAN_DEEL = (() => {
  const uit = {};
  let vorig = null;
  for (const h of HOOFDSTUKKEN) {
    if (h.deel && h.deel !== vorig) { uit[h.id] = h.deel; vorig = h.deel; }
  }
  return uit;
})();

function DeelKop({ id, klein }) {
  const deel = EERSTE_VAN_DEEL[id];
  if (!deel) return null;
  const [nummer, titel] = deel.replace(/^Deel /, '').split(' — ');
  if (klein) {
    return (
      <p style={{ margin: '14px 0 4px', fontFamily: 'var(--font-sans)', fontSize: 10.5,
                  textTransform: 'uppercase', letterSpacing: '.09em', color: 'var(--text3)',
                  fontWeight: 700, paddingTop: 10, borderTop: '1px solid rgba(0,0,0,.08)' }}>
        Deel {nummer} · {titel}
      </p>
    );
  }
  return (
    <p style={{ margin: '2.5rem 0 -0.5rem', paddingTop: '1.1rem',
                borderTop: '2px solid var(--accent2)', fontFamily: 'var(--font-sans)',
                fontSize: 12, textTransform: 'uppercase', letterSpacing: '.12em',
                color: 'var(--accent2)', fontWeight: 700 }}>
      Deel {nummer} <span style={{ color: 'var(--text2)', letterSpacing: '.06em' }}>· {titel}</span>
    </p>
  );
}

/* sfeerfoto per hoofdstuk — alleen in de magazinevorm */
const HOOFDSTUK_FOTO = {
  'scope': 'assets/photos/hero-plant.jpg',
  'a-klem': 'assets/photos/invalshoek-bedrijf.jpg',
  'b-opgaves': 'assets/photos/invalshoek-water.jpg',
  'c-omslag': 'assets/photos/activiteit-overleg-in-het-veld.jpg',
  'd-concept': 'assets/photos/invalshoek-dier.jpg',
  'f-ondernemer': 'assets/photos/activiteit-experimenteren-op-veen.jpg',
  'f-overheid': 'assets/photos/invalshoek-bodem.jpg',
  'f3-bedrijfsleven': 'assets/photos/activiteit-innovatiesprints.jpg',
  'g-perspectief': 'assets/photos/activiteit-leren-uit-het-veld.jpg',
  'h-risicos': 'assets/photos/invalshoek-plant.jpg',
  'slot': 'assets/photos/activiteit-groepen-rondleiden.jpg',
};

/* pull-quotes — letterlijke zinnen uit de hoofdstukken, herhaald als inzet */
const PULL_QUOTES = {
  'scope': 'Geen religie, geen opgedrongen verhaal.',
  'a-klem': 'Niet door eigen falen, maar door een systeem dat ze alleen de verkeerde opties biedt.',
  'b-opgaves': 'Op korte termijn vernietigt margedruk het rentmeesterschap.',
  'c-omslag': 'De boer is niet het probleem, de boer is de motor.',
  'd-concept': 'Het is niet strenger én slechter, het is anders én beter.',
  'e-aktes': 'De motor draait, maar op de verkeerde brandstof.',
  'f-ondernemer': 'De veenweideboer — de ondernemer van akte III — bepaalt zelf hóe de doelen gehaald worden.',
  'f-overheid': 'Ze werken alleen als systeem, je moet op zes niveaus tegelijk bewegen.',
  'f3-bedrijfsleven': 'Het verdienmodel bestaat alleen als de markt aan de andere kant aansluit.',
  'g-perspectief': 'Wat dit document probeert te doen, voorbij de analyse, is iets dat in de meeste beleidsstukken ontbreekt: erkenning.',
  'h-risicos': 'Dezelfde goedbedoelde beleidslogica die akte II deed mislukken, kan ook akte III ondermijnen.',
  'slot': 'Daartussen ligt geen wonder, maar een ontwerpkeuze.',
};

function PullQuote({ tekst }) {
  return <blockquote className="magh-pq">“{tekst}”</blockquote>;
}

/* kop uit de samenvatting — los: meta-badges en H1 */
const VISIE_KOP = (() => {
  const d = document.createElement('div');
  d.innerHTML = visieByid['samenvatting'].html;
  const meta = d.querySelector('.meta-row');
  const h1 = d.querySelector('h1');
  return { meta: meta ? meta.outerHTML : '', h1: h1 ? h1.outerHTML : '' };
})();

/* ---- documentvorm: één doorlopende pagina, hoofdstukken in/uitklapbaar ---- */

function DocumentLezer({ openToolbox, wisselVorm }) {
  const [open, setOpen] = React.useState(() => {
    try { return JSON.parse(localStorage.getItem('vic-v4-doc-open')) || {}; } catch (e) { return {}; }
  });
  // standaard uitgeklapt: alleen expliciet ingeklapte hoofdstukken (false) zijn dicht
  const isUit = (id) => open[id] !== false;
  React.useEffect(() => { localStorage.setItem('vic-v4-doc-open', JSON.stringify(open)); }, [open]);
  const toggle = (id) => setOpen((o) => ({ ...o, [id]: !isUit(id) }));
  const alles = (waarde) => setOpen(Object.fromEntries(HOOFDSTUKKEN.map((h) => [h.id, waarde])));
  const aantalOpen = HOOFDSTUKKEN.filter((h) => isUit(h.id)).length;
  const klapIn = (id) => {
    toggle(id);
    const el = document.getElementById('doc-' + id);
    if (el) { const y = el.getBoundingClientRect().top + window.scrollY - 90; window.scrollTo(0, y); }
  };

  // sticky inhoudsopgave: welk hoofdstuk is in beeld?
  const [actief, setActief] = React.useState(HOOFDSTUKKEN[0] && HOOFDSTUKKEN[0].id);
  React.useEffect(() => {
    const ids = HOOFDSTUKKEN.map((h) => h.id);
    const onScroll = () => {
      let cur = ids[0];
      for (const id of ids) {
        const el = document.getElementById('doc-' + id);
        if (el && el.getBoundingClientRect().top <= 130) cur = id;
      }
      setActief(cur);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  // klik in inhoudsopgave: hoofdstuk openen en er soepel heen scrollen
  const gaNaar = (id) => {
    setOpen((o) => ({ ...o, [id]: true }));
    requestAnimationFrame(() => {
      const el = document.getElementById('doc-' + id);
      if (el) { const y = el.getBoundingClientRect().top + window.scrollY - 96; window.scrollTo({ top: y, behavior: 'smooth' }); }
    });
  };

  return (
    <div data-screen-label="Visie document (doorlopend)">
      <div className="v4-doc-layout">
        <nav className="v4-toc" aria-label="Inhoudsopgave">
          <p className="v4-toc-kop">inhoud</p>
          {HOOFDSTUKKEN.map((h) => (
            <React.Fragment key={h.id}>
              <DeelKop id={h.id} klein={true}></DeelKop>
              <a className={'v4-toc-link' + (actief === h.id ? ' actief' : '')} onClick={() => gaNaar(h.id)}>
                <span className="v4-toc-letter">{h.letter || '·'}</span>
                <span className="v4-toc-titel">{h.titel}</span>
              </a>
            </React.Fragment>
          ))}
        </nav>
        <div className="v4-doc-body">
      <article className="v4-doc" style={{ marginBottom: 6 }}>
        <Html html={VISIE_KOP.meta}></Html>
        <Html html={VISIE_KOP.h1}></Html>
      </article>
      <article className="v4-doc">
        <p className="v4-allesklap" style={{ textAlign: 'right', margin: '0 0 2px' }}>
          <span onClick={() => alles(aantalOpen === 0)}
            style={{ cursor: 'pointer', fontFamily: 'var(--font-sans)', fontSize: 13, fontWeight: 700, color: 'var(--accent2)', whiteSpace: 'nowrap' }}>
            {aantalOpen > 0 ? '\u25be alles inklappen' : '\u25b8 alles uitklappen'}
          </span>
        </p>
        {HOOFDSTUKKEN.map((h) => {
          const isOpen = isUit(h.id);
          const isAktes = h.id === 'e-aktes';
          const isToolbox = h.id === 'f-ondernemer';
          const klap = (
            <span style={{ fontSize: 13, fontFamily: 'var(--font-heading)', fontWeight: 700, color: isOpen ? 'var(--accent2)' : 'var(--text3)', whiteSpace: 'nowrap', flexShrink: 0 }}>
              {isOpen ? '\u25be inklappen' : '\u25b8 uitklappen'}
            </span>
          );
          return (
            <section key={h.id} id={'doc-' + h.id}>
              <DeelKop id={h.id}></DeelKop>
              <h2 onClick={() => toggle(h.id)} style={{ cursor: 'pointer', display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 16 }}>
                <span>{h.letter ? h.letter + ' \u2014 ' : ''}{h.titel}</span>
                {klap}
              </h2>
              <Werkstand h={h}></Werkstand>
              {!isOpen && h.intro && (
                <p onClick={() => toggle(h.id)} style={{ cursor: 'pointer', color: 'var(--text2)' }}>
                  {h.intro.slice(0, 220)}{h.intro.length > 220 ? '\u2026' : ''}
                </p>
              )}
              {!isOpen && isAktes && (
                <div onClick={() => toggle(h.id)} style={{ display: 'flex', gap: 10, cursor: 'pointer' }}>
                  {AKTES.map((a) => <img key={a.n} src={a.src} alt={'Akte ' + a.n} style={{ width: 120, borderRadius: 6, border: '1px solid var(--vic-border)' }} />)}
                </div>
              )}
              {isOpen && (
                <div className="v4-doc-inline">
                  <Skelet h={h}></Skelet>
                  {isAktes && <div style={{ margin: '6px 0 26px' }}><AkteViewer></AkteViewer></div>}
                  <Html html={h.html}></Html>
                  {isToolbox && (
                    <div style={{ margin: '18px 0' }}>
                      <DocCard naam="de toolbox" sub="alle maatregelen als fiches — per categorie, met literatuur" onClick={openToolbox}></DocCard>
                    </div>
                  )}
                  <p onClick={() => klapIn(h.id)} style={{ cursor: 'pointer', fontSize: 13, fontFamily: 'var(--font-heading)', fontWeight: 700, color: 'var(--accent2)', margin: '14px 0 0', textAlign: 'right' }}>
                    ▾ hoofdstuk inklappen
                  </p>
                </div>
              )}
            </section>
          );
        })}
      </article>
      {wisselVorm && (
        <p style={{ maxWidth: 760, margin: '36px auto 0', fontSize: 13, fontFamily: 'var(--font-sans)', color: 'var(--text3)' }}>
          liever als magazine lezen?{' '}
          <span onClick={() => wisselVorm('mag')} style={{ cursor: 'pointer', color: 'var(--accent2)', fontWeight: 700 }}>wissel van vorm →</span>
        </p>
      )}
        </div>
      </div>
    </div>
  );
}

/* ---- magazinevorm: één lange vertelling — volledige tekst, vrijer gezet ---- */

function MagazineLezer({ openToolbox, wisselVorm }) {
  return (
    <div data-screen-label="Visie magazine">
      {/* magazine-cover */}
      <div style={{ maxWidth: 980, margin: '0 auto 18px' }}>
        <div style={{ position: 'relative', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
          <img src="assets/photos/hero-plant.jpg" alt="" style={{ width: '100%', height: 420, objectFit: 'cover', display: 'block' }} />
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(20,30,15,.62), rgba(20,30,15,.05) 55%)' }}></div>
          <div style={{ position: 'absolute', left: 40, right: 40, bottom: 34 }}>
            <p style={{ margin: 0, fontFamily: 'var(--font-sans)', fontSize: 13, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: '#cfe8c8' }}>VIC — visie</p>
            <h1 className="v4-cover-titel" style={{ margin: '6px 0 0', fontSize: 46 }}>Veenweide<span className="cv-groen">boeren</span></h1>
          </div>
        </div>
      </div>

      {HOOFDSTUKKEN.map((h, i) => {
        const foto = HOOFDSTUK_FOTO[h.id];
        if (h.id === 'c-omslag') {
          return (
            <section key={h.id} id={'mag-' + h.id} style={{ margin: '0 auto', maxWidth: 1020, paddingTop: 'clamp(72px, 9vw, 128px)' }}>
              <MagC foto={foto}></MagC>
            </section>
          );
        }
        return (
          <MagHoofdstuk key={h.id} h={h} index={i} foto={foto} quote={PULL_QUOTES[h.id]}
            vooraf={h.id === 'e-aktes' ? <div className="magh-akteviewer"><AkteViewer></AkteViewer></div> : null}
            naBody={h.id === 'f-ondernemer' ? (
              <div className="magh-nabody">
                <DocCard naam="de toolbox" sub="alle maatregelen als fiches — per categorie, met literatuur; de verdieping waarmee we aan de slag gaan" onClick={openToolbox}></DocCard>
              </div>
            ) : null}></MagHoofdstuk>
        );
      })}

      {wisselVorm && (
        <p style={{ maxWidth: 820, margin: '56px auto 0', fontSize: 13, fontFamily: 'var(--font-sans)', color: 'var(--text3)' }}>
          liever als doorlopend document lezen?{' '}
          <span onClick={() => wisselVorm('doc')} style={{ cursor: 'pointer', color: 'var(--accent2)', fontWeight: 700 }}>wissel van vorm →</span>
        </p>
      )}
    </div>
  );
}

/* ---- laag 1 ---- */

function VisieLaag1({ vorm, wisselVorm, openHoofdstuk, openToolbox }) {
  if (vorm === 'mag') return <MagazineLezer openToolbox={openToolbox} wisselVorm={wisselVorm}></MagazineLezer>;
  return <DocumentLezer openToolbox={openToolbox} wisselVorm={wisselVorm}></DocumentLezer>;
}

Object.assign(window, { VISIE, HOOFDSTUKKEN, VisieLaag1, visieByid });
