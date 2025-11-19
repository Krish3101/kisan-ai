import requests
import time
import sys

BASE_URL = "http://127.0.0.1:9000"

def test_endpoint(name, url, method="GET", data=None):
    print(f"Testing {name}...", end=" ")
    try:
        if method == "GET":
            r = requests.get(url)
        else:
            r = requests.post(url, json=data)
        
        if r.status_code == 200:
            print("✅ OK")
            return True
        else:
            print(f"❌ Failed ({r.status_code})")
            print(r.text)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_tests():
    print("Waiting for server to start...")
    time.sleep(2) # Give server a moment if just started
    
    # 1. Health Check
    if not test_endpoint("Health Check", f"{BASE_URL}/"):
        print("Server not running or unreachable. Aborting tests.")
        return

    # 2. Weather
    test_endpoint("Weather (Pune)", f"{BASE_URL}/weather?city=Pune")

    # 3. Price
    test_endpoint("Price (Tomato)", f"{BASE_URL}/price?crop=Tomato")

    # 4. Soil
    test_endpoint("Soil Report", f"{BASE_URL}/soil")

    # 5. Crops
    test_endpoint("Get Crops", f"{BASE_URL}/crops")
    
    # 6. Add Crop
    test_endpoint("Add Crop", f"{BASE_URL}/crops/add", "POST", {"crop": "Test Crop", "plot": "Test Plot"})

    # 7. Finance Summary
    test_endpoint("Finance Summary", f"{BASE_URL}/expense/summary")

    # 8. Chatbot
    test_endpoint("Chatbot", f"{BASE_URL}/chatbot", "POST", {"question": "Is it good time to plant wheat?"})

    print("\nTests Completed.")

if __name__ == "__main__":
    run_tests()
