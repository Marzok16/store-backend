!/usr/bin/env python
"""
Simple test script for dashboard API endpoints
Run this after starting the Django server to test the dashboard API
"""

import requests
import json
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_endpoint(method, url, data=None, headers=None, expected_status=200):
    """Test an API endpoint"""
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        print(f"{method.upper()} {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            print(f"Expected: {expected_status}, Got: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_data = response.json()
                print(f"Response: {json.dumps(json_data, indent=2)[:200]}...")
            except:
                print(f"Response: {response.text[:200]}...")
        else:
            print(f"Response: {response.text[:200]}...")
        
        print("-" * 50)
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Could not connect to {url}")
        print("Make sure the Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def main():
    print("🧪 Testing Dashboard API Endpoints")
    print("=" * 50)
    
    # Test public endpoints first
    print("\n1. Testing Public Endpoints")
    test_endpoint('GET', f"{API_BASE}/products/")
    test_endpoint('GET', f"{API_BASE}/products/categories/")
    test_endpoint('GET', f"{API_BASE}/products/price-range/")
    
    # Test dashboard endpoints without authentication (should fail)
    print("\n2. Testing Dashboard Endpoints (No Auth - Should Fail)")
    test_endpoint('GET', f"{API_BASE}/products/dashboard/stats/", expected_status=401)
    test_endpoint('GET', f"{API_BASE}/products/dashboard/products/", expected_status=401)
    test_endpoint('POST', f"{API_BASE}/products/dashboard/products/create/", 
                  data={"title": "Test Product"}, expected_status=401)
    
    print("\n3. Testing User Management Endpoints (No Auth - Should Fail)")
    test_endpoint('GET', f"{API_BASE}/users/admin/users/", expected_status=401)
    test_endpoint('POST', f"{API_BASE}/users/admin/make-admin/", 
                  data={"user_id": 1}, expected_status=401)
    
    print("\n✅ Basic API structure test completed!")
    print("\n📝 Next Steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Login to get JWT token")
    print("3. Use the token to test authenticated endpoints")
    print("4. Make a user admin using the admin endpoint")
    print("5. Test dashboard functionality with admin user")

if __name__ == "__main__":
    main()


