#!/usr/bin/env python3

import requests
import json
import time
from pathlib import Path

def test_api_endpoints():
    results = {}
    base_url = "http://localhost:5000"
    
    # Test debug endpoint
    try:
        response = requests.get(f"{base_url}/api/debug", timeout=10)
        results["debug"] = {
            "status": response.status_code,
            "data": response.json() if response.status_code == 200 else response.text
        }
    except Exception as e:
        results["debug"] = {"error": str(e)}
    
    # Test ask endpoint with a simple question
    try:
        payload = {
            "question": "O que é direito civil brasileiro?",
            "top_k": 3,
            "min_relevance": 0.3
        }
        response = requests.post(f"{base_url}/api/ask", json=payload, timeout=30)
        results["ask"] = {
            "status": response.status_code,
            "data": response.json() if response.status_code == 200 else response.text,
            "payload": payload
        }
    except Exception as e:
        results["ask"] = {"error": str(e)}
    
    # Test with the special "teste" trigger from the code
    try:
        payload = {
            "question": "Este é um teste do sistema OpenAI",
            "top_k": 3,
            "min_relevance": 0.3
        }
        response = requests.post(f"{base_url}/api/ask", json=payload, timeout=30)
        results["ask_teste"] = {
            "status": response.status_code,
            "data": response.json() if response.status_code == 200 else response.text,
            "payload": payload
        }
    except Exception as e:
        results["ask_teste"] = {"error": str(e)}
    
    # Write results to file
    output_file = Path("api_test_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results written to {output_file}")
    
    # Also print summary to console
    print("\n=== API TEST SUMMARY ===")
    for endpoint, result in results.items():
        print(f"\n{endpoint.upper()}:")
        if "error" in result:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  Status: {result['status']}")
            if endpoint == "debug" and result['status'] == 200:
                data = result['data']
                print(f"  OpenAI Available: {data.get('openai_client_available', 'Unknown')}")
                print(f"  Active Model: {data.get('active_model', 'Unknown')}")
                print(f"  API Key Configured: {data.get('api_key_configured', 'Unknown')}")
            elif endpoint in ["ask", "ask_teste"] and result['status'] == 200:
                data = result['data']
                answer = data.get('answer', 'No answer')
                print(f"  Answer Preview: {answer[:100]}...")
                # Check for fallback indicators
                if any(phrase in answer.lower() for phrase in ["não posso", "informações suficientes", "orientação jurídica"]):
                    print("  ⚠️  FALLBACK CONTENT DETECTED")
                elif "✅ VERSÃO" in answer:
                    print("  ✅ TEST RESPONSE DETECTED")
                else:
                    print("  ✅ Appears to be AI response")

if __name__ == "__main__":
    test_api_endpoints()
