#!/usr/bin/env python3
"""
Quick database connection test for JuSimples admin dashboard
"""
import os
import sys
import logging
from pathlib import Path

# Add current directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

from retrieval import init_pgvector, is_ready, get_db_status, admin_db_overview

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test the database connection and report status"""
    print("=" * 50)
    print("JuSimples Database Connection Test")
    print("=" * 50)
    
    # Check environment variables
    print("\n1. Environment Variables:")
    db_url = os.getenv("DATABASE_URL", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    use_semantic = os.getenv("USE_SEMANTIC_RETRIEVAL", "false").lower()
    
    print(f"   DATABASE_URL: {'✓ Set' if db_url else '✗ Not set'}")
    print(f"   OPENAI_API_KEY: {'✓ Set' if openai_key else '✗ Not set'}")
    print(f"   USE_SEMANTIC_RETRIEVAL: {use_semantic}")
    
    if db_url:
        # Mask sensitive info for display
        masked_url = "*****" + db_url[-30:] if len(db_url) > 30 else "[masked]"
        print(f"   DB URL (masked): {masked_url}")
    
    # Test connection initialization
    print("\n2. Database Connection Test:")
    try:
        print("   Attempting to initialize pgvector...")
        success = init_pgvector()
        print(f"   Connection initialization: {'✓ Success' if success else '✗ Failed'}")
        
        # Test if ready
        ready = is_ready()
        print(f"   Database ready: {'✓ Yes' if ready else '✗ No'}")
        
        if ready:
            print("\n3. Database Status:")
            status = get_db_status()
            print(f"   PostgreSQL Version: {status.get('version', 'unknown')}")
            print(f"   Database Name: {status.get('database_name', 'unknown')}")
            print(f"   User: {status.get('user', 'unknown')}")
            print(f"   Vector Extension: {'✓ Installed' if status.get('vector_ready') else '✗ Not available'}")
            print(f"   Extensions: {', '.join(status.get('extensions', []))}")
            
            print("\n4. Database Overview:")
            overview = admin_db_overview()
            counts = overview.get('counts', {})
            print(f"   Legal Chunks: {counts.get('legal_chunks', 0)}")
            print(f"   Search Logs: {counts.get('search_logs', 0)}")
            print(f"   Ask Logs: {counts.get('ask_logs', 0)}")
            
            categories = overview.get('categories', [])
            if categories:
                print(f"   Categories: {len(categories)} found")
                for cat in categories[:5]:  # Show top 5
                    print(f"     - {cat.get('category', 'Unknown')}: {cat.get('count', 0)} docs")
        else:
            print("\n3. Connection Failed - Admin Dashboard will use mock data")
            print("   This is why you're seeing sample/fake data instead of real data")
            
    except Exception as e:
        print(f"   ✗ Connection failed with error: {e}")
        print("   This explains why the admin dashboard is showing mock data")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_database_connection()
