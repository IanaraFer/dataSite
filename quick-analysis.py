"""
QUICK ANALYSIS SCRIPT FOR ONE-TIME REPORTS
Run this locally on your computer to generate customer reports
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# ===== CONFIGURATION =====
CUSTOMER_NAME = "John Doe"  # Change this for each customer
INPUT_FILE = "customer-data/john-doe-2026-01-21/raw-data.csv"
OUTPUT_FOLDER = "customer-data/john-doe-2026-01-21/output/"

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ===== LOAD DATA =====
print(f"📊 Loading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
print(f"Data info:\n{df.info()}\n")

# ===== ANALYSIS 1: REVENUE TREND =====
print("Analyzing revenue trends...")
# Assuming 'date' and 'revenue' columns exist
if 'date' in df.columns and 'revenue' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    daily_revenue = df.groupby('date')['revenue'].sum().sort_index()
    
    plt.figure(figsize=(12, 5))
    plt.plot(daily_revenue.index, daily_revenue.values, linewidth=2, color='#2ca02c')
    plt.title('Revenue Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Revenue (€)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_FOLDER}01-revenue-trend.png", dpi=300)
    print("✓ Revenue trend chart saved")
else:
    print("⚠️ Columns 'date' or 'revenue' not found")

# ===== ANALYSIS 2: TOP PRODUCTS =====
print("Analyzing top products...")
if 'product' in df.columns and 'revenue' in df.columns:
    top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    top_products.plot(kind='bar', color='#667eea')
    plt.title('Top 10 Products by Revenue', fontsize=16, fontweight='bold')
    plt.xlabel('Product')
    plt.ylabel('Revenue (€)')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_FOLDER}02-top-products.png", dpi=300)
    print("✓ Top products chart saved")

# ===== ANALYSIS 3: CUSTOMER SEGMENTS =====
print("Analyzing customer segments...")
if 'customer_id' in df.columns and 'revenue' in df.columns:
    customer_revenue = df.groupby('customer_id')['revenue'].sum().sort_values(ascending=False)
    
    # Segment customers
    vip_threshold = customer_revenue.quantile(0.9)
    regular_threshold = customer_revenue.quantile(0.5)
    
    segments = []
    for revenue in customer_revenue:
        if revenue >= vip_threshold:
            segments.append('VIP')
        elif revenue >= regular_threshold:
            segments.append('Regular')
        else:
            segments.append('Occasional')
    
    segment_counts = pd.Series(segments).value_counts()
    
    plt.figure(figsize=(8, 8))
    segment_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    plt.title('Customer Segmentation', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_FOLDER}03-customer-segments.png", dpi=300)
    print("✓ Customer segments chart saved")

# ===== KEY METRICS =====
print("\n📈 KEY METRICS:")
if 'revenue' in df.columns:
    total_revenue = df['revenue'].sum()
    avg_revenue = df['revenue'].mean()
    print(f"Total Revenue: €{total_revenue:,.2f}")
    print(f"Average Transaction: €{avg_revenue:,.2f}")

if 'customer_id' in df.columns:
    unique_customers = df['customer_id'].nunique()
    print(f"Unique Customers: {unique_customers}")

# ===== EXPORT DATA =====
print("\nExporting processed data to Excel...")
df.to_excel(f"{OUTPUT_FOLDER}04-processed-data.xlsx", index=False)
print("✓ Excel export saved")

# ===== CREATE SUMMARY =====
summary = f"""
ANALYSIS SUMMARY - {CUSTOMER_NAME}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATA OVERVIEW:
- Total rows: {len(df)}
- Total columns: {len(df.columns)}
- Date range: (if applicable)

KEY FINDINGS:
1. [Insert your main insight here]
2. [Insert your second insight here]
3. [Insert your third insight here]

RECOMMENDATIONS:
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

FILES GENERATED:
✓ 01-revenue-trend.png
✓ 02-top-products.png
✓ 03-customer-segments.png
✓ 04-processed-data.xlsx
✓ 05-summary.txt
"""

with open(f"{OUTPUT_FOLDER}05-summary.txt", "w") as f:
    f.write(summary)

print("\n✅ ANALYSIS COMPLETE!")
print(f"All files saved to: {OUTPUT_FOLDER}")
print("\nNext steps:")
print("1. Upload files to OneDrive")
print("2. Create share links (view-only)")
print("3. Send links to customer via email")
