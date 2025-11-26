"""
Test script for shopping API integration
Tests Myntra and Ajio data in the chatbot
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_chatbot_shopping():
    """Test chatbot shopping commands"""
    print("=" * 60)
    print("Testing Chatbot Shopping Integration")
    print("=" * 60)
    
    test_messages = [
        "I want to buy a t-shirt",
        "Search for t-shirts",
        "Show trending items",
        "Compare jeans prices",
        "Find shoes on Myntra and Ajio"
    ]
    
    for message in test_messages:
        print(f"\n📝 User: {message}")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/chatbot",
                json={"message": message},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Bot Response:")
                print(data.get('response', 'No response'))
                
                if data.get('suggestions'):
                    print(f"\n💡 Suggestions: {', '.join(data['suggestions'][:3])}")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

def test_shopping_search():
    """Test shopping search API"""
    print("\n" + "=" * 60)
    print("Testing Shopping Search API")
    print("=" * 60)
    
    queries = ["t-shirt", "jeans", "kurta", "shoes"]
    
    for query in queries:
        print(f"\n🔍 Searching for: {query}")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/shopping/search",
                json={
                    "query": query,
                    "category": "clothing",
                    "max_results": 3
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', {})
                
                print(f"✅ Found {results.get('summary', {}).get('total_items', 0)} items")
                
                # Show Myntra items
                myntra_items = results.get('myntra', [])
                if myntra_items:
                    print(f"\n🏪 Myntra ({len(myntra_items)} items):")
                    for item in myntra_items[:2]:
                        print(f"   • {item['name']} - ₹{item['price']:,} ({item['discount']}% off) ⭐{item['rating']}")
                
                # Show Ajio items
                ajio_items = results.get('ajio', [])
                if ajio_items:
                    print(f"\n🏪 Ajio ({len(ajio_items)} items):")
                    for item in ajio_items[:2]:
                        print(f"   • {item['name']} - ₹{item['price']:,} ({item['discount']}% off) ⭐{item['rating']}")
                
                # Show price range
                summary = results.get('summary', {})
                price_range = summary.get('price_range', {})
                if price_range.get('min'):
                    print(f"\n💰 Price Range: ₹{price_range['min']:,} - ₹{price_range['max']:,}")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

def test_trending_items():
    """Test trending items API"""
    print("\n" + "=" * 60)
    print("Testing Trending Items API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/shopping/trending", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Trending Items Retrieved")
            print(data.get('trending', 'No trending data'))
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_price_comparison():
    """Test price comparison API"""
    print("\n" + "=" * 60)
    print("Testing Price Comparison API")
    print("=" * 60)
    
    items = ["t-shirt", "jeans"]
    
    for item in items:
        print(f"\n💰 Comparing prices for: {item}")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/shopping/compare",
                json={"item_name": item},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Price Comparison:")
                print(data.get('comparison', 'No comparison data'))
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("\n🚀 Starting Shopping API Tests...")
    print("Make sure Flask server is running on http://127.0.0.1:5000\n")
    
    try:
        # Test if server is running
        response = requests.get(BASE_URL, timeout=5)
        print("✅ Server is running!\n")
        
        # Run tests
        test_shopping_search()
        test_trending_items()
        test_price_comparison()
        test_chatbot_shopping()
        
        print("\n" + "=" * 60)
        print("✅ All Tests Completed!")
        print("=" * 60)
        print("\n💡 You can now use the chatbot with commands like:")
        print("   • 'Search for t-shirts'")
        print("   • 'Show trending items'")
        print("   • 'Compare jeans prices'")
        print("   • 'I want to buy shoes'")
        print("\n🌐 Open http://127.0.0.1:5000 in your browser to try it!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Flask server")
        print("Please make sure the server is running: python web/app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
