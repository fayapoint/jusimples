#!/usr/bin/env python3
"""
WSGI entry point for JuSimples backend
Production-ready Flask application
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from app import app

# Initialize data collection system
try:
    from data_collector import initialize_legal_data
    initialize_legal_data()
except Exception as e:
    print(f"Warning: Legal data initialization failed: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
