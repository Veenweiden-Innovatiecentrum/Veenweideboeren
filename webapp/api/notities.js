// Notities-API — Upstash Redis via REST (geen dependencies).
// Koppel de bestaande Upstash Redis-store aan dit project (Storage → Connect),
// dan staan UPSTASH_REDIS_REST_URL en UPSTASH_REDIS_REST_TOKEN automatisch klaar.
// Alle sleutels hebben prefix "vwb:" zodat ze naast andere sites in dezelfde
// database kunnen bestaan (zoals visie-op-noordeloos).

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
    if (!REDIS_URL || !REDIS_TOKEN) {
      return res.status(500).json({ fout: 'Database niet gekoppeld: verbind de Upstash Redis-store met dit project (Storage → Connect).' });
    }

    // eigen notities ophalen
    if (req.method === 'GET') {
      const bezoeker = String(req.query.bezoeker || '');
      if (!bezoeker) return res.status(400).json({ fout: 'bezoeker ontbreekt' });
      const plat = (await redis(['HGETALL', 'vwb:nt:' + bezoeker])) || [];
      const uit = [];
      for (let i = 0; i < plat.length; i += 2) { try { uit.push(JSON.parse(plat[i + 1])); } catch (e) {} }
      return res.status(200).json(uit);
    }

    // notitie opslaan / bijwerken
    if (req.method === 'POST') {
      const n = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
      const { bezoekerId, naam, pagina, anker, tekst } = n;
      if (!bezoekerId || !naam || !anker || !tekst) return res.status(400).json({ fout: 'verplichte velden ontbreken (naam is verplicht)' });
      if (String(tekst).length > 4000 || String(naam).length > 80) return res.status(400).json({ fout: 'tekst of naam te lang' });
      const notitie = {
        id: String(n.id || (bezoekerId + ':' + anker)),
        bezoekerId: String(bezoekerId),
        naam: String(naam),
        pagina: String(pagina || ''),
        anker: String(anker),
        tekst: String(tekst),
        aangemaakt: String(n.aangemaakt || new Date().toISOString()),
        gewijzigd: new Date().toISOString(),
      };
      await redis(['HSET', 'vwb:nt:' + notitie.bezoekerId, notitie.anker, JSON.stringify(notitie)]);
      await redis(['SADD', 'vwb:nt:bezoekers', notitie.bezoekerId]);
      return res.status(200).json({ ok: true, gewijzigd: notitie.gewijzigd });
    }

    // notitie verwijderen
    if (req.method === 'DELETE') {
      const bezoeker = String(req.query.bezoeker || '');
      const anker = String(req.query.anker || '');
      if (!bezoeker || !anker) return res.status(400).json({ fout: 'bezoeker/anker ontbreekt' });
      await redis(['HDEL', 'vwb:nt:' + bezoeker, anker]);
      return res.status(200).json({ ok: true });
    }

    return res.status(405).json({ fout: 'methode niet toegestaan' });
  } catch (e) {
    return res.status(500).json({ fout: String((e && e.message) || e) });
  }
};
