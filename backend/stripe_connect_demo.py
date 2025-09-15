"""
Stripe Connect Demo Integration
- Onboard connected accounts (Express)
- Create products
- Display products/storefront
- Process destination charges with application fee
- Uses Stripe API version 2025-08-27.basil
"""

import os
import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Stripe API setup
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    raise RuntimeError("Stripe secret key missing. Set STRIPE_SECRET_KEY in your .env file.")
stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = "2025-08-27.basil"

app = FastAPI(title="Stripe Connect Demo", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for product/account mapping (replace with DB in production)
PRODUCT_ACCOUNT_MAP = {}

class AccountCreateRequest(BaseModel):
    email: str
    business_name: str

@app.post("/api/connect/create-account")
def create_connected_account(req: AccountCreateRequest):
    """
    Create a Stripe connected account (Express) with platform responsible for fees/losses.
    """
    try:
        account = stripe.Account.create(
            controller={
                "fees": {"payer": "application"},
                "losses": {"payments": "application"},
                "stripe_dashboard": {"type": "express"}
            },
            email=req.email,
            business_profile={"name": req.business_name}
        )
        return {"account_id": account.id, "dashboard": account.controller["stripe_dashboard"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")

@app.get("/api/connect/account-status/{account_id}")
def get_account_status(account_id: str):
    """
    Retrieve the status of a connected account from Stripe.
    """
    try:
        account = stripe.Account.retrieve(account_id)
        return {"id": account.id, "details_submitted": account.details_submitted, "charges_enabled": account.charges_enabled, "payouts_enabled": account.payouts_enabled}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")

@app.post("/api/connect/onboard-link")
def create_onboard_link(account_id: str):
    """
    Create an onboarding link for a connected account.
    """
    try:
        link = stripe.AccountLink.create(
            account=account_id,
            refresh_url="https://yourdomain.com/reauth",
            return_url="https://yourdomain.com/onboarded",
            type="account_onboarding"
        )
        return {"url": link.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")

class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: int
    currency: str
    account_id: str

@app.post("/api/products/create")
def create_product(req: ProductCreateRequest):
    """
    Create a product at the platform level and map to a connected account.
    """
    try:
        product = stripe.Product.create(
            name=req.name,
            description=req.description,
            default_price_data={
                "unit_amount": req.price,
                "currency": req.currency
            }
        )
        # Store mapping in memory (replace with DB in production)
        PRODUCT_ACCOUNT_MAP[product.id] = req.account_id
        return {"product_id": product.id, "price_id": product.default_price, "account_id": req.account_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")

@app.get("/api/products/list")
def list_products():
    """
    List all products and their connected account mapping.
    """
    products = stripe.Product.list(limit=20)
    result = []
    for prod in products.data:
        result.append({
            "id": prod.id,
            "name": prod.name,
            "description": prod.description,
            "price_id": prod.default_price,
            "account_id": PRODUCT_ACCOUNT_MAP.get(prod.id, "Not mapped")
        })
    return result

class CheckoutRequest(BaseModel):
    product_id: str
    quantity: int

@app.post("/api/storefront/checkout")
def create_checkout_session(req: CheckoutRequest):
    """
    Create a Stripe Checkout session for a product, using destination charge and application fee.
    """
    account_id = PRODUCT_ACCOUNT_MAP.get(req.product_id)
    if not account_id:
        raise HTTPException(status_code=400, detail="Product not mapped to a connected account.")
    try:
        product = stripe.Product.retrieve(req.product_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                "price": product.default_price,
                "quantity": req.quantity
            }],
            payment_intent_data={
                "application_fee_amount": 123,  # Set your fee here
                "transfer_data": {"destination": account_id}
            },
            mode="payment",
            success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/cancel"
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")

@app.get("/storefront", response_class=HTMLResponse)
def storefront():
    """
    Simple HTML storefront to display products and allow purchase.
    """
    products = stripe.Product.list(limit=20)
    html = """
    <html><head><title>Storefront</title><style>
    body { font-family: Arial, sans-serif; background: #f8f9fa; }
    .product { border: 1px solid #ddd; padding: 16px; margin: 16px; background: #fff; border-radius: 8px; }
    .btn { background: #007bff; color: #fff; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }
    </style></head><body>
    <h2>Storefront</h2>
    <div>"""
    for prod in products.data:
        html += f'<div class="product"><h3>{prod.name}</h3><p>{prod.description}</p>'
        html += f'<form action="/api/storefront/checkout" method="post"><input type="hidden" name="product_id" value="{prod.id}">'\
                '<input type="number" name="quantity" value="1" min="1" style="width:60px;">'
        html += f'<button class="btn" type="submit">Buy</button></form>'
        html += f'<p>Connected Account: {PRODUCT_ACCOUNT_MAP.get(prod.id, "Not mapped")}</p></div>'
    html += "</div></body></html>"
    return HTMLResponse(content=html)

# To run: uvicorn stripe_connect_demo:app --reload
