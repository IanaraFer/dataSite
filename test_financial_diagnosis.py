"""
Integration Test for Financial Diagnosis Module
Tests all core functionality and API endpoints
"""

import requests
import json
import sys

API_BASE = "http://localhost:5001"

def test_health_check():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_BASE}/api/diagnosis/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Make sure to run: python financial_diagnosis_api.py")
        return False

def test_registration():
    """Test user registration"""
    try:
        test_user = {
            "email": "test@analytica.ai",
            "password": "testpass123",
            "name": "Test User"
        }
        
        response = requests.post(
            f"{API_BASE}/api/diagnosis/register",
            json=test_user
        )
        
        if response.status_code == 201:
            print("✅ User registration works")
            return True
        elif response.status_code == 409:
            print("✅ User registration works (user already exists)")
            return True
        else:
            print(f"❌ Registration failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Registration test error: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        credentials = {
            "email": "test@analytica.ai",
            "password": "testpass123"
        }
        
        session = requests.Session()
        response = session.post(
            f"{API_BASE}/api/diagnosis/login",
            json=credentials
        )
        
        if response.status_code == 200:
            print("✅ User login works")
            return session
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return None

def test_profile(session):
    """Test profile endpoint"""
    try:
        response = session.get(f"{API_BASE}/api/diagnosis/profile")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Profile retrieval works (User: {data.get('email')})")
            return True
        else:
            print(f"❌ Profile test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Profile test error: {e}")
        return False

def test_analysis(session):
    """Test analysis with sample data"""
    try:
        sample_data = {
            "transactions": [
                {"date": "2026-01-01", "type": "income", "category": "Salary", "amount": 3000, "description": "Monthly salary"},
                {"date": "2026-01-05", "type": "expense", "category": "Rent", "amount": 1200, "description": "Rent payment"},
                {"date": "2026-01-10", "type": "expense", "category": "Groceries", "amount": 150, "description": "Supermarket"},
                {"date": "2026-01-15", "type": "expense", "category": "Transport", "amount": 80, "description": "Gas"},
                {"date": "2026-01-20", "type": "expense", "category": "Dining", "amount": 200, "description": "Restaurants"},
            ],
            "accounts": [
                {"account": "Checking", "type": "cash", "balance": 1500},
                {"account": "Savings", "type": "savings", "balance": 5000}
            ]
        }
        
        response = session.post(
            f"{API_BASE}/api/diagnosis/analyze",
            json=sample_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Financial analysis works")
            print(f"   Income: €{data.get('total_income', 0)}")
            print(f"   Expenses: €{data.get('total_expenses', 0)}")
            print(f"   Savings Rate: {data.get('savings_rate', 0):.1f}%")
            return True
        else:
            print(f"❌ Analysis failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Analysis test error: {e}")
        return False

def test_module_imports():
    """Test if all modules can be imported"""
    try:
        from financial_diagnosis import analyze_finances, run_diagnostics, parse_file
        print("✅ All financial diagnosis modules import successfully")
        return True
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False

def main():
    print("=" * 60)
    print("FINANCIAL DIAGNOSIS INTEGRATION TEST")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Module Imports
    print("Test 1: Module Imports")
    results.append(test_module_imports())
    print()
    
    # Test 2: API Health
    print("Test 2: API Health Check")
    api_running = test_health_check()
    results.append(api_running)
    print()
    
    if not api_running:
        print("❌ Cannot proceed with API tests - API is not running")
        print("   Start the API with: python financial_diagnosis_api.py")
        return
    
    # Test 3: Registration
    print("Test 3: User Registration")
    results.append(test_registration())
    print()
    
    # Test 4: Login
    print("Test 4: User Login")
    session = test_login()
    results.append(session is not None)
    print()
    
    if session:
        # Test 5: Profile
        print("Test 5: Get Profile")
        results.append(test_profile(session))
        print()
        
        # Test 6: Analysis
        print("Test 6: Financial Analysis")
        results.append(test_analysis(session))
        print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Integration successful!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
