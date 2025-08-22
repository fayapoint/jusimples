#!/usr/bin/env python3

import sys
import os
import time
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

def test_openai_flow():
    try:
        # Import after adding to path
        from openai_utils import is_openai_available, get_completion, openai_manager
        from app import generate_ai_response
        
        # Test 1: Check if OpenAI is available
        available = is_openai_available()
        print(f"OpenAI Available: {available}")
        
        if openai_manager:
            print(f"OpenAI Manager Active Model: {openai_manager.active_model}")
            print(f"OpenAI Manager API Key Set: {'Yes' if openai_manager.api_key else 'No'}")
            print(f"OpenAI Manager Client Ready: {'Yes' if openai_manager.client else 'No'}")
            print(f"OpenAI Manager Ready Status: {openai_manager.is_ready()}")
        
        # Test 2: Direct completion test
        if available:
            print("\n=== Testing Direct Completion ===")
            result = get_completion(
                prompt="Responda em uma frase: O que é direito civil brasileiro?",
                system_message="Você é um assistente jurídico.",
                temperature=0.3,
                max_tokens=150
            )
            print(f"Direct completion success: {result.get('success', False)}")
            if result.get('success'):
                print(f"Response: {result.get('content', 'No content')[:200]}...")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Test 3: Test generate_ai_response function
        print("\n=== Testing generate_ai_response ===")
        test_response = generate_ai_response(
            "O que é direito civil brasileiro?",
            [{"title": "Direito Civil", "content": "O direito civil regula as relações privadas entre pessoas físicas e jurídicas."}]
        )
        
        print(f"Generate AI Response: {test_response[:300]}...")
        
        # Check if it's fallback content
        if "não posso" in test_response.lower() or "informações suficientes" in test_response.lower():
            print("⚠️  FALLBACK CONTENT DETECTED!")
        elif "Erro" in test_response:
            print("❌ ERROR RESPONSE DETECTED!")
        else:
            print("✅ Appears to be real AI response")
            
    except Exception as e:
        print(f"Test failed: {type(e).__name__}: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_openai_flow()
