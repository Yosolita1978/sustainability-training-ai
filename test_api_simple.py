import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test API health"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_training():
    """Test training session"""
    training_request = {
        "industry": "Marketing Agency",
        "regulations": "EU (Green Claims Directive, CSRD)", 
        "difficulty": "Intermediate"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/training/start",
            json=training_request
        )
        print(f"Training start: {response.status_code}")
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data["session_id"]
            print(f"Session ID: {session_id}")
            return session_id
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Training start failed: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing Sustainability API...")
    
    if test_health():
        print("✅ Health check passed")
        session_id = test_training()
        if session_id:
            print(f"✅ Training started: {session_id}")
        else:
            print("❌ Training failed to start")
    else:
        print("❌ Health check failed")