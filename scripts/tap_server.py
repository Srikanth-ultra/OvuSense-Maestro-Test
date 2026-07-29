#!/usr/bin/env python3
"""HTTP server that executes adb shell input tap for Maestro tests.

Maestro's tapOn/swipe touch injection doesn't work at the Settings tab
coordinates on the CI emulator, but adb shell input tap does. This server
bridges the gap by exposing adb tap as an HTTP endpoint that Maestro's
runScript JavaScript can call via http.get().
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import time
import sys


class TapHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if '/tap_settings' in self.path:
            # Tap the Settings tab in the bottom navigation bar
            # Coordinates: center of navigation_settings [864,2127][1080,2274]
            subprocess.run(['adb', 'shell', 'input', 'tap', '972', '2200'])
            time.sleep(1)  # Wait for navigation animation
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        elif '/tap' in self.path:
            # Generic tap: /tap?x=100&y=200
            from urllib.parse import urlparse, parse_qs
            params = parse_qs(urlparse(self.path).query)
            x = params.get('x', ['540'])[0]
            y = params.get('y', ['1200'])[0]
            subprocess.run(['adb', 'shell', 'input', 'tap', x, y])
            time.sleep(0.5)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        elif '/health' in self.path:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress per-request logs to keep CI output clean
        pass


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8089
    server = HTTPServer(('0.0.0.0', port), TapHandler)
    print(f'Tap server listening on port {port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
