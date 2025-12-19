#!/usr/bin/env python3
"""
Test script to verify Django API is working correctly.
Run this from the project root: python test_api_connection.py
"""
import requests  # pyright: ignore[reportMissingModuleSource]
import json

API_BASE = "http://localhost:8000"

def test_api():
    print("🧪 Testing Django Alerts API Connection\n")
    
    # Test 1: List alerts for MGR001
    print("1️⃣ Testing GET /api/alerts?manager_id=MGR001&scope=direct")
    try:
        response = requests.get(
            f"{API_BASE}/api/alerts",
            params={"manager_id": "MGR001", "scope": "direct"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Found {data['count']} alerts")
            if data['results']:
                print(f"   📋 First alert: {data['results'][0]['category']} ({data['results'][0]['severity']})")
            else:
                print("   ⚠️  No alerts found (you may need to run: python manage.py seed_alerts)")
        else:
            print(f"   ❌ Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed! Is Django server running?")
        print("   Run: cd backend && python manage.py runserver")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # Test 2: Test dismiss endpoint
    print("2️⃣ Testing POST /api/alerts/ALT001/dismiss")
    try:
        response = requests.post(f"{API_BASE}/api/alerts/ALT001/dismiss")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Alert status: {data['status']}")
        else:
            print(f"   ⚠️  Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    print()
    print("✅ API tests complete!")
    print("\n📝 Next steps:")
    print("   1. Make sure Django server is running: cd backend && python manage.py runserver")
    print("   2. Make sure React frontend is running: cd alerts-frontend && npm start")
    print("   3. Open http://localhost:3000 in your browser")
    print("   4. Use Manager ID: MGR001")
    
    return True

if __name__ == "__main__":
    test_api()


