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
        product_id = body.get("product_id")
        quantity = body.get("quantity", 1)
        account_id = body.get("account_id")
        if not all([product_id, account_id]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing product_id or account_id."})
            }
        product = stripe.Product.retrieve(product_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                "price": product.default_price,
                "quantity": quantity
            }],
            payment_intent_data={
                "application_fee_amount": 123,  # Set your fee here
                "transfer_data": {"destination": account_id}
            },
            mode="payment",
            success_url="https://yourdomain.com/thankyou.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/cancel"
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"checkout_url": session.url})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
