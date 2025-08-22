import os
import sys
import logging
import psycopg
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

def fix_search_logs_schema():
    """
    Add missing 'category' column to search_logs table if it doesn't exist.
    This fixes the schema issue identified in the admin dashboard.
    """
    logger.info("🔧 Starting search_logs schema fix...")
    
    # Get database URL from environment
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.error("❌ No DATABASE_URL found in environment variables")
        return False
    
    try:
        # Connect to the database
        logger.info("📊 Connecting to database...")
        conn = psycopg.connect(db_url, sslmode='require')
        
        # Check if the category column exists
        with conn.cursor() as cur:
            # Check if column exists
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'search_logs' AND column_name = 'category'
            """)
            
            category_exists = cur.fetchone() is not None
            
            if category_exists:
                logger.info("✅ Category column already exists in search_logs table")
            else:
                logger.info("🔧 Adding category column to search_logs table...")
                cur.execute("ALTER TABLE search_logs ADD COLUMN category VARCHAR(100)")
                conn.commit()
                logger.info("✅ Successfully added category column to search_logs table")
            
            # Validate the column was added correctly
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'search_logs' AND column_name = 'category'
            """)
            
            result = cur.fetchone()
            if result:
                logger.info(f"✅ Verified column: {result[0]} with type {result[1]}")
            else:
                logger.error("❌ Failed to verify the category column was added")
                
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error fixing search_logs schema: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_search_logs_schema()
    if success:
        logger.info("✅ Schema fix completed successfully")
    else:
        logger.error("❌ Schema fix failed")
        sys.exit(1)
