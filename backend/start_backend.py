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
    logger.info("=== STARTING JUSIMPLES BACKEND ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Environment variables:")
    logger.info(f"  PORT: {os.getenv('PORT', 'Not set')}")
    logger.info(f"  OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    logger.info(f"  OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'Not set')}")
    
    logger.info("Importing Flask app...")
    from app import app, client, active_model
    logger.info("✅ Flask app imported successfully")
    logger.info(f"OpenAI client status: {'Available' if client else 'Not available'}")
    logger.info(f"Active model: {active_model or 'None'}")
    
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting Flask server on 0.0.0.0:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
    
except Exception as e:
    logger.error(f"❌ FAILED TO START APPLICATION: {str(e)}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Full traceback:\n{traceback.format_exc()}")
    sys.exit(1)
