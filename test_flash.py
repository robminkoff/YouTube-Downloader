#!/usr/bin/env python3
"""
Simple test to verify flash messages are working.
"""

import requests

def test_flash_messages():
    """Test if flash messages are working."""
    url = "http://localhost:8080"
    
    # Test GET request
    print("Testing GET request...")
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    # Test POST request with invalid URL
    print("\nTesting POST request with invalid URL...")
    data = {'youtube_url': 'invalid-url'}
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    
    # Check if flash message is in response
    if 'error' in response.text.lower() or 'invalid' in response.text.lower():
        print("✅ Flash messages are working!")
    else:
        print("❌ Flash messages might not be working")

if __name__ == "__main__":
    test_flash_messages() 