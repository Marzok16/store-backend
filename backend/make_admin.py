#!/usr/bin/env python
"""
Script to make a user admin via API
Run this after starting the Django server
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def login_and_get_token(email, password):
    """Login and get JWT token"""
    try:
        response = requests.post(f"{API_BASE}/users/login/", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access')
        else:
            print(f"Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Could not connect to Django server")
        print("Make sure the Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def make_user_admin(token, user_id):
    """Make a user admin"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{API_BASE}/users/admin/make-admin/", 
                               json={"user_id": user_id}, 
                               headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: {data.get('message', 'User made admin successfully')}")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def list_users(token):
    """List all users"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{API_BASE}/users/admin/users/", headers=headers)
        
        if response.status_code == 200:
            users = response.json()
            print("\n📋 Available Users:")
            print("-" * 50)
            for user in users:
                status = "Admin" if user.get('is_staff') else "User"
                print(f"ID: {user['id']} | {user['email']} | {status}")
            return users
        else:
            print(f"❌ FAILED to list users: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return []

def main():
    print("🔧 Make User Admin Script")
    print("=" * 50)
    
    # Get superuser credentials
    print("\n1. Login as superuser")
    email = input("Enter superuser email: ").strip()
    password = input("Enter superuser password: ").strip()
    
    # Login and get token
    token = login_and_get_token(email, password)
    if not token:
        print("❌ Failed to login. Exiting.")
        return
    
    print("✅ Login successful!")
    
    # List users
    users = list_users(token)
    if not users:
        print("❌ No users found or failed to list users.")
        return
    
    # Get user ID to make admin
    print("\n2. Select user to make admin")
    try:
        user_id = int(input("Enter user ID to make admin: ").strip())
        
        # Verify user exists
        user_exists = any(user['id'] == user_id for user in users)
        if not user_exists:
            print(f"❌ User with ID {user_id} not found.")
            return
        
        # Make user admin
        print(f"\n3. Making user {user_id} admin...")
        success = make_user_admin(token, user_id)
        
        if success:
            print("\n🎉 User is now an admin!")
            print("They can now access the dashboard at /dashboard")
        else:
            print("\n❌ Failed to make user admin.")
            
    except ValueError:
        print("❌ Invalid user ID. Please enter a number.")
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")

if __name__ == "__main__":
    main()


