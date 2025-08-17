#!/usr/bin/env python3
"""
Comprehensive OpenAI API Key Test
Tests all aspects of OpenAI integration to identify issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_comprehensive():
    """Test OpenAI API key comprehensively"""
    
    print("=== OpenAI API Comprehensive Test ===\n")
    
    # 1. Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"1. API Key Check:")
    print(f"   - Exists: {'Yes' if api_key else 'No'}")
    print(f"   - Length: {len(api_key) if api_key else 0}")
    print(f"   - Format: {'sk-...' if api_key and api_key.startswith('sk-') else 'Invalid format'}")
    print(f"   - First 10 chars: {api_key[:10] if api_key else 'None'}")
    print()
    
    if not api_key or not api_key.startswith('sk-'):
        print("❌ API key is missing or has invalid format")
        return False
    
    # 2. Test OpenAI import
    print("2. OpenAI Library Import:")
    try:
        from openai import OpenAI
        print("   ✅ OpenAI library imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import OpenAI: {e}")
        return False
    print()
    
    # 3. Test client initialization
    print("3. Client Initialization:")
    try:
        client = OpenAI(api_key=api_key.strip())
        print("   ✅ OpenAI client created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create client: {type(e).__name__}: {e}")
        return False
    print()
    
    # 4. Test model list (to verify API key works)
    print("4. API Key Authentication Test:")
    try:
        models = client.models.list()
        print("   ✅ API key authenticated successfully")
        print(f"   - Available models count: {len(models.data)}")
        
        # Check for specific models
        model_names = [model.id for model in models.data]
        gpt4_models = [m for m in model_names if 'gpt-4' in m]
        gpt35_models = [m for m in model_names if 'gpt-3.5' in m]
        
        print(f"   - GPT-4 models: {len(gpt4_models)}")
        print(f"   - GPT-3.5 models: {len(gpt35_models)}")
        
        # Check for our target models
        target_models = ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']
        available_targets = [m for m in target_models if m in model_names]
        print(f"   - Target models available: {available_targets}")
        
    except Exception as e:
        print(f"   ❌ API authentication failed: {type(e).__name__}: {e}")
        return False
    print()
    
    # 5. Test specific model (gpt-4o-mini)
    print("5. Model-Specific Test (gpt-4o-mini):")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("   ✅ gpt-4o-mini works successfully")
        print(f"   - Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"   ❌ gpt-4o-mini failed: {type(e).__name__}: {e}")
        
        # Try fallback model
        print("\n6. Fallback Model Test (gpt-3.5-turbo):")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print("   ✅ gpt-3.5-turbo works successfully")
            print(f"   - Response: {response.choices[0].message.content}")
            return "gpt-3.5-turbo"
        except Exception as e2:
            print(f"   ❌ gpt-3.5-turbo also failed: {type(e2).__name__}: {e2}")
            return False
    print()
    
    return "gpt-4o-mini"

if __name__ == "__main__":
    result = test_openai_comprehensive()
    
    print("\n=== Test Summary ===")
    if result:
        print(f"✅ OpenAI integration working with model: {result}")
    else:
        print("❌ OpenAI integration failed")
        
    print("\n=== Next Steps ===")
    if not result:
        print("1. Check API key in Railway environment variables")
        print("2. Verify API key has proper permissions")
        print("3. Check billing/usage limits")
    else:
        print("1. Update Railway OPENAI_MODEL environment variable")
        print("2. Restart Railway deployment")
        print("3. Test system again")
