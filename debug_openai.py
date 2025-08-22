#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the functions directly
from openai_utils import is_openai_available, get_completion, openai_manager
from app import generate_ai_response

def test_openai_direct():
    print("=== DIRECT OPENAI TEST ===")
    print(f"is_openai_available(): {is_openai_available()}")
    print(f"openai_manager: {openai_manager}")
    if openai_manager:
        print(f"openai_manager.api_key: {'SET' if openai_manager.api_key else 'NOT SET'}")
        print(f"openai_manager.active_model: {openai_manager.active_model}")
        print(f"openai_manager.client: {'SET' if openai_manager.client else 'NOT SET'}")
    
    # Test direct completion
    print("\n=== DIRECT COMPLETION TEST ===")
    if is_openai_available():
        try:
            result = get_completion(
                prompt="Responda em uma frase: O que é direito civil?",
                system_message="Você é um assistente jurídico.",
                temperature=0.3,
                max_tokens=100
            )
            print(f"get_completion() result: {result}")
        except Exception as e:
            print(f"get_completion() error: {e}")
    else:
        print("OpenAI not available, skipping direct completion test")
    
    # Test generate_ai_response function
    print("\n=== GENERATE AI RESPONSE TEST ===")
    try:
        response = generate_ai_response("O que é direito civil?", [])
        print(f"generate_ai_response() result: {response[:200]}...")
    except Exception as e:
        print(f"generate_ai_response() error: {e}")

if __name__ == "__main__":
    test_openai_direct()
