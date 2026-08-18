/* Notitielaag — bezoekers laten per blok een notitie achter.
   Demo-opslag: localStorage, in exact de datastructuur van de latere
   Vercel-API ({id, bezoekerId, naam, pagina, anker, tekst, aangemaakt,
   gewijzigd}). Productie: POST /api/notities + GET /api/notities?bezoeker=…
   Naam is verplicht; notities zijn alleen zichtbaar voor de bezoeker zelf
   en (centraal) voor het VIC. */

(() => {
  const LS_PROFIEL = 'vic-nt-profiel';
  const LS_NOTITIES = 'vic-nt-notities';

  const lees = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } };
  const schrijf = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : 'nt-' + Math.random().toString(36).slice(2) + Date.now());

  let profiel = lees(LS_PROFIEL, null);
  if (!profiel) { profiel = { id: uuid(), naam: '' }; schrijf(LS_PROFIEL, profiel); }

  let notitieCache = null;
  const alleNotities = () => notitieCache || (notitieCache = lees(LS_NOTITIES, []));
  const bewaarNotities = (n) => { notitieCache = n; schrijf(LS_NOTITIES, n); werkWidgetBij(); };

  /* ---------- server-synchronisatie (Upstash via /api/notities) ---------- */

  function syncBewaar(notitie) {
    fetch('/api/notities', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(notitie),
    }).catch(() => {});
  }
  function syncVerwijder(anker) {
    fetch('/api/notities?bezoeker=' + encodeURIComponent(profiel.id) + '&anker=' + encodeURIComponent(anker), { method: 'DELETE' }).catch(() => {});
  }
  async function syncOphalen() {
    try {
      const r = await fetch('/api/notities?bezoeker=' + encodeURIComponent(profiel.id));
      if (!r.ok) return;
      const server = await r.json();
      if (!Array.isArray(server) || !server.length) return;
      // samenvoegen: per anker wint de nieuwste versie
      const lokaal = alleNotities();
      const perAnker = {};
      for (const n of lokaal) perAnker[n.anker] = n;
      let gewijzigd = false;
      for (const n of server) {
        const eigen = perAnker[n.anker];
        if (!eigen || (n.gewijzigd > eigen.gewijzigd)) { perAnker[n.anker] = n; gewijzigd = true; }
      }
      if (gewijzigd) {
        bewaarNotities(Object.values(perAnker));
        for (const m of markers) bijwerkMarker(m);
      }
    } catch (e) { /* geen server (lokale preview) — stil doorgaan */ }
  }
  const notitieVoor = (anker) => alleNotities().find((n) => n.anker === anker);

  const route = () => lees('vic-v4-route', { page: '?' });

  const hoofdstukTitel = (key) => {
    const hs = (window.HOOFDSTUKKEN || []).find((h) => h.id === key);
    if (hs) return (hs.letter ? hs.letter + ' — ' : '') + hs.titel;
    return key;
  };

  /* ---------- ankers stempelen ---------- */

  const SKIP = new Set(['H1', 'H2', 'SCRIPT', 'STYLE']);
  let markers = []; // {anker, blok, el}

  function stempel() {
    notitieCache = null;
    // dode markers: knop écht uit de DOM halen vóór ze uit de lijst gaan
    markers = markers.filter((m) => {
      const leeft = document.contains(m.blok);
      if (!leeft) m.el.remove();
      return leeft;
    });
    // weesknoppen die buiten de lijst om zijn achtergebleven opruimen
    for (const el of document.querySelectorAll('.nt-knop')) {
      if (!markers.some((m) => m.el === el)) el.remove();
    }

    // 1. alle Html-secties
    let losseSectie = 0;
    for (const sec of document.querySelectorAll('[data-nt-sectie]')) {
      const houder = sec.closest('[id^="doc-"],[id^="mag-"]');
      const r = route();
      let key;
      if (houder) {
        key = houder.id.replace(/^(doc|mag)-/, '');
      } else {
        // geen hoofdstuk-anker: sleutel per losse sectie, in documentvolgorde
        key = r.page + (r.cat != null ? ':' + r.cat + (r.idx != null ? ':' + r.idx : '') : '') + ':s' + losseSectie;
        losseSectie++;
      }
      const inLead = !!sec.closest('.magh-lead');
      const offset = (!inLead && sec.closest('.magh-body') && sec.closest('.magh') && sec.closest('.magh').querySelector('.magh-lead')) ? 1 : 0;
      let i = 0;
      for (const blok of sec.children) {
        if (SKIP.has(blok.tagName) || blok.classList.contains('nt-knop')) continue;
        const anker = key + ':' + (inLead ? 0 : offset + i);
        maakMarker(blok, anker);
        i++;
      }
    }
    // 2. hoofdstuk C (eigen magazine-opmaak)
    const magc = document.querySelector('.magc');
    if (magc) {
      let i = 0;
      for (const blok of magc.children) {
        if (blok.tagName === 'HEADER' || blok.classList.contains('magc-voetnoot')) continue;
        maakMarker(blok, 'c-omslag:' + i);
        i++;
      }
    }
    positioneer();
  }

  function maakMarker(blok, anker) {
    let m = markers.find((x) => x.blok === blok);
    if (m) {
      m.anker = anker; m.el.dataset.anker = anker;
      if (!document.contains(m.el)) laag().appendChild(m.el);
      bijwerkMarker(m); return;
    }
    const el = document.createElement('button');
    el.type = 'button';
    el.className = 'nt-knop';
    el.dataset.anker = anker;
    el.title = 'Notitie bij dit blok';
    laag().appendChild(el);
    m = { anker, blok, el };
    markers.push(m);
    bijwerkMarker(m);
    el.addEventListener('click', (e) => { e.stopPropagation(); openPopover(m); });
    blok.addEventListener('mouseenter', () => el.classList.add('nt-zicht'));
    blok.addEventListener('mouseleave', () => el.classList.remove('nt-zicht'));
    el.addEventListener('mouseenter', () => el.classList.add('nt-zicht'));
    el.addEventListener('mouseleave', () => el.classList.remove('nt-zicht'));
  }

  function bijwerkMarker(m) {
    m.el.classList.toggle('nt-heeft', !!notitieVoor(m.anker));
    m.el.textContent = notitieVoor(m.anker) ? '✎' : '+';
  }

  function positioneer() {
    // eerst alle metingen (één reflow), dan pas alle schrijfacties —
    // afwisselen van lezen/schrijven dwingt per marker een reflow af en
    // bevriest de pagina seconden op lange documenten
    const vw = document.documentElement.clientWidth;
    const sy = window.scrollY;
    const metingen = markers.map((m) => (document.contains(m.blok) ? m.blok.getBoundingClientRect() : null));
    markers.forEach((m, i) => {
      const r = metingen[i];
      if (!r || (r.width === 0 && r.height === 0)) { m.el.style.display = 'none'; return; }
      m.el.style.display = '';
      m.el.style.top = (r.top + sy + 2) + 'px';
      m.el.style.left = Math.min(r.right + 12, vw - 40) + 'px';
    });
  }

  let laagEl = null;
  function laag() {
    if (!laagEl || !document.contains(laagEl)) {
      laagEl = document.createElement('div');
      laagEl.className = 'nt-laag';
      document.body.appendChild(laagEl);
    }
    return laagEl;
  }

  /* ---------- popover ---------- */

  let pop = null, popAnker = null;

  function openPopover(m) {
    sluitPopover();
    popAnker = m.anker;
    const bestaand = notitieVoor(m.anker);
    pop = document.createElement('div');
    pop.className = 'nt-popover';
    pop.innerHTML =
      '<div class="nt-pop-kop">Notitie <span class="nt-pop-waar"></span></div>' +
      '<input class="nt-naam" type="text" placeholder="Uw naam (verplicht)" maxlength="80">' +
      '<textarea class="nt-tekst" rows="4" placeholder="Uw notitie bij dit blok…" maxlength="4000"></textarea>' +
      '<div class="nt-pop-rij">' +
      '<button type="button" class="nt-bewaar">bewaar</button>' +
      (bestaand ? '<button type="button" class="nt-wis">verwijder</button>' : '') +
      '<button type="button" class="nt-sluit">sluit</button>' +
      '</div>' +
      '<p class="nt-privacy"><strong>Vermeld uw naam</strong> — notities zonder naam kunnen we niet meenemen. Uw notitie is alleen zichtbaar voor u en voor het VIC.</p>';
    document.body.appendChild(pop);

    pop.querySelector('.nt-pop-waar').textContent = '— ' + hoofdstukTitel(m.anker.split(':')[0]);
    const naamEl = pop.querySelector('.nt-naam');
    const tekstEl = pop.querySelector('.nt-tekst');
    naamEl.value = (bestaand && bestaand.naam) || profiel.naam || '';
    tekstEl.value = (bestaand && bestaand.tekst) || '';

    const r = m.el.getBoundingClientRect();
    const links = Math.min(Math.max(12, r.left - 340), document.documentElement.clientWidth - 372);
    pop.style.left = links + 'px';
    pop.style.top = Math.min(r.bottom + 8, window.innerHeight - 290) + 'px';

    pop.querySelector('.nt-bewaar').addEventListener('click', () => {
      const naam = naamEl.value.trim();
      const tekst = tekstEl.value.trim();
      naamEl.classList.toggle('nt-fout', !naam);
      tekstEl.classList.toggle('nt-fout', !tekst);
      if (!naam || !tekst) return;
      profiel.naam = naam; schrijf(LS_PROFIEL, profiel);
      const nu = new Date().toISOString();
      const lijst = alleNotities();
      const idx = lijst.findIndex((n) => n.anker === m.anker);
      let notitie;
      if (idx >= 0) { notitie = { ...lijst[idx], naam, tekst, gewijzigd: nu }; lijst[idx] = notitie; }
      else {
        notitie = { id: uuid(), bezoekerId: profiel.id, naam, pagina: route().page, anker: m.anker, tekst, aangemaakt: nu, gewijzigd: nu };
        lijst.push(notitie);
      }
      bewaarNotities(lijst);
      syncBewaar(notitie);
      bijwerkMarker(m);
      sluitPopover();
    });
    const wis = pop.querySelector('.nt-wis');
    if (wis) wis.addEventListener('click', () => {
      bewaarNotities(alleNotities().filter((n) => n.anker !== m.anker));
      syncVerwijder(m.anker);
      bijwerkMarker(m);
      sluitPopover();
    });
    pop.querySelector('.nt-sluit').addEventListener('click', sluitPopover);
    (bestaand ? tekstEl : (profiel.naam ? tekstEl : naamEl)).focus();
  }

  function sluitPopover() { if (pop) { pop.remove(); pop = null; popAnker = null; } }
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { sluitPopover(); sluitPaneel(); } });
  document.addEventListener('click', (e) => {
    if (pop && !pop.contains(e.target) && !e.target.classList.contains('nt-knop')) sluitPopover();
  });

  /* ---------- widget + paneel ---------- */

  let widget = null, paneel = null;

  function werkWidgetBij() {
    const n = alleNotities().length;
    if (!widget || !document.contains(widget)) {
      widget = document.createElement('button');
      widget.type = 'button';
      widget.className = 'nt-widget';
      widget.addEventListener('click', () => (paneel && document.contains(paneel) ? sluitPaneel() : openPaneel()));
      document.body.appendChild(widget);
    }
    widget.textContent = '✎ mijn notities' + (n ? ' (' + n + ')' : '');
    widget.style.display = '';
  }

  function openPaneel() {
    sluitPaneel();
    const lijst = alleNotities();
    paneel = document.createElement('div');
    paneel.className = 'nt-paneel';
    const items = lijst.length
      ? lijst.map((nt) => {
          const d = document.createElement('div');
          d.className = 'nt-item';
          const kop = document.createElement('div'); kop.className = 'nt-item-kop';
          kop.textContent = hoofdstukTitel(nt.anker.split(':')[0]);
          const tx = document.createElement('p'); tx.textContent = nt.tekst;
          d.appendChild(kop); d.appendChild(tx);
          return d;
        })
      : [Object.assign(document.createElement('p'), { className: 'nt-leeg', textContent: 'Nog geen notities. Beweeg over een tekstblok en klik op de + in de marge.' })];
    const kop = document.createElement('div');
    kop.className = 'nt-paneel-kop';
    kop.textContent = 'Mijn notities' + (profiel.naam ? ' — ' + profiel.naam : '');
    paneel.appendChild(kop);
    const body = document.createElement('div'); body.className = 'nt-paneel-body';
    items.forEach((i) => body.appendChild(i));
    paneel.appendChild(body);
    const voet = document.createElement('div');
    voet.className = 'nt-paneel-voet';
    const dl = document.createElement('button'); dl.type = 'button'; dl.textContent = '⬇ bewaar als bestand';
    dl.addEventListener('click', downloadNotities);
    const adm = document.createElement('button'); adm.type = 'button'; adm.textContent = 'beheer (VIC)'; adm.className = 'nt-adm';
    adm.addEventListener('click', openAdmin);
    voet.appendChild(dl); voet.appendChild(adm);
    paneel.appendChild(voet);
    const priv = document.createElement('p');
    priv.className = 'nt-privacy';
    priv.textContent = 'Uw notities zijn alleen zichtbaar voor u en voor het VIC.';
    paneel.appendChild(priv);
    document.body.appendChild(paneel);
  }

  function sluitPaneel() { if (paneel) { paneel.remove(); paneel = null; } }

  function downloadNotities() {
    const lijst = alleNotities();
    const regels = [
      'Notities — VIC Veenweideboeren',
      'Van: ' + (profiel.naam || 'onbekend'),
      'Bewaard: ' + new Date().toLocaleString('nl-NL'),
      ''.padEnd(48, '—'), '',
    ];
    for (const nt of lijst) {
      regels.push('[' + hoofdstukTitel(nt.anker.split(':')[0]) + ' · blok ' + nt.anker.split(':').slice(1).join(':') + ']');
      regels.push(nt.tekst, '');
    }
    if (!lijst.length) regels.push('(geen notities)');
    const blob = new Blob([regels.join('\n')], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'notities-veenweideboeren.txt';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  }

  /* ---------- admin (demo) — achter wachtwoord ---------- */

  const ADMIN_WACHTWOORD = 'veenweide'; // terugval voor lokale preview zonder server
  let adminOntgrendeld = false;
  let adminServerSleutel = null;

  function openAdmin() {
    if (!adminOntgrendeld) { openAdminLogin(); return; }
    haalAdminNotities();
  }

  async function haalAdminNotities() {
    if (adminServerSleutel !== null) {
      try {
        const r = await fetch('/api/admin', { headers: { 'x-beheer-sleutel': adminServerSleutel } });
        if (r.ok) { toonAdmin(await r.json(), 'server'); return; }
      } catch (e) { /* val terug op lokaal */ }
    }
    toonAdmin(alleNotities(), 'lokaal');
  }

  function openAdminLogin() {
    const scrim = document.createElement('div');
    scrim.className = 'nt-admin-scrim';
    const p = document.createElement('div');
    p.className = 'nt-admin nt-admin-login';
    const kop = document.createElement('div'); kop.className = 'nt-paneel-kop';
    kop.textContent = 'Beheer — alleen voor het VIC';
    const uitleg = document.createElement('p'); uitleg.className = 'nt-leeg';
    uitleg.textContent = 'Deze pagina toont alle bezoekersnotities en is afgeschermd. Gebruik het beheerwachtwoord dat bij Vercel is ingesteld.';
    const veld = document.createElement('input');
    veld.type = 'password'; veld.placeholder = 'Wachtwoord'; veld.className = 'nt-admin-wachtwoord';
    const rij = document.createElement('div'); rij.className = 'nt-pop-rij';
    const ok = document.createElement('button'); ok.type = 'button'; ok.textContent = 'inloggen'; ok.className = 'nt-bewaar';
    const annuleer = document.createElement('button'); annuleer.type = 'button'; annuleer.textContent = 'annuleer'; annuleer.className = 'nt-sluit';
    const probeer = async () => {
      const poging = veld.value;
      // 1. echte controle bij de server (alle bezoekersnotities)
      try {
        const r = await fetch('/api/admin', { headers: { 'x-beheer-sleutel': poging } });
        if (r.ok) {
          adminOntgrendeld = true; adminServerSleutel = poging;
          scrim.remove(); toonAdmin(await r.json(), 'server'); return;
        }
        if (r.status === 401) { veld.classList.add('nt-fout'); veld.value = ''; veld.placeholder = 'Onjuist wachtwoord'; veld.focus(); return; }
      } catch (e) { /* geen server — lokale preview */ }
      // 2. terugval: lokale demo zonder server
      if (poging === ADMIN_WACHTWOORD) { adminOntgrendeld = true; scrim.remove(); toonAdmin(alleNotities(), 'lokaal'); }
      else { veld.classList.add('nt-fout'); veld.value = ''; veld.placeholder = 'Onjuist wachtwoord'; veld.focus(); }
    };
    ok.addEventListener('click', probeer);
    veld.addEventListener('keydown', (e) => { if (e.key === 'Enter') probeer(); });
    annuleer.addEventListener('click', () => scrim.remove());
    rij.appendChild(ok); rij.appendChild(annuleer);
    p.appendChild(kop); p.appendChild(uitleg); p.appendChild(veld); p.appendChild(rij);
    scrim.appendChild(p);
    scrim.addEventListener('click', (e) => { if (e.target === scrim) scrim.remove(); });
    document.body.appendChild(scrim);
    veld.focus();
  }

  function toonAdmin(lijst, bron) {
    const scrim = document.createElement('div');
    scrim.className = 'nt-admin-scrim';
    const p = document.createElement('div');
    p.className = 'nt-admin';
    const kop = document.createElement('div'); kop.className = 'nt-paneel-kop';
    kop.textContent = 'Beheer — alle notities';
    const uitleg = document.createElement('p');
    uitleg.className = 'nt-leeg';
    uitleg.textContent = bron === 'server'
      ? 'Alle bezoekersnotities uit de centrale database, gegroepeerd per hoofdstuk — nieuwste eerst.'
      : 'Lokale weergave (geen databaseverbinding): alleen de notities in deze browser.';
    p.appendChild(kop); p.appendChild(uitleg);
    const groepen = {};
    for (const nt of (lijst || [])) {
      const k = nt.anker.split(':')[0];
      (groepen[k] = groepen[k] || []).push(nt);
    }
    for (const [k, lijst] of Object.entries(groepen)) {
      const g = document.createElement('div'); g.className = 'nt-admin-groep';
      const gk = document.createElement('div'); gk.className = 'nt-item-kop'; gk.textContent = hoofdstukTitel(k);
      g.appendChild(gk);
      for (const nt of lijst) {
        const rij = document.createElement('div'); rij.className = 'nt-admin-rij';
        const wie = document.createElement('span'); wie.className = 'nt-wie';
        wie.textContent = nt.naam + ' · ' + new Date(nt.gewijzigd).toLocaleDateString('nl-NL') + ' · blok ' + nt.anker.split(':').slice(1).join(':');
        const tx = document.createElement('p'); tx.textContent = nt.tekst;
        rij.appendChild(wie); rij.appendChild(tx);
        g.appendChild(rij);
      }
      p.appendChild(g);
    }
    if (!Object.keys(groepen).length) {
      const leeg = document.createElement('p'); leeg.className = 'nt-leeg'; leeg.textContent = '(nog geen notities)';
      p.appendChild(leeg);
    }
    const sluit = document.createElement('button'); sluit.type = 'button'; sluit.textContent = 'sluit'; sluit.className = 'nt-admin-sluit';
    sluit.addEventListener('click', () => scrim.remove());
    p.appendChild(sluit);
    scrim.appendChild(p);
    scrim.addEventListener('click', (e) => { if (e.target === scrim) scrim.remove(); });
    document.body.appendChild(scrim);
  }

  /* ---------- her-stempelen bij DOM-wijzigingen ---------- */

  let timer = null;
  const observer = new MutationObserver((muts) => {
    if (muts.every((m) => m.target.closest && m.target.closest('.nt-laag,.nt-popover,.nt-paneel,.nt-admin-scrim,.nt-widget'))) return;
    clearTimeout(timer);
    timer = setTimeout(stempel, 250);
  });

  function start() {
    const root = document.getElementById('root') || document.body;
    observer.observe(root, { childList: true, subtree: true });
    window.addEventListener('resize', () => { clearTimeout(timer); timer = setTimeout(positioneer, 150); });
    window.addEventListener('load', () => setTimeout(stempel, 800));
    setTimeout(stempel, 1200);
    werkWidgetBij();
    syncOphalen();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
