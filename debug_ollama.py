#!/usr/bin/env python3
"""
Debug Ollama API
Test trực tiếp Ollama API để tìm vấn đề
"""

import requests
import json

def test_ollama_api():
    """Test Ollama API trực tiếp"""
    print("🔧 Debug Ollama API")
    print("=" * 40)
    
    # Test 1: Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"✅ Ollama status: {response.status_code}")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"📦 Models available: {len(models)}")
            for model in models:
                print(f"   - {model.get('name', 'Unknown')}")
    except Exception as e:
        print(f"❌ Ollama not running: {e}")
        return
    
    # Test 2: Test generate API
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "gpt_assistant:latest",
        "prompt": "RSI là gì?",
        "stream": False
    }
    
    print(f"\n🔍 Testing generate API...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=180)  # 3 minutes
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            answer = result.get("response", "")
            if answer:
                print(f"✅ Success! Answer: {answer[:100]}...")
            else:
                print("❌ Empty response")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ollama_api() 