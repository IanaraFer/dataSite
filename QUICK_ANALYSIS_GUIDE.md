# How to Generate Reports Using quick-analysis.py

## Quick Start (5 minutes)

### Step 1: Customer Sends File
- They email you: `sales-data.csv` or `customers.xlsx`
- Or upload via OneDrive link you provide

### Step 2: Save Customer Data
```
customer-data/
  └── john-doe-2026-01-21/
      └── raw-data.csv  ← Save customer file here
```

### Step 3: Update the Script
Open `quick-analysis.py` and change:

```python
CUSTOMER_NAME = "John Doe"  # ← Change this
INPUT_FILE = "customer-data/john-doe-2026-01-21/raw-data.csv"  # ← Change this
OUTPUT_FOLDER = "customer-data/john-doe-2026-01-21/output/"  # ← Change this
```

### Step 4: Run the Script
```bash
python quick-analysis.py
```

### Step 5: Check Output
```
customer-data/john-doe-2026-01-21/output/
  ├── 01-revenue-trend.png
  ├── 02-top-products.png
  ├── 03-customer-segments.png
  ├── 04-processed-data.xlsx
  └── 05-summary.txt
```

### Step 6: Create PDF Report
Use these images + summary to create a PDF:

**Option A: Google Docs (Easy)**
1. Create new Google Doc
2. Paste images + summary text
3. File → Download → PDF
4. Save as: `Analytica-Report-[Customer]-[Date].pdf`

**Option B: Word (Also easy)**
1. Create new Word doc
2. Insert images
3. File → Save As → PDF

### Step 7: Upload to OneDrive
1. Go to: https://onedrive.live.com
2. Upload PDF + Excel file
3. Get share links (view-only)

### Step 8: Send to Customer
Use the email template from `EMAIL_TEMPLATES.md`

---

## 📊 Customizing for Your Data

The script assumes these columns:
- `date` - Date of transaction
- `revenue` - Revenue amount
- `product` - Product name
- `customer_id` - Customer identifier

**Your data might be different!** That's OK, edit the script:

### Example: Your data has different columns

If your data has:
- `sales_date` instead of `date`
- `amount` instead of `revenue`
- `item_name` instead of `product`

**Change the code:**
```python
# Before:
if 'date' in df.columns and 'revenue' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    daily_revenue = df.groupby('date')['revenue'].sum()

# After:
if 'sales_date' in df.columns and 'amount' in df.columns:
    df['sales_date'] = pd.to_datetime(df['sales_date'])
    daily_revenue = df.groupby('sales_date')['amount'].sum()
```

---

## ⚙️ Installation (First Time Only)

Make sure you have required libraries:

```bash
pip install pandas matplotlib seaborn openpyxl
```

---

## 🎯 Full Workflow Example

**Customer: Jane Smith**
**Order: €29.99 Analysis**
**Date: 2026-01-22**

```bash
# Step 1: Create folder
mkdir customer-data/jane-smith-2026-01-22

# Step 2: Get file from customer (jane_sales.csv)
# Save to: customer-data/jane-smith-2026-01-22/raw-data.csv

# Step 3: Edit quick-analysis.py
CUSTOMER_NAME = "Jane Smith"
INPUT_FILE = "customer-data/jane-smith-2026-01-22/raw-data.csv"
OUTPUT_FOLDER = "customer-data/jane-smith-2026-01-22/output/"

# Step 4: Run analysis
python quick-analysis.py

# Output:
# ✓ revenue-trend.png
# ✓ top-products.png
# ✓ customer-segments.png
# ✓ processed-data.xlsx

# Step 5: Create PDF (using Google Docs or Word)
# → Analytica-Report-Jane-Smith-2026-01-22.pdf

# Step 6: Upload to OneDrive
# Jane Smith folder with:
#   - Analytica-Report-Jane-Smith-2026-01-22.pdf
#   - processed-data.xlsx

# Step 7: Send download links via email
```

---

## 📝 Automating This (Next Level)

Once you're doing multiple orders per week, you might want to:

1. **Create a shell script** to automate folder creation
2. **Use a Jupyter Notebook** with customer inputs
3. **Build a Streamlit app** for web-based uploads
4. **Schedule automatic reports** if they subscribe

For now, this manual script works great! ✅

---

## 🐛 Troubleshooting

**Error: "Module not found"**
```bash
pip install pandas matplotlib seaborn openpyxl
```

**Error: "File not found"**
- Check the INPUT_FILE path is correct
- Make sure file is saved in right folder

**Error: "Column 'date' not found"**
- Your CSV might have different column names
- Print the columns: `print(df.columns)`
- Update the script to match your data

---

## 📧 Next Steps After Report

1. ✅ Create PDF + Excel
2. ✅ Upload to OneDrive
3. ✅ Send share links via email
4. ✅ Follow-up in 3 days (see EMAIL_TEMPLATES.md)
5. ✅ Delete customer data after 30 days (GDPR)

---

*Ready to generate your first report?* Let's go! 🚀
