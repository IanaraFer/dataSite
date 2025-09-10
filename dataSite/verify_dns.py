#!/usr/bin/env python3
"""
DNS Verification Script for AnalyticaCore AI
Checks if SendGrid DNS records are properly configured
"""

import subprocess
import sys

def check_dns_record(record_type, host, expected_value=None):
    """Check if a DNS record exists and optionally verify its value"""
    try:
        if record_type.upper() == 'CNAME':
            cmd = ['nslookup', '-type=CNAME', host]
        elif record_type.upper() == 'TXT':
            cmd = ['nslookup', '-type=TXT', host]
        else:
            cmd = ['nslookup', host]
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            output = result.stdout.lower()
            if expected_value and expected_value.lower() in output:
                return True, f"✅ {host} -> {expected_value}"
            elif 'non-existent' in output or 'can\'t find' in output:
                return False, f"❌ {host} - Record not found"
            else:
                return True, f"⚠️  {host} - Record exists but value unclear"
        else:
            return False, f"❌ {host} - DNS lookup failed"
            
    except subprocess.TimeoutExpired:
        return False, f"❌ {host} - DNS lookup timeout"
    except Exception as e:
        return False, f"❌ {host} - Error: {str(e)}"

def main():
    """Main verification function"""
    print("🔍 AnalyticaCore AI DNS Verification")
    print("=====================================")
    print()
    
    # SendGrid DNS records to check
    dns_records = [
        ('CNAME', 'url8860.analyticacoreai.ie', 'sendgrid.net'),
        ('CNAME', '55387076.analyticacoreai.ie', 'sendgrid.net'),
        ('CNAME', 'em4558.analyticacoreai.ie', 'u55387076.wl077.sendgrid.net'),
        ('CNAME', 's1._domainkey.analyticacoreai.ie', 's1.domainkey.u55387076.wl077.sendgrid.net'),
        ('CNAME', 's2._domainkey.analyticacoreai.ie', 's2.domainkey.u55387076.wl077.sendgrid.net'),
        ('TXT', '_dmarc.analyticacoreai.ie', 'v=DMARC1; p=none;')
    ]
    
    print("📧 SendGrid Email Authentication Records:")
    print("-" * 45)
    
    all_passed = True
    
    for record_type, host, expected in dns_records:
        success, message = check_dns_record(record_type, host, expected)
        print(message)
        if not success:
            all_passed = False
    
    print()
    print("🌐 Additional Domain Records:")
    print("-" * 30)
    
    # Check main domain
    main_success, main_message = check_dns_record('A', 'analyticacoreai.ie')
    print(main_message)
    if not main_success:
        all_passed = False
    
    www_success, www_message = check_dns_record('CNAME', 'www.analyticacoreai.ie')
    print(www_message)
    if not www_success:
        all_passed = False
    
    print()
    print("=" * 50)
    
    if all_passed:
        print("🎉 All DNS records configured correctly!")
        print("✅ Your domain is ready for SendGrid and Vercel!")
    else:
        print("⚠️  Some DNS records need attention.")
        print("📝 Add missing records to your DNS provider.")
        print("⏰ Allow 24-48 hours for DNS propagation.")
    
    print()
    print("🔗 Next Steps:")
    print("1. Verify domain in SendGrid dashboard")
    print("2. Test email sending functionality")  
    print("3. Connect domain to Vercel project")
    print("4. Monitor email delivery rates")

if __name__ == "__main__":
    main()
