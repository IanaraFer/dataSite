from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "AnalyticaCore AI API",
            "status": "healthy",
            "version": "1.0.0"
        }
        self.wfile.write(json.dumps(response).encode())
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Get the path
        path = self.path
        
        if path == '/api/contact':
            response = {
                "message": "Thank you! We'll contact you within 24 hours.",
                "status": "success"
            }
        elif path == '/api/upload':
            response = {
                "message": "File upload received",
                "status": "success",
                "analysis": {
                    "total_records": 1000,
                    "revenue_trend": "📈 +15% growth",
                    "top_customer": "ABC Corp",
                    "insights": [
                        "Revenue increased 15% this quarter",
                        "Customer retention rate: 85%",
                        "Top performing product: Analytics Pro"
                    ]
                }
            }
        else:
            response = {
                "message": "API endpoint not found",
                "status": "error"
            }
        
        self.wfile.write(json.dumps(response).encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
