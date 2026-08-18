// Digest-mail — wordt twee keer per dag aangeroepen door Vercel Cron
// (zie vercel.json). Verzamelt alle notities die sinds de vorige digest
// zijn toegevoegd of gewijzigd en mailt ze in één overzicht via Resend.
//
// Benodigde environment-variabelen:
//   RESEND_API_KEY     — API-sleutel van resend.com (gratis tot 100 mails/dag)
//   NOTIFICATIE_EMAIL  — het adres dat de digest ontvangt
//   EMAIL_VAN          — (optioneel) afzender; standaard onboarding@resend.dev
//   CRON_SECRET        — (aanbevolen) Vercel stuurt deze automatisch mee,
//                        zodat niemand anders de digest kan afdwingen

const REDIS_URL = process.env.UPSTASH_REDIS_REST_URL || process.env.KV_REST_API_URL;
const REDIS_TOKEN = process.env.UPSTASH_REDIS_REST_TOKEN || process.env.KV_REST_API_TOKEN;

async function redis(cmd) {
  const r = await fetch(REDIS_URL, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + REDIS_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(cmd),
  });
  if (!r.ok) throw new Error('database antwoordde ' + r.status);
  return (await r.json()).result;
}

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

module.exports = async (req, res) => {
  try {
    // toegang: Vercel Cron (CRON_SECRET) of de beheerder (handmatig testen)
    if (process.env.CRON_SECRET) {
      const auth = req.headers['authorization'] || '';
      const beheer = req.headers['x-beheer-sleutel'] || '';
      if (auth !== 'Bearer ' + process.env.CRON_SECRET && (!process.env.BEHEER_WACHTWOORD || beheer !== process.env.BEHEER_WACHTWOORD)) {
        return res.status(401).json({ fout: 'geen toegang' });
      }
    }
    if (!REDIS_URL || !REDIS_TOKEN) return res.status(500).json({ fout: 'Database niet gekoppeld (Storage → Connect).' });
    if (!process.env.RESEND_API_KEY || !process.env.NOTIFICATIE_EMAIL) {
      return res.status(500).json({ fout: 'RESEND_API_KEY of NOTIFICATIE_EMAIL niet ingesteld (Settings → Environment Variables).' });
    }

    const laatst = (await redis(['GET', 'vwb:nt:digest-laatst'])) || '1970-01-01T00:00:00.000Z';
    const bezoekers = (await redis(['SMEMBERS', 'vwb:nt:bezoekers'])) || [];
    const nieuw = [];
    for (const b of bezoekers) {
      const plat = (await redis(['HGETALL', 'vwb:nt:' + b])) || [];
      for (let i = 0; i < plat.length; i += 2) {
        try {
          const n = JSON.parse(plat[i + 1]);
          if (n.gewijzigd > laatst) nieuw.push(n);
        } catch (e) {}
      }
    }
    const nu = new Date().toISOString();

    if (!nieuw.length) {
      await redis(['SET', 'vwb:nt:digest-laatst', nu]);
      return res.status(200).json({ ok: true, verzonden: 0, melding: 'geen nieuwe notities — geen mail verstuurd' });
    }

    nieuw.sort((a, b) => (a.anker < b.anker ? -1 : 1));
    const regels = nieuw.map((n) =>
      '<p style="margin:0 0 16px;line-height:1.5">' +
      '<strong>' + esc(n.naam) + '</strong>' +
      ' &middot; ' + esc(n.pagina || '') + ' / ' + esc(n.anker) +
      ' &middot; ' + new Date(n.gewijzigd).toLocaleString('nl-NL', { timeZone: 'Europe/Amsterdam' }) +
      '<br>' + esc(n.tekst) + '</p>'
    ).join('');

    const mail = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.EMAIL_VAN || 'Veenweideboeren Visie <onboarding@resend.dev>',
        to: [process.env.NOTIFICATIE_EMAIL],
        subject: nieuw.length + ' nieuwe notitie' + (nieuw.length === 1 ? '' : 's') + ' — Veenweideboeren Visie',
        html:
          '<div style="font-family:sans-serif;max-width:640px">' +
          '<h2 style="color:#1d3176;margin:0 0 6px">Veenweideboeren Visie — notitie-digest</h2>' +
          '<p style="color:#6b6f6a;margin:0 0 20px">' + nieuw.length + ' nieuwe of gewijzigde notitie' + (nieuw.length === 1 ? '' : 's') + ' sinds de vorige digest.</p>' +
          regels +
          '<p style="color:#6b6f6a;font-size:12px;margin-top:24px">Volledig overzicht: open de site &rarr; &#9998; mijn notities &rarr; beheer (VIC).</p>' +
          '</div>',
      }),
    });
    if (!mail.ok) throw new Error('Resend antwoordde ' + mail.status + ': ' + (await mail.text()).slice(0, 200));

    await redis(['SET', 'vwb:nt:digest-laatst', nu]);
    return res.status(200).json({ ok: true, verzonden: nieuw.length });
  } catch (e) {
    return res.status(500).json({ fout: String((e && e.message) || e) });
  }
};
