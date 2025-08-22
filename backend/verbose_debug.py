#!/usr/bin/env python3

# Print immediate output before any imports
print("Starting verbose debug script...")
print("This is a test of Python execution")

import os
import sys
import time

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("Environment variables:", [k for k in os.environ.keys() if not k.startswith('_')])
print("DATABASE_URL configured:", bool(os.environ.get('DATABASE_URL')))
print("OPENAI_API_KEY configured:", bool(os.environ.get('OPENAI_API_KEY')))

try:
    # Try to load dotenv
    print("Attempting to load dotenv...")
    from dotenv import load_dotenv
    load_dotenv()
    print(".env loaded successfully")
except ImportError:
    print("dotenv not available")
except Exception as e:
    print(f"Error loading .env: {e}")

# Always print this output regardless of errors
print("Script completed")
