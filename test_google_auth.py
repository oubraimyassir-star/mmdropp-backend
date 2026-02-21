"""
Test script to verify Google Auth endpoint is working correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_google_auth_endpoint():
    """Test that the /auth/google endpoint is accessible and returns proper errors"""
    
    print("=" * 60)
    print("Testing Google Auth Endpoint")
    print("=" * 60)
    
    # Test with invalid credential (should fail gracefully)
    print("\n1. Testing with invalid credential...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/google",
            json={"credential": "invalid_test_token"},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("   ✓ Endpoint correctly rejects invalid token with 401")
        elif response.status_code == 500:
            error_detail = response.json().get("detail", "")
            if "DOMAIN" in error_detail or "NameError" in error_detail:
                print("   ✗ CRITICAL: DOMAIN variable error detected!")
                print(f"   Error: {error_detail}")
                return False
            else:
                print(f"   ⚠ Server error (500): {error_detail}")
        else:
            print(f"   ⚠ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ✗ ERROR: Cannot connect to backend server!")
        print("   Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"   ✗ ERROR: {str(e)}")
        return False
    
    # Test server health
    print("\n2. Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Server is running")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"   ⚠ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ✗ ERROR: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("- Backend server is accessible")
    print("- Google Auth endpoint is responding")
    print("- No critical configuration errors detected")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_google_auth_endpoint()
    exit(0 if success else 1)
