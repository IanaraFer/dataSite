# Customer Order Workflow Guide
**For €29.99 One-Time Analysis & All Service Tiers**

---

## 📧 Step 1: Email Received (Sample Report or One-Time Analysis)

When you receive an email from your forms (formsubmit.co → information@analyticacoreai.ie), you'll get:

**Sample Report Request:**
- Name, Email, Company, Industry, Goal, Data Size, Bottleneck description
- Action: Send them a **sample/template report** (no real data needed)

**One-Time Analysis Order (€29.99):**
- Name, Email, Phone, Project Type, Message, Data File (if attached)
- Action: Follow the workflow below

---

## 🔄 Complete One-Time Analysis Workflow

### Phase 1: Initial Response (Within 2 hours)
**Email Template:**
```
Subject: Order Confirmed - Data Analysis #[ORDER_NUMBER]

Hi [Name],

Thank you for ordering your €29.99 data analysis! I've received your request.

NEXT STEPS:
1. Payment: Please complete payment here → https://buy.stripe.com/6oUbJ1ebW0d5h30d6Q5c400
2. Data Upload: Once paid, please reply with your data file OR use this secure upload link: [WeTransfer/Google Drive/Dropbox link]

ACCEPTED FORMATS:
• CSV, Excel (.xlsx, .xls)
• JSON, TXT
• Max 50,000 rows

DELIVERY:
• Timeline: 48-72 hours after payment + data received
• What you'll get: PDF report, Excel export, interactive charts, action plan

Questions? Just reply to this email.

Best regards,
Ianara Fernandes
Founder & Data Scientist
Analytica Core AI
information@analyticacoreai.ie
```

---

### Phase 2: Data Collection

**Option A: Email Attachment**
- If file is small (<25MB), they can reply with attachment
- Save to: `customer-data/[customer-name]-[date]/raw-data.csv`

**Option B: Secure Upload Link** (Recommended for larger files)
- Use **WeTransfer** (free, no signup): https://wetransfer.com
- Use **Google Drive** shared link
- Use **Dropbox** file request
- Customer uploads → You download to local folder

**Folder Structure:**
```
customer-data/
  ├── john-doe-2026-01-21/
  │   ├── raw-data.csv
  │   ├── analysis-output/
  │   └── final-delivery/
  ├── jane-smith-2026-01-22/
  │   ├── raw-data.xlsx
  │   └── ...
```

---

### Phase 3: Data Analysis (Use Your Platform)

**Where to Process:**
1. **Upload to your Streamlit app** (if you have it running locally or deployed)
2. **Use Python scripts** in this workspace
3. **Manual analysis** with pandas, matplotlib, seaborn

**Create a Quick Analysis Script:**
```python
# analysis_template.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load customer data
df = pd.read_csv('customer-data/[customer-folder]/raw-data.csv')

# Generate outputs
# 1. Revenue forecast
# 2. Customer segmentation
# 3. Trend analysis
# 4. Anomaly detection
# 5. KPI summary

# Save outputs
output_folder = 'customer-data/[customer-folder]/analysis-output/'
# ... save charts, tables, insights
```

---

### Phase 4: Delivery Preparation

**What to Create:**

1. **PDF Report** (Main deliverable)
   - Cover page with customer name & date
   - Executive summary (1 page)
   - Charts & visualizations (4-6 pages)
   - Data tables (2-3 pages)
   - AI Insights & recommendations (2 pages)
   - Action plan (1 page)
   
2. **Excel Export**
   - Raw data (cleaned)
   - Calculated metrics
   - Pivot tables
   - Charts

3. **Interactive Dashboard** (Optional - HTML file)
   - Can be opened in browser
   - Interactive charts with Plotly

**Tools to Use:**
- **PDF**: matplotlib/seaborn → save as PNG → combine in Word/Google Docs → Export PDF
- **Or use:** ReportLab (Python), Jupyter Notebook → PDF export
- **Excel**: pandas `.to_excel()` with multiple sheets

---

### Phase 5: Quality Check

Before sending, verify:
- [ ] All charts are clear and labeled
- [ ] Insights are in plain English (no jargon)
- [ ] Action plan is specific and actionable
- [ ] Customer name/company is correct everywhere
- [ ] Files are named professionally: `Analytica-Report-[CustomerName]-[Date].pdf`

---

### Phase 6: Final Delivery (Within 48-72h)

