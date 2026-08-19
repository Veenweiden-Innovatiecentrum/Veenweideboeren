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
"""
import functools, http.server, os, socket, socketserver, sys

# Wat een herbouw raakt: de gebouwde inhoud en de lezer zelf.
GEVOLGD = ('webapp/site/content-visie.js', 'webapp/site/content-programma.js',
           'webapp/site/content-toolbox.js', 'webapp/site/v4-visie.jsx',
           'webapp/site/v4-shared.jsx', 'webapp/site/document-styles.css',
           'webapp/index.html')


def stempel():
    """De hoogste wijzigingstijd van de gevolgde bestanden."""
    tijden = [os.path.getmtime(p) for p in GEVOLGD if os.path.exists(p)]
    return f'{max(tijden):.3f}' if tijden else '0'


class GeenCache(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/__stamp':
            body = stempel().encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

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
        httpd.serve_forever()
