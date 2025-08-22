import requests
import json
import sys

def test_ask_endpoint():
    url = "http://localhost:5000/api/ask"
    
    # Test question
    payload = {
        "question": "O que é direito civil?",
        "top_k": 3,
        "min_relevance": 0.3
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Testing {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print("-" * 50)
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Check for signs of fallback content
            answer = data.get('answer', '')
            if 'não posso' in answer.lower() or 'informações suficientes' in answer.lower():
                print("\n⚠️  FALLBACK DETECTED: Response seems to be fallback content")
            else:
                print("\n✅ Seems like a proper AI response")
                
        else:
            print("Response Text:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

def test_debug_endpoint():
    url = "http://localhost:5000/api/debug"
    try:
        print(f"\nTesting debug endpoint: {url}")
        response = requests.get(url, timeout=10)
        print(f"Debug Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Debug Info:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Debug Response: {response.text}")
    except Exception as e:
        print(f"Debug endpoint error: {e}")

if __name__ == "__main__":
    test_debug_endpoint()
    print("\n" + "="*80 + "\n")
    test_ask_endpoint()
