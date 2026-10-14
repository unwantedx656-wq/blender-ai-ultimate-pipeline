"""
Blender AI Ultimate Studio: Local Web Server
Provides a visual interface for engine selection, API configuration, and 3D preview.
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add repo root to sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.hybrid_3d_engine import Hybrid3DEngine

engine = Hybrid3DEngine()
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class StudioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self.send_json_response(engine.get_full_status())
        elif path == "/api/check-local":
            self.send_json_response(engine.check_trellis_status())
        elif path == "/api/check-blender":
            self.send_json_response(engine.check_blender_status())
        elif path == "/" or path == "/index.html":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        
        try:
            data = json.loads(body)
        except:
            data = {}

        if path == "/api/set-engine":
            target = data.get("engine", "meshy")
            res = engine.set_engine(target)
            self.send_json_response(res)
        elif path == "/api/set-key":
            key = data.get("api_key", "")
            res = engine.set_meshy_api_key(key)
            # Recheck status immediately
            res["status"] = engine.check_meshy_status()
            self.send_json_response(res)
        elif path == "/api/import-blender":
            glb_path = data.get("glb_path", "")
            res = engine.import_glb_to_blender(glb_path)
            self.send_json_response(res)
        else:
            self.send_response(404)
            self.end_headers()

    def send_json_response(self, data: dict, status_code: int = 200):
        resp = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(resp)

def run_server(port: int = 5050):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, StudioHandler)
    print(f"[*] Blender AI Ultimate Studio activo en: http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Deteniendo Studio Server...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5050
    run_server(port)
