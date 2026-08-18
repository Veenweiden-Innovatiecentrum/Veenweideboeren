// Beheer-API — geeft ALLE bezoekersnotities terug, alleen met het juiste
// wachtwoord. Stel in Vercel de environment-variabele BEHEER_WACHTWOORD in
// (Settings → Environment Variables) en redeploy.

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

module.exports = async (req, res) => {
  try {
    if (!process.env.BEHEER_WACHTWOORD) {
      return res.status(500).json({ fout: 'BEHEER_WACHTWOORD is nog niet ingesteld bij Vercel (Settings → Environment Variables).' });
    }
    const sleutel = req.headers['x-beheer-sleutel'] || String(req.query.key || '');
    if (sleutel !== process.env.BEHEER_WACHTWOORD) {
      return res.status(401).json({ fout: 'onjuist wachtwoord' });
    }
    if (!REDIS_URL || !REDIS_TOKEN) {
      return res.status(500).json({ fout: 'Database niet gekoppeld (Storage → Connect).' });
    }
    const bezoekers = (await redis(['SMEMBERS', 'vwb:nt:bezoekers'])) || [];
    const alles = [];
    for (const b of bezoekers) {
      const plat = (await redis(['HGETALL', 'vwb:nt:' + b])) || [];
      for (let i = 0; i < plat.length; i += 2) { try { alles.push(JSON.parse(plat[i + 1])); } catch (e) {} }
    }
    alles.sort((a, b) => (a.gewijzigd < b.gewijzigd ? 1 : -1));
    return res.status(200).json(alles);
  } catch (e) {
    return res.status(500).json({ fout: String((e && e.message) || e) });
  }
};
