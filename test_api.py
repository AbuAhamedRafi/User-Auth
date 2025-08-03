"""
Test script for User Authentication API
This script demonstrates the main functionality of the API
"""

import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Test the API endpoints"""
    
    print("🚀 Testing User Authentication API")
    
    # 1. Test API Overview
    print("\n1. Testing API Overview...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "API Overview")
    
    # 2. Test User Registration
    print("\n2. Testing User Registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "role": "user"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
    print_response(response, "User Registration")
    
    if response.status_code == 201:
        tokens = response.json().get('tokens', {})
        access_token = tokens.get('access')
        
        if access_token:
            # 3. Test User Info
            print("\n3. Testing User Info...")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/auth/user-info/", headers=headers)
            print_response(response, "User Info")
            
            # 4. Test User List
            print("\n4. Testing User List...")
            response = requests.get(f"{BASE_URL}/users/", headers=headers)
            print_response(response, "User List")
            
            # 5. Test Profile Update
            print("\n5. Testing Profile Update...")
            update_data = {
                "first_name": "Updated",
                "last_name": "Name"
            }
            response = requests.put(f"{BASE_URL}/auth/profile/", json=update_data, headers=headers)
            print_response(response, "Profile Update")
    
    # 6. Test Admin Login
    print("\n6. Testing Admin Login...")
    admin_login = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=admin_login)
    print_response(response, "Admin Login")
    
    if response.status_code == 200:
        admin_token = response.json().get('access')
        
        if admin_token:
            # 7. Test User Stats (Admin only)
            print("\n7. Testing User Stats (Admin only)...")
            admin_headers = {"Authorization": f"Bearer {admin_token}"}
            response = requests.get(f"{BASE_URL}/users/stats/", headers=admin_headers)
            print_response(response, "User Statistics")
            
            # 8. Test Create User (Admin only)
            print("\n8. Testing Create User (Admin only)...")
            new_user_data = {
                "username": "adminuser",
                "email": "adminuser@example.com",
                "first_name": "Admin",
                "last_name": "Created",
                "password": "adminpassword123",
                "password_confirm": "adminpassword123",
                "role": "user",
                "is_active": True
            }
            response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=admin_headers)
            print_response(response, "Create User (Admin)")
    
    print(f"\n{'='*50}")
    print("✅ API Testing Complete!")
    print(f"{'='*50}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the API server.")
        print("Please make sure the Django development server is running:")
        print("python manage.py runserver")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
