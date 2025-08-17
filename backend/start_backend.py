#!/usr/bin/env python3
"""
JuSimples Backend Startup Script
Initializes the RAG system and starts the Flask server
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("The system will run in limited mode without AI capabilities")
        logger.warning("Please set up your .env file based on .env.example")
    
    return len(missing_vars) == 0

def initialize_system():
    """Initialize the legal data collection system"""
    try:
        from data_collector import initialize_legal_data
        
        logger.info("Initializing legal data collection system...")
        success = initialize_legal_data()
        
        if success:
            logger.info("Legal data system initialized successfully")
        else:
            logger.warning("Legal data system initialization failed, using fallback data")
        
        return success
        
    except Exception as e:
        logger.error(f"Error initializing system: {str(e)}")
        return False

def start_server():
    """Start the Flask server"""
    try:
        from app import app
        
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV') == 'development'
        
        logger.info(f"Starting JuSimples API server on port {port}")
        logger.info(f"Debug mode: {debug}")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)

def main():
    """Main startup function"""
    logger.info("=" * 50)
    logger.info("JuSimples Legal AI Platform - Backend")
    logger.info("=" * 50)
    
    # Check environment
    env_ok = check_environment()
    
    # Initialize system
    init_ok = initialize_system()
    
    if not env_ok:
        logger.warning("Environment setup incomplete - some features may not work")
    
    if not init_ok:
        logger.warning("System initialization incomplete - using basic functionality")
    
    # Start server
    logger.info("Starting Flask server...")
    start_server()

if __name__ == "__main__":
    main()
