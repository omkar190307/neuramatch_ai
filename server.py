"""
NeuraMatch - AI Recommendation Engine (Web Server)
DecodeLabs | AI Project 3

HOW TO RUN IN VS CODE:
  1. Open terminal  (Ctrl + `)
  2. Run:  python server.py
  3. Browser opens at http://localhost:8080
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

sys.stdout.reconfigure(encoding='utf-8')

PORT      = 8080
HOST      = "localhost"
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"  [GET] {self.path}")

def open_browser():
    time.sleep(0.8)
    webbrowser.open(f"http://{HOST}:{PORT}")

def main():
    os.chdir(DIRECTORY)
    print("\n" + "=" * 52)
    print("   NeuraMatch - AI Recommendation Engine")
    print("   DecodeLabs | AI Project 3")
    print("=" * 52)
    print(f"\n  [OK]  Server running at http://{HOST}:{PORT}")
    print(f"  [DIR] {DIRECTORY}")
    print("\n  Press Ctrl+C to stop\n")
    print("-" * 52)
    threading.Thread(target=open_browser, daemon=True).start()
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  [STOP] Server stopped.\n")

if __name__ == "__main__":
    main()
