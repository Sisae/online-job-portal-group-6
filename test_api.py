#!/usr/bin/env python
"""
Simple API test script for the Job Portal API
Run this script to test the API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_api():
    print("🚀 Testing Job Portal API")
    print("=" * 50)
    
    # Test 1: Register a new employer
    print("\n1. Registering new employer...")
    register_data = {
        "username": "test_employer",
        "first_name": "Test",
        "last_name": "Employer",
        "email": "test@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "user_type": "employer"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    if response.status_code == 201:
        print("✅ Registration successful")
        token = response.json()['token']
        print(f"Token: {token[:20]}...")
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(response.text)
        return
    
    # Test 2: Create company profile
    print("\n2. Creating company profile...")
    company_data = {
        "name": "Test Company Inc",
        "website": "https://testcompany.com",
        "description": "A test company for API testing",
        "location": "Test City, TC",
        "contact_email": "contact@testcompany.com"
    }
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{BASE_URL}/companies/", json=company_data, headers=headers)
    if response.status_code == 201:
        print("✅ Company created successfully")
        company_id = response.json()['id']
    else:
        print(f"❌ Company creation failed: {response.status_code}")
        print(response.text)
        return
    
    # Test 3: Create a job
    print("\n3. Creating a job...")
    job_data = {
        "title": "Senior Python Developer",
        "description": "We are looking for an experienced Python developer to join our team.",
        "location": "Test City, TC",
        "remote": True,
        "job_type": "full-time",
        "salary": 100000,
        "closing_date": "2024-12-31T23:59:59Z",
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/jobs/", json=job_data, headers=headers)
    if response.status_code == 201:
        print("✅ Job created successfully")
        job_id = response.json()['id']
    else:
        print(f"❌ Job creation failed: {response.status_code}")
        print(response.text)
        return
    
    # Test 4: Get dashboard stats
    print("\n4. Getting dashboard statistics...")
    response = requests.get(f"{BASE_URL}/dashboard/stats/", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print("✅ Dashboard stats retrieved")
        print(f"   Total jobs: {stats['total_jobs']}")
        print(f"   Active jobs: {stats['active_jobs']}")
        print(f"   Total applications: {stats['total_applications']}")
    else:
        print(f"❌ Dashboard stats failed: {response.status_code}")
        print(response.text)
    
    # Test 5: Search jobs
    print("\n5. Searching jobs...")
    response = requests.get(f"{BASE_URL}/jobs/search/?search=python", headers=headers)
    if response.status_code == 200:
        jobs = response.json()
        print(f"✅ Found {len(jobs['results'])} jobs")
    else:
        print(f"❌ Job search failed: {response.status_code}")
        print(response.text)
    
    # Test 6: Get company profile
    print("\n6. Getting company profile...")
    response = requests.get(f"{BASE_URL}/companies/my_company/", headers=headers)
    if response.status_code == 200:
        company = response.json()
        print("✅ Company profile retrieved")
        print(f"   Company: {company['name']}")
        print(f"   Location: {company['location']}")
    else:
        print(f"❌ Company profile failed: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print(f"API Base URL: {BASE_URL}")
    print(f"Admin Panel: http://127.0.0.1:8000/admin/")
    print(f"API Documentation: {BASE_URL}/")

if __name__ == "__main__":
    test_api()


