from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse


def _json_response(handler: BaseHTTPRequestHandler, status_code: int, payload: dict):
    handler.send_response(status_code)
    handler.send_header('Content-type', 'application/json')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.end_headers()
    handler.wfile.write(json.dumps(payload).encode('utf-8'))


def _read_request_body(handler: BaseHTTPRequestHandler) -> bytes:
    content_length = handler.headers.get('Content-Length')
    if content_length is None:
        return b''
    try:
        length = int(content_length)
    except ValueError:
        length = 0
    if length <= 0:
        return b''
    return handler.rfile.read(length)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ('/api', '/api/', '/api/health'):
            return _json_response(self, 200, {
                "message": "AnalyticaCore AI API",
                "status": "healthy",
                "version": "1.0.0"
            })

        if path == '/api/email/test':
            return _json_response(self, 200, {"status": "ok", "message": "Email service reachable (simulated)"})

        # Unknown GET endpoint
        return _json_response(self, 404, {"error": "Not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        raw_body = _read_request_body(self)
        content_type = self.headers.get('Content-Type', '')

        # Best-effort JSON parse
        body = {}
        if 'application/json' in content_type and raw_body:
            try:
                body = json.loads(raw_body.decode('utf-8'))
            except Exception:
                body = {}

        # Contact form (simple ack)
        if path == '/api/contact':
            name = body.get('name') if isinstance(body, dict) else None
            return _json_response(self, 200, {
                "status": "success",
                "message": f"Thanks {name or 'there'}! We'll contact you within 24 hours."
            })

        # File upload endpoint used by free trial form
        if path == '/api/free_trial_upload':
            # We do not persist files here; just acknowledge receipt
            return _json_response(self, 200, {
                "status": "received",
                "message": "Free trial submission received",
                "analysis_eta_minutes": 15
            })

        # One-time analysis request
        if path == '/api/one-time-analysis':
            return _json_response(self, 200, {
                "status": "queued",
                "job_id": "job_simulated_123",
                "message": "Your analysis request has been queued"
            })

        # Stripe Checkout via price data (preferred in website/working-payment.html)
        if path in ('/api/create-checkout-session', '/api/create-subscription'):
            # Attempt real Stripe checkout if configured; otherwise simulate
            stripe_secret = os.getenv('STRIPE_SECRET_KEY')
            if stripe_secret:
                try:
                    import stripe  # type: ignore
                    stripe.api_key = stripe_secret

                    price_data = (body or {}).get('price_data')
                    mode = (body or {}).get('mode', 'subscription')
                    success_url = (body or {}).get('success_url') or f"{self.headers.get('Origin') or ''}/success.html"
                    cancel_url = (body or {}).get('cancel_url') or f"{self.headers.get('Origin') or ''}/pricing.html"

                    if price_data:
                        session = stripe.checkout.Session.create(
                            mode=mode,
                            payment_method_types=['card'],
                            line_items=[{ 'price_data': price_data, 'quantity': 1 }],
                            success_url=success_url,
                            cancel_url=cancel_url,
                        )
                    else:
                        # Fallback expects price_id on body
                        price_id = (body or {}).get('price_id')
                        if not price_id:
                            return _json_response(self, 400, {"error": "Missing price_data or price_id"})
                        session = stripe.checkout.Session.create(
                            mode=mode,
                            payment_method_types=['card'],
                            line_items=[{ 'price': price_id, 'quantity': 1 }],
                            success_url=success_url,
                            cancel_url=cancel_url,
                        )
                    return _json_response(self, 200, {"id": session.id, "url": session.url})
                except Exception as e:
                    return _json_response(self, 500, {"error": f"Stripe error: {str(e)}"})

            # Simulated success (no Stripe configured)
            return _json_response(self, 200, {
                "id": "cs_test_simulated_123",
                "url": "https://checkout.stripe.com/test/sessions/cs_test_simulated_123",
                "requires_action": False,
                "customer_id": "cus_test_123"
            })

        # Stripe Connect Checkout (subscribe.html)
        if path == '/api/stripe_connect_checkout':
            # Simulate a connected account checkout link
            return _json_response(self, 200, {
                "checkout_url": "https://checkout.stripe.com/test/connect/cs_test_simulated_abc"
            })

        # Customer details placeholder (dashboard)
        if path.startswith('/api/customer/'):
            customer_id = path.rsplit('/', 1)[-1]
            return _json_response(self, 200, {
                "customer_id": customer_id,
                "email": "customer@example.com",
                "plan": "professional",
                "status": "active"
            })

        # Upload dataset placeholder (dashboard)
        if path == '/api/upload-dataset':
            return _json_response(self, 200, {
                "status": "uploaded",
                "rows": 1234,
                "message": "Dataset received"
            })

        # Unknown POST endpoint
        return _json_response(self, 404, {"error": "Not found"})
