#!/usr/bin/env python3
"""
JuSimples Setup Script
Installs dependencies and initializes the system
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✓ {command}")
            return True
        else:
            logger.error(f"✗ {command}")
            logger.error(f"Error: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"✗ {command} - Exception: {str(e)}")
        return False

def setup_backend():
    """Set up the backend environment"""
    logger.info("Setting up backend...")
    
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Create virtual environment
    if not os.path.exists(os.path.join(backend_dir, 'venv')):
        logger.info("Creating virtual environment...")
        if not run_command('python -m venv venv', backend_dir):
            return False
    
    # Install dependencies
    logger.info("Installing Python dependencies...")
    pip_cmd = os.path.join(backend_dir, 'venv', 'Scripts', 'pip.exe')
    if not run_command(f'"{pip_cmd}" install -r requirements.txt', backend_dir):
        return False
    
    # Create .env file if it doesn't exist
    env_file = os.path.join(backend_dir, '.env')
    if not os.path.exists(env_file):
        logger.info("Creating .env file...")
        example_file = os.path.join(backend_dir, '.env.example')
        if os.path.exists(example_file):
            with open(example_file, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            logger.info("Please configure your API keys in backend/.env")
    
    return True

def setup_frontend():
    """Set up the frontend environment"""
    logger.info("Setting up frontend...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Install npm dependencies
    if not run_command('npm install', frontend_dir):
        return False
    
    return True

def main():
    """Main setup function"""
    logger.info("=" * 50)
    logger.info("JuSimples Setup")
    logger.info("=" * 50)
    
    # Setup backend
    if not setup_backend():
        logger.error("Backend setup failed")
        return False
    
    # Setup frontend
    if not setup_frontend():
        logger.error("Frontend setup failed")
        return False
    
    logger.info("=" * 50)
    logger.info("Setup completed successfully!")
    logger.info("=" * 50)
    logger.info("Next steps:")
    logger.info("1. Configure API keys in backend/.env")
    logger.info("2. Start backend: cd backend && python start_backend.py")
    logger.info("3. Start frontend: cd frontend && npm start")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