**Email Template:**
```
Subject: ✅ Your Data Analysis is Ready! [Order #XXX]

Hi [Name],

Your complete data analysis is ready! 🎉

DOWNLOAD YOUR REPORTS:
📊 PDF Report: [Google Drive/Dropbox link]
📈 Excel Export: [Link]
💡 Interactive Dashboard: [Link] (open in browser)

WHAT'S INSIDE:
✓ Revenue trends & 6-month forecast
✓ Customer segmentation analysis
✓ Top opportunities ranked by impact
✓ Anomaly detection & alerts
✓ Actionable next steps with priority levels

NEXT STEPS:
1. Review the Executive Summary (page 2)
2. Check the Action Plan (last page)
3. Questions? Reply to this email - I'm here to help!

OPTIONAL ADD-ON:
Need ongoing monitoring? Check our subscription plans:
→ Professional (€199/mo): Monthly reports + alerts
→ Business (€399/mo): Real-time dashboard + API access

Thank you for trusting Analytica Core AI!

Best regards,
Ianara Fernandes
Founder & Data Scientist
Analytica Core AI

P.S. If you found this valuable, I'd love a testimonial or LinkedIn recommendation! 🙏
```

---

### Phase 7: Follow-Up (3 days after delivery)

**Email Template:**
```
Subject: How's the analysis working out?

Hi [Name],

Just checking in - did you get a chance to review your data analysis?

Quick questions:
• Were the insights useful?
• Any questions about the recommendations?
• Need help implementing any of the action items?

If you're happy with the results, I'd be grateful for:
✓ A quick testimonial I can feature on the website
✓ A LinkedIn recommendation
✓ Referral to colleagues who might benefit

Let me know how I can help!

Best,
Ianara
```

---

## 🛠️ Tools You'll Need

### File Storage & Sharing:
- **Google Drive** (15GB free) - For delivery links
- **WeTransfer** (Free, 2GB transfers) - For large files
- **Dropbox** (Free, 2GB) - Alternative

### Analysis Tools:
- **Python**: pandas, matplotlib, seaborn, plotly
- **Jupyter Notebook**: Great for creating reports
- **Excel/Google Sheets**: Quick calculations
- **Your Streamlit app**: If deployed

### PDF Creation:
- **Google Docs** → Export as PDF
- **Microsoft Word** → Save as PDF
- **Python**: ReportLab or fpdf
- **Jupyter Notebook** → Print to PDF

### Payment Verification:
- **Stripe Dashboard**: Check if payment received
- Login at: https://dashboard.stripe.com

---

## ⚡ Quick Automation Ideas

### Create a Template Response Script:
```python
# email_templates.py
def send_confirmation_email(customer_name, order_number):
    # Auto-generate response with order details
    pass

def send_delivery_email(customer_name, drive_links):
    # Auto-send when analysis is ready
    pass
```

### Batch Processing:
- Process multiple orders on same day
- Create reusable analysis notebooks
- Build template reports (just swap data)

---

## 💰 Pricing Reminder

**One-Time Analysis: €29.99**
- Up to 50k rows
- 48-72h delivery
- All analysis types included

**If customer needs more:**
- **100k+ rows**: Custom quote (€49-€99)
- **Recurring reports**: Suggest Professional plan (€199/mo)
- **Real-time dashboard**: Suggest Business plan (€399/mo)

---

## 🔒 Data Privacy & GDPR

**CRITICAL:**
1. **Delete customer data** after 30 days (state this in email)
2. **Don't share** their data with anyone
3. **Secure storage**: Encrypt sensitive files
4. **Anonymize examples**: If you use their case as a testimonial, remove identifying info

**Add to every email:**
```
Your data is stored securely and will be deleted 30 days after delivery 
per GDPR compliance. We never share or sell your data.
```

---

## 📊 Sample Report Template

For "Sample Report" requests (no real data), send them a **pre-made template** showing:
- Mock charts & KPIs
- Example insights
- Sample action plan
- "This is what you'll get when you order"

**Create once, reuse forever!**

---

## ✅ Checklist for Each Order

- [ ] Payment received (check Stripe)
- [ ] Data file received and saved
- [ ] Analysis completed
- [ ] PDF report created
- [ ] Excel export created
- [ ] Quality check passed
- [ ] Files uploaded to Drive/Dropbox
- [ ] Delivery email sent
- [ ] Follow-up scheduled (3 days)
- [ ] Customer data deletion scheduled (30 days)

---

## 🎯 Success Metrics to Track

- Average delivery time
- Customer satisfaction (ask for rating 1-5)
- Number of upsells to subscriptions
- Referral rate
- Testimonials collected

---

**Ready to scale?** As you get more orders, consider:
1. Hiring a data analyst (part-time)
2. Automating report generation
3. Building a customer portal
4. Creating video walkthrough of reports

---

*Last updated: January 21, 2026*
*Questions? Update this workflow as you learn!*
