# Veenweideboeren — site (prototype)

Statische site: geen build-stap nodig. `index.html` is het startpunt;
alles wat de site nodig heeft zit in deze map.

## Publiceren op Vercel (zonder terminal)

1. Ga naar https://vercel.com/new (log in met je bestaande account).
2. Kies rechts "…or deploy a project without Git" → sleep deze hele map
   (de map `vercel-site`, of de uitgepakte zip) in het uploadvak.
3. Projectnaam invullen (bijv. `veenweideboeren`) → Deploy.
4. Na ±30 seconden krijg je een URL: `https://veenweideboeren.vercel.app`.

## Publiceren via de Vercel CLI (met terminal)

    cd vercel-site
    npx vercel          # eerste keer: inloggen + vragen beantwoorden
    npx vercel --prod   # naar productie

## Afschermen voor de buitenwereld

Het is een interne conceptversie. Twee opties in het Vercel-dashboard
(project → Settings → Deployment Protection):

- "Vercel Authentication": alleen ingelogde teamleden zien de site (gratis).
- "Password Protection": één wachtwoord voor iedereen met de link (Pro-plan).

Deel anders simpelweg de URL alleen met de juiste mensen; de site is
niet vindbaar via zoekmachines zolang nergens naar gelinkt wordt.

## Database koppelen (Upstash Redis — zelfde als visie-op-noordeloos)

De notities-API staat al in de map (`api/notities.js` + `api/admin.js`,
zonder dependencies). Na de eerste deploy:

1. Open het project in het Vercel-dashboard → tab **Storage**.
2. Klik **Connect Store** → kies je bestaande **Upstash for Redis**-store
   (dezelfde die visie-op-noordeloos gebruikt) → koppel aan alle
   environments. Vercel zet dan zelf `UPSTASH_REDIS_REST_URL` en
   `UPSTASH_REDIS_REST_TOKEN` klaar.
3. Ga naar **Settings → Environment Variables** en voeg toe:
   `BEHEER_WACHTWOORD` = een zelfgekozen sterk wachtwoord (dit wordt het
   echte wachtwoord van "beheer (VIC)").
4. **Redeploy** (Deployments → ⋯ → Redeploy) zodat de variabelen actief zijn.

Alle sleutels in Redis krijgen prefix `vwb:` — de Noordeloos-data blijft
er volledig los van staan.

## Hoe de notities werken

- Bezoekers slaan notities op in hun eigen browser én (op de echte site)
  centraal in Redis. Bij terugkomst worden ze samengevoegd — nieuwste wint.
- Naam is verplicht; zonder naam wordt er niets opgeslagen.
- "beheer (VIC)" controleert het wachtwoord server-side en toont dan álle
  bezoekersnotities, per hoofdstuk, nieuwste eerst.
- Zonder databasekoppeling (bijv. lokaal openen) valt alles stil terug op
  browser-opslag; het demo-wachtwoord is dan `veenweide`.

## Wat dit prototype verder doet

- Elke verse paginalading begint op de startpagina.
- De rode banner "onder constructie" staat op de startpagina.

## E-maildigest (twee keer per dag)

`api/digest.js` mailt één keer per dag een overzicht van nieuwe en
gewijzigde notities. De tijd staat in `vercel.json` als cron-schema in
**UTC**: `0 10` = 12:00 Nederlandse zomertijd (in de winter 11:00).

**Let op — Vercel Hobby-plan:** een cron-job mag maar één keer per dag
draaien. Daarom staat er precies één entry in `vercel.json`. Voeg er geen
tweede toe zolang je op Hobby zit, anders faalt de hele deploy. Wil je
twee digests per dag, dan is een Pro-plan nodig.

Eenmalige setup:

1. Maak een gratis account op https://resend.com → API Keys → maak een
   sleutel aan.
2. In Vercel: Settings → Environment Variables, voeg toe:
   - `RESEND_API_KEY`    = de sleutel uit stap 1
   - `NOTIFICATIE_EMAIL` = jouw e-mailadres
3. Redeploy. Vercel activeert de cron-jobs automatisch (zichtbaar onder
   Settings → Cron Jobs).

Geen nieuwe notities = geen mail. Testen zonder te wachten: open
`https://<jouw-site>/api/digest` — met de header `x-beheer-sleutel:
<BEHEER_WACHTWOORD>` als je `CRON_SECRET` hebt ingesteld; zonder
`CRON_SECRET` werkt de URL direct.

Let op (Resend gratis): zolang je geen eigen domein verifieert, mailt
Resend alleen naar het adres waarmee je het Resend-account aanmaakte —
gebruik dat adres dus als `NOTIFICATIE_EMAIL`.

## Mappen

- `index.html`     — de hele site (één pagina, React via CDN)
- `api/`           — serverless functies: notities opslaan/ophalen + beheer
- `site/`          — inhoud (content-*.js) en componenten (v4-*.jsx/css)
- `assets/`        — logo, foto's, akte-illustraties
- `tokens/` + `styles.css` — VIC-huisstijl (kleuren, typografie)

Let op: deze map is de deploy-versie. De notities-serverkoppeling zit
alleen hier (niet in het wireframe in het ontwerpproject).
