#!/usr/bin/env python
"""
Script to create an admin user quickly
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User

def create_admin_user():
    print("🔧 Creating Admin User")
    print("=" * 40)
    
    email = input("Enter email for admin user: ").strip()
    password = input("Enter password: ").strip()
    first_name = input("Enter first name (optional): ").strip()
    last_name = input("Enter last name (optional): ").strip()
    
    try:
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"❌ User with email {email} already exists!")
            choice = input("Do you want to make this user admin instead? (y/n): ").strip().lower()
            if choice == 'y':
                user = User.objects.get(email=email)
                user.is_staff = True
                user.save()
                print(f"✅ User {email} is now an admin!")
                return
            else:
                return
        
        # Create new admin user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_active=True
        )
        
        print(f"✅ Admin user created successfully!")
        print(f"Email: {email}")
        print(f"Name: {first_name} {last_name}")
        print(f"Staff status: {user.is_staff}")
        print("\n🎉 You can now login to the frontend with these credentials!")
        print("Dashboard will be available at /dashboard")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")

if __name__ == "__main__":
    create_admin_user()


