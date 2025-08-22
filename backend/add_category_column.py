#!/usr/bin/env python3
"""
Add missing category column to search_logs table
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import database connection from db_utils
from db_utils import get_db_manager

def add_category_column():
    """Add the category column to search_logs table if it doesn't exist."""
    logger.info("Adding category column to search_logs table...")
    
    # Get database manager
    db_manager = get_db_manager()
    
    if not db_manager or not db_manager.is_ready():
        logger.error("Database connection not ready")
        return False
    
    try:
        conn = db_manager.get_connection()
        with conn.cursor() as cur:
            # Check if the column exists
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'search_logs' AND column_name = 'category'
            """)
            
            column_exists = cur.fetchone() is not None
            
            if column_exists:
                logger.info("✅ Category column already exists in search_logs table")
            else:
                logger.info("Adding 'category' column to search_logs table...")
                cur.execute("ALTER TABLE search_logs ADD COLUMN category VARCHAR(100)")
                conn.commit()
                logger.info("✅ Successfully added category column to search_logs table")
                
                # Verify column was added
                cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'search_logs' AND column_name = 'category'
                """)
                result = cur.fetchone()
                if result:
                    logger.info(f"✅ Verified column: {result[0]} with type {result[1]}")
                else:
                    logger.error("❌ Failed to verify column was added")
                    return False
        
        return True
    
    except Exception as e:
        logger.error(f"Error adding category column: {e}")
        return False

if __name__ == "__main__":
    success = add_category_column()
    if success:
        print("✅ Category column added or already exists in search_logs table")
    else:
        print("❌ Failed to add category column to search_logs table")
        sys.exit(1)
