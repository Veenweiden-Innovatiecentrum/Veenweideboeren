# -*- coding: utf-8 -*-
"""De herziening lokaal serveren, in de vormgeving die het bestuur kent.

Gebruik: python3 serveer.py [poort]

Waarom niet gewoon `python3 -m http.server`: die stuurt geen cache-regels mee,
waardoor de browser oude bestanden blijft tonen na een herbouw. Dan lijkt de
herziening onveranderd terwijl ze het niet is. Hier gaat bij elk antwoord
`Cache-Control: no-store` mee, zodat verversen altijd de laatste stand geeft.
"""
import functools, http.server, socket, socketserver, sys


class GeenCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    poort = int(sys.argv[1]) if len(sys.argv) > 1 else 18620
    handler = functools.partial(GeenCache, directory='webapp')
    with Server(('0.0.0.0', poort), handler) as httpd:
        print(f'De herziening staat klaar op poort {poort} '
              f'(ook via Tailscale, host {socket.gethostname()}).')
        httpd.serve_forever()
