"""
Fix Excel export for Revolut Statement Analysis
"""

import pandas as pd
import os
from datetime import datetime

OUTPUT_DIR = "financial-analysis-output/"

print("🔧 Regenerating Excel file with proper formatting...")

# Key metrics from the analysis
summary_data = {
    'Metric': [
        'Opening Balance',
        'Closing Balance', 
        'Net Change',
        'Total Money In',
        'Total Money Out',
        'Net Cash Flow',
        'Avg Monthly Income',
        'Avg Monthly Expenses',
        'Number of Transactions',
        'Analysis Period'
    ],
    'Value': [
        '€1,328.29',
        '€288.22',
        '€-1,040.07',
        '€59,299.56',
        '€60,339.63',
        '€-1,040.07',
        '€9,409.82',
        '€1,859.52',
        '3293',
        'Jan 1 - Nov 27, 2025'
    ]
}

# Monthly breakdown
monthly_data = {
    'Month': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', 
              '2025-07', '2025-08', '2025-10', '2025-11'],
    'Money In': [4020.52, 3880.20, 1849.80, 3941.73, 4584.69, 10086.91, 
                 17011.93, 9175.38, 33730.09, 5816.96],
    'Money Out': [2736.68, 2682.20, 1380.86, 993.66, 1014.20, 1223.97, 
                  3281.01, 1549.45, 2697.40, 1035.80],
    'Net': [1283.84, 1198.00, 468.94, 2948.07, 3570.49, 8862.94, 
            13730.92, 7625.93, 31032.69, 4781.16]
}

# Category spending
category_data = {
    'Category': ['Other', 'Savings', 'Fuel', 'Groceries', 'Transfers Out', 
                 'Shopping', 'Transport', 'Entertainment', 'Restaurants', 'Crypto'],
    'Amount': [8677.35, 5345.60, 1371.21, 1174.51, 842.63, 
               575.65, 537.59, 40.60, 29.72, 0.37],
    'Percentage': [14.4, 8.9, 2.3, 1.9, 1.4, 1.0, 0.9, 0.1, 0.0, 0.0]
}

# Top expenses
top_expenses_data = {
    'Description': [
        'Booking.com',
        'IKEA',
        'Allianz',
        'Tst Foxhunter Elepha',
        'Ryanair'
    ],
    'Amount': [1059.68, 761.00, 612.71, 357.92, 314.32],
    'Date': ['24 Jul 2025', '12 Oct 2025', '21 Jan 2025', '19 Oct 2025', '17 Apr 2025']
}

# Create DataFrames
df_summary = pd.DataFrame(summary_data)
df_monthly = pd.DataFrame(monthly_data)
df_category = pd.DataFrame(category_data)
df_top_exp = pd.DataFrame(top_expenses_data)

# Write to Excel with proper formatting
try:
    with pd.ExcelWriter(f'{OUTPUT_DIR}05-revolut-analysis.xlsx', engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        df_monthly.to_excel(writer, sheet_name='Monthly Breakdown', index=False)
        df_category.to_excel(writer, sheet_name='Categories', index=False)
        df_top_exp.to_excel(writer, sheet_name='Top Expenses', index=False)
        
    print("✓ Excel file created successfully!")
    print(f"✓ Saved to: {OUTPUT_DIR}05-revolut-analysis.xlsx")
    
except Exception as e:
    print(f"✗ Error creating Excel: {e}")
    print("\n📋 Trying alternative CSV format instead...")
    
    # Fallback to CSV files
    df_summary.to_csv(f'{OUTPUT_DIR}summary.csv', index=False)
    df_monthly.to_csv(f'{OUTPUT_DIR}monthly-breakdown.csv', index=False)
    df_category.to_csv(f'{OUTPUT_DIR}categories.csv', index=False)
    df_top_exp.to_csv(f'{OUTPUT_DIR}top-expenses.csv', index=False)
    
    print("✓ Created CSV files instead (can be opened in Excel):")
    print("  - summary.csv")
    print("  - monthly-breakdown.csv")
    print("  - categories.csv")
    print("  - top-expenses.csv")

print("\n✅ Done! You can now open the file in Excel.")
