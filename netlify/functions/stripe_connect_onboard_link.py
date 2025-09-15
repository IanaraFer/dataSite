import os
import json
import stripe

def handler(event, context):
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
        account_id = body.get("account_id")
        if not account_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing account_id."})
            }
        link = stripe.AccountLink.create(
            account=account_id,
            refresh_url="https://yourdomain.com/reauth",
            return_url="https://yourdomain.com/onboarded",
            type="account_onboarding"
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"url": link.url})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
