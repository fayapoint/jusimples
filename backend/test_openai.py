#!/usr/bin/env python3
"""
Simple OpenAI connection test script
Run this to verify OpenAI API key is working
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    print("=== OpenAI Connection Test ===")
    print(f"API Key Status: {'SET' if api_key and api_key != 'your_openai_api_key_here' else 'NOT SET'}")
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello from JuSimples!'"}],
            max_tokens=50
        )
        
        print(f"✅ API call successful: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection()
