# -*- coding: utf-8 -*-
"""Anatole 面板 · 轻量静态服务(服务器自带 Python,无需依赖/docker)。
默认绑 127.0.0.1:8090(私有,走 SSH 隧道访问);
设 ANATOLE_BIND=0.0.0.0 + ANATOLE_USER/ANATOLE_PASS 可公网+基础鉴权(需自行加 TLS)。
"""
import http.server, socketserver, os, base64

DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("ANATOLE_PORT", "8090"))
BIND = os.environ.get("ANATOLE_BIND", "127.0.0.1")
USER = os.environ.get("ANATOLE_USER", "")
PASS = os.environ.get("ANATOLE_PASS", "")
AUTH = ("Basic " + base64.b64encode(f"{USER}:{PASS}".encode()).decode()) if USER and PASS else None
HOME = "panel_full.html"


class H(http.server.SimpleHTTPRequestHandler):
    def _auth_ok(self):
        if not AUTH:
            return True
        if self.headers.get("Authorization") == AUTH:
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Anatole"')
        self.end_headers()
        return False

    def do_GET(self):
        if not self._auth_ok():
            return
        if self.path in ("/", "/index.html"):
            self.path = "/" + HOME
        return super().do_GET()

    def log_message(self, *a):
        pass


os.chdir(DIR)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer((BIND, PORT), H) as httpd:
    print(f"Anatole serving http://{BIND}:{PORT}  (home={HOME}, auth={'on' if AUTH else 'off'})")
    httpd.serve_forever()
