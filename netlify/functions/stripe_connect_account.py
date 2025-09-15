import os
import json
import stripe

def handler(event, context):
    # Load Stripe secret key from Netlify environment variables
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
    if not STRIPE_SECRET_KEY:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Stripe secret key missing. Set STRIPE_SECRET_KEY in Netlify environment variables."})
        }
    stripe.api_key = STRIPE_SECRET_KEY
    stripe.api_version = "2025-08-27.basil"

    try:
        body = json.loads(event["body"])
        email = body.get("email")
        business_name = body.get("business_name")
        if not email or not business_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing email or business_name."})
            }
        account = stripe.Account.create(
            controller={
                "fees": {"payer": "application"},
                "losses": {"payments": "application"},
                "stripe_dashboard": {"type": "express"}
            },
            email=email,
            business_profile={"name": business_name}
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"account_id": account.id, "dashboard": account.controller["stripe_dashboard"]})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
