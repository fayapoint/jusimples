#!/usr/bin/env python3
"""
JuSimples Backend Startup Script - Railway Compatible
"""

import os
import sys
import logging

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

try:
    logger.info("Starting JuSimples backend...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Files in directory: {os.listdir('.')}")
    
    from app import app
    logger.info("Flask app imported successfully")
    
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
    
except Exception as e:
    logger.error(f"Failed to start application: {str(e)}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)
