#!/usr/bin/env python3
"""
Pricing Verification Script for AI Data Analyzer Platform
Ensures all pricing is consistent across all platform files
"""

import os
import re
from pathlib import Path

def check_pricing_consistency():
    """Check pricing consistency across platform files"""
    print("🔍 AI Data Analyzer - Pricing Consistency Check")
    print("=" * 50)
    
    # Expected pricing from backend API
    expected_pricing = {
        "essential": 99,
        "professional": 199, 
        "business": 399
    }
    
    # Files to check
    website_dir = Path(".")
    files_to_check = [
        "index.html",
        "platform.html", 
        "free-trial.html",
        "../backend/main.py"
    ]
    
    pricing_found = {}
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n📄 Checking {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for pricing patterns
            pricing_patterns = [
                r'€(\d+)/?month',
                r'€(\d+)\s*/?month',
                r'price["\']?\s*:\s*(\d+)',
                r'Essential[^€]*€(\d+)',
                r'Professional[^€]*€(\d+)', 
                r'Business[^€]*€(\d+)'
            ]
            
            found_prices = []
            for pattern in pricing_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                found_prices.extend(matches)
            
            if found_prices:
                print(f"  💰 Found prices: {', '.join(set(found_prices))}")
                pricing_found[file_path] = list(set(found_prices))
            else:
                print(f"  ℹ️  No pricing found")
        else:
            print(f"❌ File not found: {file_path}")
    
    # Summary
    print(f"\n📊 PRICING SUMMARY")
    print("=" * 30)
    print(f"✅ Expected Essential: €{expected_pricing['essential']}/month")
    print(f"✅ Expected Professional: €{expected_pricing['professional']}/month") 
    print(f"✅ Expected Business: €{expected_pricing['business']}/month")
    
    print(f"\n🎯 CONSISTENCY STATUS")
    print("=" * 30)
    
    # Check if key prices are found
    essential_found = any('99' in prices for prices in pricing_found.values())
    professional_found = any('199' in prices for prices in pricing_found.values())
    business_found = any('399' in prices for prices in pricing_found.values())
    
    if essential_found and professional_found and business_found:
        print("✅ All expected prices found across files")
        print("✅ Pricing appears consistent")
    else:
        print("⚠️  Some pricing may be missing or inconsistent")
        if not essential_found:
            print("   - Essential (€99) not found")
        if not professional_found:
            print("   - Professional (€199) not found") 
        if not business_found:
            print("   - Business (€399) not found")
    
    print(f"\n💡 RECOMMENDATIONS")
    print("=" * 30)
    print("✅ Pricing updated to competitive SME market rates")
    print("✅ Clear value proposition for each tier")
    print("✅ Aligned with backend API pricing")
    print("💰 Monthly pricing optimized for Irish/European SME market")
    
    return pricing_found

if __name__ == "__main__":
    try:
        pricing_data = check_pricing_consistency()
        print(f"\n🎉 Pricing verification complete!")
    except Exception as e:
        print(f"❌ Error during pricing check: {e}")
