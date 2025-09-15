<<<<<<< HEAD
@app.route("/api/payment/subscribe", methods=["POST"])
def payment_subscribe():
    try:
        data = request.get_json()
        plan_name = data.get("plan", "Starter Plan")
        price = data.get("price", 199)
        email = data.get("email")
        # Map plan name to Stripe price ID
        price_ids = {
            "Starter Plan": "price_1S2Ne8EPS0ev8tkiBKZzV4pS",      # €199
            "Professional Plan": "price_1S2NfWEPS0ev8tkiwao10uJ0", # €399
            "Enterprise Plan": "price_1S2NgSEPS0ev8tkiRuu9Xbtb"    # €799
        }
        price_id = price_ids.get(plan_name, "price_1S2Ne8EPS0ev8tkiBKZzV4pS")

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            customer_email=email,
            success_url="https://analyticacoreai.netlify.app/success.html",
            cancel_url="https://analyticacoreai.netlify.app/pricing.html",
        )
        return jsonify({"success": True, "checkout_url": checkout_session.url})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import stripe
import os
=======
from http.server import BaseHTTPRequestHandler
>>>>>>> 3a98e9729a50088f85adee2c30f3575fc7a7132d
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

<<<<<<< HEAD
@app.route("/api/contact", methods=["POST"])
def handle_contact():
    try:
        data = request.get_json()
        name = data.get('name', 'No Name')
        email = data.get('email', 'No Email')
        message = data.get('message', '')

        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        smtp_server = "smtp.office365.com"
        smtp_port = 587
        username = "information@analyticacoreai.ie"
        password = "Maiaemolly22"  # Replace with your actual password or use environment variable
        recipient_email = "information@analyticacoreai.ie"

        subject = f"New Analysis/Orcamento Request from {name}"
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, recipient_email, msg.as_string())

        return jsonify({"message": "Thank you! Your request has been sent and you will be contacted soon."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
=======
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
>>>>>>> 3a98e9729a50088f85adee2c30f3575fc7a7132d
