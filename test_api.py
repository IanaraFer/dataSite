import requests
import json

def test_backend_api():
    """Test the backend API connectivity"""
    try:
        # Test health endpoint
        health_response = requests.get('http://localhost:8001/api/health')
        print(f"✅ Health check: {health_response.status_code}")
        print(f"Response: {health_response.json()}")
        
        # Test trial submission endpoint
        test_data = {
            "firstName": "Test",
            "lastName": "User", 
            "email": "test@example.com",
            "phone": "+1234567890",
            "company": "Test Company",
            "industry": "technology",
            "revenue": "500k-1m",
            "challenge": "Testing form submission",
            "datasetName": "",
            "datasetSize": ""
        }
        
        print("\n🚀 Testing trial submission...")
        trial_response = requests.post(
            'http://localhost:8001/api/trial/submit',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(test_data)
        )
        
        print(f"✅ Trial submission: {trial_response.status_code}")
        print(f"Response: {trial_response.json()}")
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: Cannot connect to backend server")
        print(f"Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_backend_api()
