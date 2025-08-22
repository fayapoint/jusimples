#!/usr/bin/env python3
"""
Quick database connection test for JuSimples admin dashboard
"""
import os
import sys
import logging
import json
from pathlib import Path

# Add current directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

# Import from our new db_utils module
try:
    from backend.db_utils import get_db_manager, is_ready, initialize_schema
except ImportError:
    from db_utils import get_db_manager, is_ready, initialize_schema

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test the database connection and report status"""
    print("=" * 50)
    print("JuSimples Database Connection Test (Using db_utils)")
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
        # Get database manager instance
        db_manager = get_db_manager()
        print("   Attempting to initialize database schema...")
        success = initialize_schema()
        print(f"   Schema initialization: {'✓ Success' if success else '✗ Failed'}")
        
        # Test if ready
        ready = is_ready()
        print(f"   Database ready: {'✓ Yes' if ready else '✗ No'}")
        
        if ready:
            print("\n3. Database Status:")
            # Get database status
            try:
                conn = db_manager.get_connection()
                with conn.cursor() as cur:
                    # Get PostgreSQL version
                    cur.execute("SELECT version();")
                    version_info = cur.fetchone()
                    version = version_info[0] if version_info else "unknown"
                    print(f"   PostgreSQL Version: {version}")
                    
                    # Get database name and user
                    cur.execute("SELECT current_database(), current_user;")
                    db_info = cur.fetchone()
                    if db_info:
                        print(f"   Database Name: {db_info[0]}")
                        print(f"   User: {db_info[1]}")
                    
                    # Check vector extension
                    cur.execute("SELECT name FROM pg_available_extensions WHERE installed_version IS NOT NULL AND name = 'vector';")
                    vector_available = cur.fetchone() is not None
                    print(f"   Vector Extension: {'✓ Installed' if vector_available else '✗ Not available'}")
                    
                    # List extensions
                    cur.execute("SELECT name FROM pg_available_extensions WHERE installed_version IS NOT NULL;")
                    extensions = [ext[0] for ext in cur.fetchall()]
                    print(f"   Extensions: {', '.join(extensions)}")
            except Exception as e:
                print(f"   Could not fetch database status: {e}")
            
            print("\n4. Database Overview:")
            overview = db_manager.admin_db_overview()
            counts = overview.get('counts', {})
            print(f"   Legal Chunks: {counts.get('legal_chunks', 0)}")
            print(f"   Search Logs: {counts.get('search_logs', 0)}")
            print(f"   Ask Logs: {counts.get('ask_logs', 0)}")
            
            # Check vector status
            vector_status = overview.get('vector_status', {})
            print(f"   Vector Status:")
            print(f"     - Embedded Documents: {vector_status.get('embedded_docs', 0)}")
            print(f"     - Missing Embeddings: {vector_status.get('missing_embeddings', 0)}")
            print(f"     - Embedding Coverage: {vector_status.get('embedding_coverage', 0)}%")
            
            # Get recent queries
            recent_queries = overview.get('recent_queries', [])
            if recent_queries:
                print(f"   Recent Queries: {len(recent_queries)} found")
                for i, query in enumerate(recent_queries[:3]):
                    status = "✓" if query.get('success', True) else "✗"
                    print(f"     - {status} {query.get('query', 'Unknown')}")
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
