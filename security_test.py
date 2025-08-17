#!/usr/bin/env python3
"""
Security testing script for AgriTech Flask applications
Tests input validation, SQL injection prevention, and error handling
"""

import requests
import json
import time
import sys

# Test configuration
BASE_URLS = {
    'crop_recommendation': 'http://localhost:5501',
    'crop_yield': 'http://localhost:5502',
    'crop_prices': 'http://localhost:5001',
    'forum': 'http://localhost:5000',
    'disease_prediction': 'http://localhost:5000',
    'crop_planning': 'http://localhost:5003',
    'labour_alerts': 'http://localhost:5000'
}

# SQL Injection test payloads
SQL_INJECTION_PAYLOADS = [
    "admin'; DROP TABLE users; --",
    "' OR '1'='1",
    "admin' UNION SELECT * FROM users --",
    "'; INSERT INTO users VALUES ('hacker', 'password'); --",
    "' OR 1=1--",
    "admin'--",
    "'; DELETE FROM users; --"
]

# XSS test payloads
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "javascript:alert('XSS')",
    "<svg onload=alert('XSS')>",
    "';alert('XSS');//"
]

# Path traversal test payloads
PATH_TRAVERSAL_PAYLOADS = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",
    "....//....//....//etc/passwd",
    "..%2F..%2F..%2Fetc%2Fpasswd"
]

def test_missing_fields():
    """Test missing required fields"""
    print("\n=== Testing Missing Required Fields ===")
    
    # Test crop recommendation
    try:
        response = requests.post(f"{BASE_URLS['crop_recommendation']}/predict", data={})
        if response.status_code == 400:
            print("✓ Crop Recommendation: Missing fields properly rejected")
        else:
            print("✗ Crop Recommendation: Missing fields not properly handled")
    except:
        print("✗ Crop Recommendation: Service not available")
    
    # Test crop yield prediction
    try:
        response = requests.post(f"{BASE_URLS['crop_yield']}/predict", data={})
        if response.status_code == 400:
            print("✓ Crop Yield: Missing fields properly rejected")
        else:
            print("✗ Crop Yield: Missing fields not properly handled")
    except:
        print("✗ Crop Yield: Service not available")

def test_sql_injection():
    """Test SQL injection prevention"""
    print("\n=== Testing SQL Injection Prevention ===")
    
    for payload in SQL_INJECTION_PAYLOADS:
        # Test crop recommendation
        try:
            data = {
                'N': payload,
                'P': '50',
                'K': '50',
                'temperature': '25',
                'humidity': '60',
                'ph': '7',
                'rainfall': '100'
            }
            response = requests.post(f"{BASE_URLS['crop_recommendation']}/predict", data=data)
            if response.status_code == 400:
                print(f"✓ SQL Injection blocked in crop recommendation: {payload[:30]}...")
            else:
                print(f"✗ SQL Injection not blocked in crop recommendation: {payload[:30]}...")
        except:
            pass

def test_xss_prevention():
    """Test XSS prevention"""
    print("\n=== Testing XSS Prevention ===")
    
    for payload in XSS_PAYLOADS:
        # Test forum
        try:
            data = {
                'title': payload,
                'content': 'Test content',
                'author': 'Test Author'
            }
            response = requests.post(f"{BASE_URLS['forum']}/forum", 
                                   json=data, 
                                   headers={'Content-Type': 'application/json'})
            if response.status_code == 400:
                print(f"✓ XSS blocked in forum: {payload[:30]}...")
            else:
                print(f"✗ XSS not blocked in forum: {payload[:30]}...")
        except:
            pass

def test_file_upload_security():
    """Test file upload security"""
    print("\n=== Testing File Upload Security ===")
    
    # Test disease prediction with malicious filename
    try:
        files = {'file': ('../../../etc/passwd', b'fake image data', 'image/jpeg')}
        response = requests.post(f"{BASE_URLS['disease_prediction']}/predict", files=files)
        if response.status_code == 400:
            print("✓ Path traversal blocked in file upload")
        else:
            print("✗ Path traversal not blocked in file upload")
    except:
        print("✗ Disease prediction service not available")

def test_numeric_validation():
    """Test numeric input validation"""
    print("\n=== Testing Numeric Input Validation ===")
    
    # Test invalid numeric inputs
    invalid_inputs = [
        {'N': 'abc', 'P': '50', 'K': '50', 'temperature': '25', 'humidity': '60', 'ph': '7', 'rainfall': '100'},
        {'N': '50', 'P': 'xyz', 'K': '50', 'temperature': '25', 'humidity': '60', 'ph': '7', 'rainfall': '100'},
        {'N': '50', 'P': '50', 'K': '50', 'temperature': '999', 'humidity': '60', 'ph': '7', 'rainfall': '100'},
        {'N': '50', 'P': '50', 'K': '50', 'temperature': '25', 'humidity': '150', 'ph': '7', 'rainfall': '100'},
    ]
    
    for i, invalid_data in enumerate(invalid_inputs):
        try:
            response = requests.post(f"{BASE_URLS['crop_recommendation']}/predict", data=invalid_data)
            if response.status_code == 400:
                print(f"✓ Invalid numeric input {i+1} properly rejected")
            else:
                print(f"✗ Invalid numeric input {i+1} not properly handled")
        except:
            pass

def test_json_validation():
    """Test JSON input validation"""
    print("\n=== Testing JSON Input Validation ===")
    
    # Test invalid JSON
    try:
        response = requests.post(f"{BASE_URLS['crop_planning']}/predict", 
                               data="invalid json",
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 400:
            print("✓ Invalid JSON properly rejected")
        else:
            print("✗ Invalid JSON not properly handled")
    except:
        print("✗ Crop planning service not available")

def test_error_handling():
    """Test error handling"""
    print("\n=== Testing Error Handling ===")
    
    # Test with extremely large inputs
    large_input = 'A' * 10000
    try:
        data = {
            'title': large_input,
            'content': large_input,
            'author': large_input
        }
        response = requests.post(f"{BASE_URLS['forum']}/forum", 
                               json=data, 
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 400:
            print("✓ Large input properly rejected")
        else:
            print("✗ Large input not properly handled")
    except:
        print("✗ Forum service not available")

def test_api_endpoints():
    """Test API endpoint availability"""
    print("\n=== Testing API Endpoint Availability ===")
    
    endpoints = [
        (f"{BASE_URLS['crop_prices']}/get_states", "GET"),
        (f"{BASE_URLS['crop_prices']}/get_markets", "GET"),
        (f"{BASE_URLS['labour_alerts']}/news", "GET"),
    ]
    
    for url, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
            
            if response.status_code in [200, 400, 404]:
                print(f"✓ {url} is responding")
            else:
                print(f"✗ {url} returned status {response.status_code}")
        except:
            print(f"✗ {url} is not available")

def main():
    """Run all security tests"""
    print("AgriTech Security Testing Suite")
    print("=" * 50)
    
    test_missing_fields()
    test_sql_injection()
    test_xss_prevention()
    test_file_upload_security()
    test_numeric_validation()
    test_json_validation()
    test_error_handling()
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("Security testing completed!")
    print("✓ = Test passed")
    print("✗ = Test failed or service unavailable")

if __name__ == "__main__":
    main()
