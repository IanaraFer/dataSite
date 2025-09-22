from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        self._set_headers(200)
        response = {
            "message": "AnalyticaCore AI API",
            "status": "healthy",
            "version": "1.0.0"
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        # Read body (unused for mock endpoints)
        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except Exception:
            content_length = 0
        _ = self.rfile.read(content_length) if content_length > 0 else b''

        path = self.path

        if path == '/api/contact':
            self._set_headers(200)
            response = {"message": "Thank you! We'll contact you within 24 hours.", "status": "success"}
            self.wfile.write(json.dumps(response).encode())
            return

        if path == '/api/upload':
            self._set_headers(200)
            response = {"message": "File upload received", "status": "success"}
            self.wfile.write(json.dumps(response).encode())
            return

        # Not found
        self._set_headers(404)
        self.wfile.write(json.dumps({"message": "API endpoint not found", "status": "error"}).encode())
