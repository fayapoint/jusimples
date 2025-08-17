#!/usr/bin/env python3
"""
JuSimples Backend Startup Script - Simplified Version
"""

import os
from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
