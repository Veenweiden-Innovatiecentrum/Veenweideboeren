/* v4 toolbox — register met categoriefilter + maatregelfiches */

const TOOLBOX = window.TOOLBOX_CONTENT;

function FilterPill({ label, active, onClick }) {
  return (
    <button onClick={onClick} style={{
      fontFamily: 'var(--font-heading)', fontSize: 12.5,
      border: '1.5px solid ' + (active ? 'var(--accent)' : 'rgba(0,0,0,.16)'),
      background: active ? 'var(--accent-light)' : '#fff',
      color: active ? 'var(--accent2)' : 'var(--text)',
      fontWeight: active ? 700 : 400,
      borderRadius: 6, padding: '5px 13px', cursor: 'pointer',
      transition: 'all 120ms ease-out',
    }}>{label}</button>
  );
}

function ToolboxRegister({ cat, setCat, openFiche }) {
  const cats = TOOLBOX.categories;
  const zichtbaar = cats.filter((c) => !cat || c.id === cat);
  return (
    <div data-screen-label="Toolbox register">
      <article className="v4-doc" style={{ paddingBottom: 0 }}>
        <Html html={TOOLBOX.introHtml}></Html>
      </article>
      <div style={{ maxWidth: 760, margin: '26px auto 0', display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <FilterPill label="alle" active={!cat} onClick={() => setCat(null)}></FilterPill>
        {cats.map((c) => <FilterPill key={c.id} label={c.naam} active={cat === c.id} onClick={() => setCat(cat === c.id ? null : c.id)}></FilterPill>)}
      </div>
      <div style={{ maxWidth: 760, margin: '26px auto 0', display: 'flex', flexDirection: 'column', gap: 30 }}>
        {zichtbaar.map((c) => (
          <div key={c.id}>
            <h3 style={{ margin: '0 0 12px', fontFamily: 'var(--font-display)', fontSize: 20, color: 'var(--text)' }}>{c.naam}</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 14 }}>
              {c.maatregelen.map((m, i) => (
                <div key={i} onClick={() => openFiche(c.id, i)}
                  onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
                  onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(0,0,0,.12)'; e.currentTarget.style.transform = 'none'; }}
                  style={{ border: '1.5px solid rgba(0,0,0,.12)', borderRadius: 'var(--radius)', background: 'var(--bg3)', padding: '13px 15px', cursor: 'pointer', transition: 'all 140ms ease-out' }}>
                  <p style={{ margin: 0, fontWeight: 700, fontSize: 13.5, fontFamily: 'var(--font-heading)', color: 'var(--text)', lineHeight: 1.4 }}>{m.titel}</p>
                  <p style={{ margin: '6px 0 0', fontSize: 11.5, color: 'var(--text3)', fontFamily: 'var(--font-heading)' }}>{c.naam}{m.lit ? ' · met literatuur' : ''}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      <p style={{ maxWidth: 760, margin: '30px auto 0', fontSize: 13, color: 'var(--text3)', fontFamily: 'var(--font-heading)' }}>
        {cats.reduce((n, c) => n + c.maatregelen.length, 0)} maatregelen · <a href="../documenten/VIC's Veenweideboeren toolbox.html" target="_blank" style={{ color: 'var(--accent2)' }}>volledige toolbox als document ⤓</a>
      </p>
    </div>
  );
}

function FichePagina({ catId, idx, terugRegister, openFiche }) {
  const c = TOOLBOX.categories.find((x) => x.id === catId);
  const m = c && c.maatregelen[idx];
  React.useEffect(() => { window.scrollTo(0, 0); }, [catId, idx]);
  if (!m) return null;
  const buren = c.maatregelen;
  return (
    <div data-screen-label={'Fiche ' + m.titel}>
      <div style={{ maxWidth: 760, margin: '0 auto 18px' }}>
        <TerugKnop onClick={terugRegister}>← register</TerugKnop>
      </div>
      <article className="v4-doc">
        <p style={{ fontFamily: 'var(--font-heading)', fontSize: 11.5, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'var(--accent2)', fontWeight: 700, margin: '0 0 6px' }}>{c.naam}</p>
        <h2 style={{ marginTop: 0 }}>{m.titel}</h2>
        <Html html={m.html}></Html>
        {m.lit && (
          <div style={{ marginTop: 28, borderTop: '1px solid rgba(0,0,0,.1)', paddingTop: 16 }}>
            <h3>Literatuur</h3>
            <Html html={m.lit}></Html>
          </div>
        )}
      </article>
      <div style={{ maxWidth: 760, margin: '30px auto 0', display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {buren.map((b, i) => i !== idx && (
          <FilterPill key={i} label={b.titel} active={false} onClick={() => openFiche(catId, i)}></FilterPill>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { TOOLBOX, ToolboxRegister, FichePagina });
