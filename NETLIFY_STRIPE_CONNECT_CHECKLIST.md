# Netlify Stripe Connect Deployment Checklist

## 1. Prepare Your Project
- Ensure your backend Netlify Functions are in `netlify/functions/`
- Functions included:
  - `stripe_connect_account.py` (create connected accounts)
  - `stripe_connect_onboard_link.py` (onboarding links)
  - `stripe_connect_product.py` (create products)
  - `stripe_connect_checkout.py` (checkout)

## 2. Set Environment Variables in Netlify
- Go to Netlify dashboard → Site settings → Environment variables
- Add:
  - `STRIPE_SECRET_KEY=sk_live_...` (your Stripe secret key)

## 3. Deploy to Netlify
- Push your code to GitHub (if not already)
- Connect your repository to Netlify
- Netlify will auto-detect and deploy your functions

## 4. Test Your Endpoints
- Netlify Functions are available at:
  - `/.netlify/functions/stripe_connect_account`
  - `/.netlify/functions/stripe_connect_onboard_link`
  - `/.netlify/functions/stripe_connect_product`
  - `/.netlify/functions/stripe_connect_checkout`
- Use Postman or your frontend to test each endpoint

## 5. Update Frontend
- Update your frontend code to call the Netlify Function endpoints
- Example (using fetch):
```js
fetch('/.netlify/functions/stripe_connect_account', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, business_name })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 6. Go Live
- Once tested, your Stripe Connect integration is live and ready for users!

---

# Sample Frontend Code

## Create Connected Account
```html
<form id="create-account-form">
  <input type="email" id="email" placeholder="Email" required />
  <input type="text" id="business_name" placeholder="Business Name" required />
  <button type="submit">Create Connected Account</button>
</form>
<script>
document.getElementById('create-account-form').onsubmit = async function(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const business_name = document.getElementById('business_name').value;
  const res = await fetch('/.netlify/functions/stripe_connect_account', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, business_name })
  });
  const data = await res.json();
  alert('Account ID: ' + data.account_id);
};
</script>
```

## Onboard Connected Account
```html
<form id="onboard-link-form">
  <input type="text" id="account_id" placeholder="Account ID" required />
  <button type="submit">Get Onboarding Link</button>
</form>
<script>
document.getElementById('onboard-link-form').onsubmit = async function(e) {
  e.preventDefault();
  const account_id = document.getElementById('account_id').value;
  const res = await fetch('/.netlify/functions/stripe_connect_onboard_link', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ account_id })
  });
  const data = await res.json();
  window.open(data.url, '_blank');
};
</script>
```

## Create Product
```html
<form id="create-product-form">
  <input type="text" id="name" placeholder="Product Name" required />
  <input type="text" id="description" placeholder="Description" required />
  <input type="number" id="price" placeholder="Price (cents)" required />
  <input type="text" id="currency" placeholder="Currency (e.g. eur)" required />
  <input type="text" id="account_id_prod" placeholder="Account ID" required />
  <button type="submit">Create Product</button>
</form>
<script>
document.getElementById('create-product-form').onsubmit = async function(e) {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const description = document.getElementById('description').value;
  const price = parseInt(document.getElementById('price').value);
  const currency = document.getElementById('currency').value;
  const account_id = document.getElementById('account_id_prod').value;
  const res = await fetch('/.netlify/functions/stripe_connect_product', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description, price, currency, account_id })
  });
  const data = await res.json();
  alert('Product ID: ' + data.product_id);
};
</script>
```

## Checkout
```html
<form id="checkout-form">
  <input type="text" id="product_id" placeholder="Product ID" required />
  <input type="number" id="quantity" placeholder="Quantity" value="1" required />
  <input type="text" id="account_id_checkout" placeholder="Account ID" required />
  <button type="submit">Checkout</button>
</form>
<script>
document.getElementById('checkout-form').onsubmit = async function(e) {
  e.preventDefault();
  const product_id = document.getElementById('product_id').value;
  const quantity = parseInt(document.getElementById('quantity').value);
  const account_id = document.getElementById('account_id_checkout').value;
  const res = await fetch('/.netlify/functions/stripe_connect_checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id, quantity, account_id })
  });
  const data = await res.json();
  window.open(data.checkout_url, '_blank');
};
</script>
```

---

You are now ready to launch your Stripe Connect integration on Netlify!
