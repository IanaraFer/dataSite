# AnalyticaCore AI – Deployment Guide (Netlify + Vercel + Azure)

This repo is set up so the frontend is served from `website/` and all backend is handled by Netlify Functions in `python-backend/netlify/functions`.

Quick links
- Frontend: `website/`
- Functions: `python-backend/netlify/functions`
- Netlify config: `netlify.toml` (publish=website, functions mapped, `/api/*` to functions)
- Vercel config: `vercel.json` (rewrites everything to `/website`)
- Azure SWA config: `website/staticwebapp.config.json`

## 1) Prepare the repo

1) Merge branch `site-improvements` → `main` in GitHub: `IanaraFer/dataSite`.
2) Confirm the following files exist:
   - `netlify.toml` (publish website; `/api/*` → functions)
   - `vercel.json` (rewrites to `/website`)
   - `website/staticwebapp.config.json` (SPA fallback)

## 2) Netlify (primary hosting)

Site settings → Build & deploy:
- Build command: empty
- Publish directory: `website`
- Functions directory: `python-backend/netlify/functions`
- Environment variables (All contexts):
  - SMTP_HOST = smtp.office365.com
  - SMTP_PORT = 587
  - SMTP_USER = information@analyticacoreai.ie
  - SMTP_PASS = <mailbox password or app password if MFA>
  - STRIPE_SECRET_KEY = <your Stripe secret key>
  - STRIPE_PRICE_ID_STARTER = <price_...>
  - STRIPE_PRICE_ID_PROFESSIONAL = <price_...>
  - STRIPE_PRICE_ID_ENTERPRISE = <price_...>
  - POWER_AUTOMATE_URL = <Flow HTTP Request URL> (optional)
  - (Optional S3) AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION=eu-west-1, S3_BUCKET_NAME

Connect to GitHub repo `IanaraFer/dataSite`, branch `main`, and Deploy site.

Forms (Netlify → Forms):
- Add email notifications for forms `free-trial`, `health-check`, `newsletter` to `information@analyticacoreai.ie`.

Functions included:
- `trial-submit` (multipart form + optional file; emails admin + user)
- `upload` (file upload; S3 optional)
- `forward-power-automate` (forwards JSON to Flow URL)
- `contact` (contact emails via Microsoft 365 SMTP)
- `create-subscription` (legacy; not used by UI)
- `create-checkout-session` (Stripe Checkout for subscriptions)
- `test-smtp` (diagnostic)

## 3) Vercel (optional static mirror)

Use the same repo with either:
- Root Directory: `website` (recommended in UI), or
- Keep root and rely on `vercel.json`:
  ```json
  {"version":2,"rewrites":[{"source":"/","destination":"/website/index.html"},{"source":"/(.*)","destination":"/website/$1"}]}
  ```

No backend on Vercel; all API calls use absolute Netlify Functions URLs (already coded):
- Upload: `https://analyticacoreai.netlify.app/.netlify/functions/upload`
- Trial submit: `https://analyticacoreai.netlify.app/.netlify/functions/trial-submit`
- Power Automate: `https://analyticacoreai.netlify.app/.netlify/functions/forward-power-automate`
- Checkout: `https://analyticacoreai.netlify.app/.netlify/functions/create-checkout-session`

## 4) Azure Static Web Apps (optional)

Create a Static Web App:
- App location: `website`
- API location: (leave empty)
- Output location: (leave empty)
SPA fallback is configured in `website/staticwebapp.config.json`.

## 5) Post-deploy verification

1) SMTP test
- Open: `/.netlify/functions/test-smtp` (on your Netlify domain)
- Expect JSON success and an email to `information@analyticacoreai.ie`

2) File upload (two pages)
- `free-trial-simple` and `generate-analysis`
- Choose a file (<10MB; csv/xlsx/xls/json) → Upload → Expect success message

3) Trial form submission
- Submit `free-trial-simple` → Check Netlify → Forms → `free-trial` and inbox

4) Newsletter
- Submit footer form (newsletter) → Check Netlify → Forms → `newsletter` and inbox

5) Payment
- Open `website/working-payment.html` (or `subscribe.html`)
- Click a plan → Redirect to Stripe Checkout
- If not, check Netlify Functions logs for `create-checkout-session`

## 6) Common errors and fixes

- Payment error: “Unexpected token '<'”
  - Cause: Frontend called a non-JSON endpoint (e.g., static HTML) instead of the function.
  - Fix: Ensure pages call `https://analyticacoreai.netlify.app/.netlify/functions/create-checkout-session`.

- SMTP fails
  - Ensure SMTP_AUTH enabled for mailbox in Microsoft 365; if MFA, use an App Password.
  - Verify `SMTP_*` env vars and redeploy.

- Upload fails
  - Ensure file <10MB and supported extension.
  - Check Netlify → Functions → `upload` logs; errors show boundary/size issues.

- Power Automate receives nothing
  - Set `POWER_AUTOMATE_URL` and redeploy; confirm `forward-power-automate` logs.

## 7) Domains & DNS (reference)

- Apex DNS for `analyticacoreai.ie` should point to your host (e.g., Netlify/Vercel).
- Email DNS (Microsoft 365 + SendGrid/Stripe DKIM) remain as configured.

---

If any step fails, copy the first error line from the platform logs (Netlify Functions / Vercel / Azure) and I’ll provide the one-line fix.
