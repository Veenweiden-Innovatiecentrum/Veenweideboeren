/* v4 gedeelde componenten — Html-renderer, ScenarioViewer, kleine UI-delen */

function Html({ html, className, style }) {
  return <section data-nt-sectie="" className={className} style={style} dangerouslySetInnerHTML={{ __html: html }}></section>;
}

const SCENARIOS = [
  { n: 'I', src: 'assets/illustraties/akte-1.jpg', sub: 'er wordt gestuurd op middelen' },
  { n: 'II', src: 'assets/illustraties/akte-2.jpg', sub: 'sturen op doelen, zonder verdienmodel eronder' },
  { n: 'III', src: 'assets/illustraties/akte-3.jpg', sub: 'dezelfde doelsturing, mét verdienmodel eronder' },
];

function ScenarioViewer() {
  const [scenario, setScenario] = React.useState(0);
  const [playing, setPlaying] = React.useState(false);

  React.useEffect(() => {
    if (!playing) return;
    const id = setInterval(() => {
      setScenario((a) => { if (a >= 2) { setPlaying(false); return 2; } return a + 1; });
    }, 3200);
    return () => clearInterval(id);
  }, [playing]);

  const knop = (active) => ({
    fontFamily: 'var(--font-heading)', fontSize: 13.5, fontWeight: active ? 700 : 400,
    border: '1.5px solid ' + (active ? 'var(--accent)' : 'rgba(0,0,0,.18)'),
    background: active ? 'var(--accent-light)' : '#fff',
    color: active ? 'var(--accent2)' : 'var(--text)',
    borderRadius: 6, padding: '7px 18px', cursor: 'pointer',
    transition: 'all 140ms ease-out',
  });

  return (
    <div>
      <div style={{ position: 'relative', aspectRatio: '2560 / 1600', borderRadius: 'var(--radius-lg)', overflow: 'hidden', background: '#fff', border: '1px solid rgba(0,0,0,.08)' }}>
        {SCENARIOS.map((a, i) => (
          <img key={a.n} src={a.src} alt={'Scenario ' + a.n}
            style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain', opacity: i === scenario ? 1 : 0, transition: 'opacity 1500ms ease-in-out' }} />
        ))}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10, marginTop: 16, flexWrap: 'wrap' }}>
        {SCENARIOS.map((a, i) => (
          <button key={a.n} onClick={() => { setPlaying(false); setScenario(i); }} style={knop(i === scenario)}>scenario {a.n}</button>
        ))}
        <button onClick={() => { if (!playing && scenario === 2) setScenario(0); setPlaying(!playing); }}
          style={{ ...knop(playing), borderColor: 'var(--blue)', color: playing ? '#fff' : 'var(--blue)', background: playing ? 'var(--blue)' : '#fff' }}>
          {playing ? '\u25fc stop' : '\u25b6 speel af'}
        </button>
      </div>
      <p style={{ textAlign: 'center', margin: '12px 0 0', fontSize: 13, color: 'var(--text3)', fontFamily: 'var(--font-heading)' }}>
        scenario {SCENARIOS[scenario].n} — {SCENARIOS[scenario].sub}
      </p>
    </div>
  );
}

function TerugKnop({ onClick, children }) {
  return (
    <button onClick={onClick} style={{
      fontFamily: 'var(--font-heading)', fontSize: 13, border: '1.5px solid rgba(0,0,0,.18)',
      background: '#fff', borderRadius: 6, padding: '6px 14px', cursor: 'pointer', color: 'var(--text2)',
    }}>{children}</button>
  );
}

function Kicker({ color = 'var(--accent2)', children }) {
  return <span style={{ fontFamily: 'var(--font-heading)', fontSize: 11.5, letterSpacing: '0.14em', textTransform: 'uppercase', color, fontWeight: 700 }}>{children}</span>;
}

function DocCard({ naam, sub, onClick }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div onClick={onClick} onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        border: '1.5px solid ' + (hover ? 'var(--blue)' : 'rgba(0,0,0,.12)'),
        background: 'var(--bg3)', borderRadius: 'var(--radius-lg)', padding: '20px 22px',
        cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: 8,
        transition: 'transform 140ms ease-out, border-color 140ms ease-out, box-shadow 140ms ease-out',
        transform: hover ? 'translateY(-3px)' : 'none',
        boxShadow: hover ? '0 8px 20px rgba(29,49,118,.10)' : '0 2px 6px rgba(0,0,0,.04)',
      }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
        <p style={{ margin: 0, fontWeight: 700, fontSize: 16, fontFamily: 'var(--font-display)', color: hover ? 'var(--blue)' : 'var(--text)' }}>{naam}</p>
        <span style={{ color: 'var(--blue)', fontWeight: 700, fontSize: 18 }}>→</span>
      </div>
      <p style={{ margin: 0, fontSize: 13.5, color: 'var(--text2)', lineHeight: 1.55 }}>{sub}</p>
    </div>
  );
}

Object.assign(window, { Html, SCENARIOS, ScenarioViewer, TerugKnop, Kicker, DocCard });
