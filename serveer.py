# -*- coding: utf-8 -*-
"""De herziening lokaal serveren, in de vormgeving die het bestuur kent.

Gebruik: python3 serveer.py [poort]

Waarom niet gewoon `python3 -m http.server`: die stuurt geen cache-regels mee,
waardoor de browser oude bestanden blijft tonen na een herbouw. Dan lijkt de
herziening onveranderd terwijl ze het niet is. Hier gaat bij elk antwoord
`Cache-Control: no-store` mee, zodat verversen altijd de laatste stand geeft.

Daarnaast serveert deze server `/__stamp`: de nieuwste wijzigingstijd van de
gebouwde inhoud en de lezer. De pagina vraagt die elke seconde op en herlaadt
zichzelf zodra hij verandert (Tim, 19-8: geen Command-Shift-R meer). Op Vercel
bestaat dat pad niet, dus daar stopt de lus vanzelf.

Verder neemt deze server `POST /__redactie` aan. Dat is de knop uit de
redactiemodus in de lezer: hij stuurt de alinea's die met de hand zijn gewijzigd
hierheen, en die worden als leesbare markdown aan `feedback/redactie-<datum>.md`
toegevoegd. **Er wordt nooit in `content/` geschreven.** Dat is met opzet: zo kan
een wijziging van Tim niet botsen met een schrijfactie van een sessie, ongeacht
wie er op dat moment bezig is, en blijft de diff in `content/` exact tonen wat er
veranderde. Dat laatste eist `CLAUDE.md` en het gaat verloren als de browser
rechtstreeks in de bron schrijft.

En deze server zet in de pagina die hij uitlevert de vlag `VIC_HERZIENING`.
Daarop opent de lezer meteen op de visie in plaats van op het keuzescherm
(Tim, 19-8). Dezelfde `index.html` gaat ook naar Vercel, waar het bestuur wél
op de startpagina hoort te beginnen; die vlag komt daar niet langs, want zij
wordt hier bij het uitleveren toegevoegd en staat niet in het bestand. Zo is er
niets wat vóór publicatie met de hand omgezet moet worden.
"""
import datetime, functools, http.server, json, os, socket, socketserver, sys

# Wat een herbouw raakt: de gebouwde inhoud en de lezer zelf.
GEVOLGD = ('webapp/site/content-visie.js', 'webapp/site/content-programma.js',
           'webapp/site/content-toolbox.js', 'webapp/site/v4-visie.jsx',
           'webapp/site/v4-shared.jsx', 'webapp/site/document-styles.css',
           'webapp/index.html')

INDEX = 'webapp/index.html'
WACHTRIJ = 'feedback'
VLAG = '<script>window.VIC_HERZIENING = true;</script>\n'


def stempel():
    """De hoogste wijzigingstijd van de gevolgde bestanden."""
    tijden = [os.path.getmtime(p) for p in GEVOLGD if os.path.exists(p)]
    return f'{max(tijden):.3f}' if tijden else '0'


def schrijf_wachtrij(gegevens):
    """De wijzigingen als markdown aan het dagbestand toevoegen, en het pad
    teruggeven. Eén bestand per dag, zodat een sessie precies weet waar te kijken."""
    dag = datetime.date.today().isoformat()
    pad = os.path.join(WACHTRIJ, f'redactie-{dag}.md')
    nieuw = not os.path.exists(pad)
    klok = datetime.datetime.now().strftime('%H:%M')
    regels = []
    if nieuw:
        regels += [f'# Redactievoorstellen van {dag}', '',
                   '*Getypt in de redactiemodus van de lezer en hierheen gestuurd. Elk',
                   'blok geeft het hoofdstuk, de oude tekst en de nieuwe. Een sessie past',
                   'ze toe in `content/` en vinkt af; dit bestand is de wachtrij en niet',
                   'de bron.*', '']
    regels += [f'## {klok} — {len(gegevens.get("wijzigingen", []))} wijziging(en)', '']
    for w in gegevens.get('wijzigingen', []):
        exact = 'exact te vervangen' if w.get('exact') else 'voorstel met context (uit een partial of fiche)'
        regels += [f'- [ ] **{w.get("hoofdstuk", "?")}** · {exact}', '',
                   '  **was:**', '', '  > ' + (w.get('was') or '').replace('\n', ' '), '',
                   '  **wordt:**', '', '  > ' + (w.get('wordt') or '').replace('\n', ' '), '']
    with open(pad, 'a', encoding='utf-8') as f:
        f.write('\n'.join(regels) + '\n')
    return pad


class GeenCache(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path.split('?')[0] != '/__redactie':
            self.send_error(404)
            return
        try:
            lengte = int(self.headers.get('Content-Length') or 0)
            gegevens = json.loads(self.rfile.read(lengte) or b'{}')
            aantal = len(gegevens.get('wijzigingen', []))
            if not aantal:
                raise ValueError('geen wijzigingen meegestuurd')
            pad = schrijf_wachtrij(gegevens)
        except Exception as e:
            body = json.dumps({'ok': False, 'fout': str(e)}).encode()
            self.send_response(400)
        else:
            body = json.dumps({'ok': True, 'aantal': aantal, 'bestand': pad}).encode()
            self.send_response(200)
            print(f'{aantal} redactievoorstel(len) bijgeschreven in {pad}')
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        pad = self.path.split('?')[0]
        if pad == '/__stamp':
            body = stempel().encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if pad in ('/', '/index.html'):
            self.stuur_index()
            return
        super().do_GET()

    def stuur_index(self):
        """De pagina met de herzieningsvlag erin, vóór `</head>`."""
        try:
            html = open(INDEX, encoding='utf-8').read()
        except OSError:
            self.send_error(404, 'webapp/index.html niet gevonden')
            return
        body = html.replace('</head>', VLAG + '</head>', 1).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, *a):
        pass  # de logregels per bestand zeggen niets; stil is bruikbaarder


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    poort = int(sys.argv[1]) if len(sys.argv) > 1 else 18620
    handler = functools.partial(GeenCache, directory='webapp')
    with Server(('0.0.0.0', poort), handler) as httpd:
        print(f'De herziening staat klaar op poort {poort} '
              f'(ook via Tailscale, host {socket.gethostname()}).')
        print('Live herladen staat aan: de pagina ververst zichzelf na elke herbouw.')
        print('Redactiemodus staat klaar: wijzigingen komen in feedback/redactie-<datum>.md.')
        httpd.serve_forever()
