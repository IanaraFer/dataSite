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
        name = body.get("name")
        description = body.get("description")
        price = body.get("price")
        currency = body.get("currency")
        account_id = body.get("account_id")
        if not all([name, description, price, currency, account_id]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required product fields."})
            }
        product = stripe.Product.create(
            name=name,
            description=description,
            default_price_data={
                "unit_amount": price,
                "currency": currency
            }
        )
        # In production, store mapping in DB
        return {
            "statusCode": 200,
            "body": json.dumps({"product_id": product.id, "price_id": product.default_price, "account_id": account_id})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
