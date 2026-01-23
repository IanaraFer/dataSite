"""
COMPLETE BANK STATEMENT ANALYZER
Extracts data from PDF and generates full financial report
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Try to import PDF libraries
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ pdfplumber not installed. Install with: pip install pdfplumber")

# Configuration
PDF_FILE = r"c:\Users\35387\Downloads\account-statement_2025-01-01_2025-11-27_en-ie_b8eae1 (1).pdf"
OUTPUT_DIR = "financial-analysis-output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("           FINANCIAL ANALYSIS - BANK STATEMENT ANALYZER")
print("=" * 70)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Statement File: {PDF_FILE}")
print("=" * 70)

if not PDF_AVAILABLE:
    print("\n📦 REQUIRED INSTALLATION:")
    print("-" * 70)
    print("Please run these commands first:")
    print("  pip install pdfplumber")
    print("  pip install pandas matplotlib seaborn openpyxl")
    print("\nThen run this script again.")
    print("=" * 70)
    exit()

# Extract data from PDF
print("\n📄 EXTRACTING DATA FROM PDF...")
try:
    with pdfplumber.open(PDF_FILE) as pdf:
        all_text = []
        for page in pdf.pages:
            all_text.append(page.extract_text())
        
        full_text = "\n".join(all_text)
        
        # Save extracted text for review
        with open(f"{OUTPUT_DIR}extracted-text.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
        
        print(f"✓ Extracted {len(pdf.pages)} pages")
        print(f"✓ Text saved to: {OUTPUT_DIR}extracted-text.txt")
        
        # Parse transactions (this part needs to be customized based on your bank's format)
        lines = full_text.split('\n')
        
        print("\n📊 PREVIEW OF EXTRACTED DATA:")
        print("-" * 70)
        for i, line in enumerate(lines[:30]):  # First 30 lines
            print(f"{i+1}: {line}")
        
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("-" * 70)
        print("1. Review 'extracted-text.txt' to see your statement data")
        print("2. I'll create a parser based on your bank's format")
        print("3. Then generate complete analysis with charts")
        print("=" * 70)

except Exception as e:
    print(f"❌ Error reading PDF: {e}")
    print("\nTIP: Make sure the PDF file exists at:")
    print(f"  {PDF_FILE}")
