from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import stripe
import os
import json

app = Flask(__name__)
CORS(app)

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_51234567890")

@app.route("/api/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.get_json()
        price_id = data.get("price_id")
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url="https://analyticacoreai.netlify.app/success.html",
            cancel_url="https://analyticacoreai.netlify.app/pricing.html",
        )
        return jsonify({"url": checkout_session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/upload", methods=["POST"])
def handle_upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Process file (simplified demo)
        analysis_result = {
            "filename": file.filename,
            "size": len(file.read()),
            "analysis": {
                "total_records": 1000,
                "revenue_trend": "?? +15% growth",
                "top_customer": "ABC Corp",
                "insights": [
                    "Revenue increased 15% this quarter",
                    "Customer retention rate: 85%",
                    "Top performing product: Analytics Pro"
                ]
            }
        }
        
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/contact", methods=["POST"])
def handle_contact():
    try:
        data = request.get_json()
        # Send email (simplified - in production use SendGrid)
        return jsonify({"message": "Thank you! We'll contact you within 24 hours."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
