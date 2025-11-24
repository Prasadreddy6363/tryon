"""
Test script to verify the virtual try-on route is working
"""
import requests
import time

def test_virtual_tryon_route():
    """Test that the virtual try-on route exists and returns the correct template"""
    try:
        # Test the virtual try-on route
        response = requests.get('http://localhost:5000/virtual_tryon')
        
        # Check if the response is successful
        if response.status_code == 200:
            print("✅ Virtual Try-On route is working!")
            print(f"✅ Status Code: {response.status_code}")
            
            # Check if the response contains expected content
            if "Virtual Try-On System" in response.text:
                print("✅ Correct template is being served!")
                return True
            else:
                print("⚠️ Route is working but template content is unexpected")
                return False
        else:
            print(f"❌ Virtual Try-On route failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error testing virtual try-on route: {e}")
        return False

def test_api_endpoints():
    """Test that API endpoints are accessible"""
    try:
        # Test the main index route
        response = requests.get('http://localhost:5000/')
        
        if response.status_code == 200:
            print("✅ Main index route is working!")
        else:
            print(f"❌ Main index route failed with status code: {response.status_code}")
            
        # Test API endpoints
        response = requests.get('http://localhost:5000/api/dataset/stats')
        
        if response.status_code == 200:
            print("✅ Dataset stats API is working!")
            data = response.json()
            print(f"📊 Dataset stats: {data}")
        else:
            print(f"❌ Dataset stats API failed with status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask server. Is it running?")
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")

if __name__ == "__main__":
    print("🔍 Testing Virtual Try-On Implementation...")
    print("=" * 50)
    
    # Test the virtual try-on route
    success = test_virtual_tryon_route()
    
    print("\n" + "=" * 50)
    
    # Test other API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 All tests passed! The virtual try-on system is ready.")
        print("🌐 Visit http://localhost:5000/virtual_tryon in your browser")
    else:
        print("⚠️ Some tests failed. Please check the Flask server.")