#!/usr/bin/env python3
"""
Database Schema Migration Script for Analytics Tables
Fixes missing columns and schema issues for JuSimples analytics dashboard.
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_analytics_schema():
    """Fix analytics database schema issues"""
    try:
        # Import database connection
        from retrieval import get_connection
        
        logger.info("🔧 Starting analytics schema migration...")
        
        # Get database connection
        conn = get_connection()
        if not conn:
            logger.error("❌ Failed to connect to database")
            return False
            
        cur = conn.cursor()
        
        # Check current schema
        logger.info("📋 Checking current database schema...")
        
        # Fix search_logs table
        logger.info("🔍 Checking search_logs table...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'search_logs' AND table_schema = 'public'
        """)
        search_cols = [row[0] for row in cur.fetchall()]
        logger.info(f"Current search_logs columns: {search_cols}")
        
        # Add missing columns to search_logs
        missing_search_cols = {
            'success': 'BOOLEAN DEFAULT true',
            'response_time_ms': 'INTEGER DEFAULT 0',
            'session_id': 'VARCHAR(255)',
            'user_id': 'VARCHAR(255)',
            'user_agent': 'TEXT',
            'ip_address': 'VARCHAR(45)',
            'context_found': 'INTEGER DEFAULT 0'
        }
        
        for col_name, col_def in missing_search_cols.items():
            if col_name not in search_cols:
                try:
                    cur.execute(f"ALTER TABLE search_logs ADD COLUMN {col_name} {col_def}")
                    logger.info(f"✅ Added column {col_name} to search_logs")
                except Exception as e:
                    logger.warning(f"⚠️ Could not add {col_name} to search_logs: {e}")
        
        # Fix ask_logs table
        logger.info("🔍 Checking ask_logs table...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'ask_logs' AND table_schema = 'public'
        """)
        ask_cols = [row[0] for row in cur.fetchall()]
        logger.info(f"Current ask_logs columns: {ask_cols}")
        
        # Add missing columns to ask_logs
        missing_ask_cols = {
            'success': 'BOOLEAN DEFAULT true',
            'response_time_ms': 'INTEGER DEFAULT 0',
            'session_id': 'VARCHAR(255)',
            'user_id': 'VARCHAR(255)',
            'user_agent': 'TEXT',
            'ip_address': 'VARCHAR(45)',
            'context_found': 'INTEGER DEFAULT 0',
            'llm_model': 'VARCHAR(255)',
            'llm_tokens_used': 'INTEGER DEFAULT 0',
            'llm_cost': 'DECIMAL(10,6) DEFAULT 0.0',
            'answer': 'TEXT'
        }
        
        for col_name, col_def in missing_ask_cols.items():
            if col_name not in ask_cols:
                try:
                    cur.execute(f"ALTER TABLE ask_logs ADD COLUMN {col_name} {col_def}")
                    logger.info(f"✅ Added column {col_name} to ask_logs")
                except Exception as e:
                    logger.warning(f"⚠️ Could not add {col_name} to ask_logs: {e}")
        
        # Create API usage logs table if not exists
        logger.info("🔍 Creating API usage logs table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS api_usage_logs (
                id SERIAL PRIMARY KEY,
                api_name VARCHAR(255) NOT NULL,
                endpoint VARCHAR(255),
                success BOOLEAN DEFAULT true,
                response_time_ms INTEGER DEFAULT 0,
                cost DECIMAL(10,6) DEFAULT 0.0,
                error_message TEXT,
                request_data JSONB,
                response_data JSONB,
                user_agent TEXT,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logger.info("✅ API usage logs table ready")
        
        # Update existing records with default values
        logger.info("🔄 Updating existing records with default values...")
        
        # Update search_logs records without success values
        cur.execute("UPDATE search_logs SET success = true WHERE success IS NULL")
        updated_search = cur.rowcount
        logger.info(f"✅ Updated {updated_search} search_logs records")
        
        # Update ask_logs records without success values  
        cur.execute("UPDATE ask_logs SET success = true WHERE success IS NULL")
        updated_ask = cur.rowcount
        logger.info(f"✅ Updated {updated_ask} ask_logs records")
        
        # Create indexes for better performance
        logger.info("📊 Creating performance indexes...")
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_search_logs_created_at ON search_logs(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_search_logs_success ON search_logs(success)",
            "CREATE INDEX IF NOT EXISTS idx_search_logs_session ON search_logs(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_ask_logs_created_at ON ask_logs(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_ask_logs_success ON ask_logs(success)", 
            "CREATE INDEX IF NOT EXISTS idx_ask_logs_session ON ask_logs(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_api_usage_created_at ON api_usage_logs(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_api_usage_api_name ON api_usage_logs(api_name)"
        ]
        
        for idx_sql in indexes:
            try:
                cur.execute(idx_sql)
                logger.info(f"✅ Created index: {idx_sql.split()[-1]}")
            except Exception as e:
                logger.warning(f"⚠️ Could not create index: {e}")
        
        # Commit all changes
        conn.commit()
        logger.info("✅ All schema changes committed successfully")
        
        # Close connections
        cur.close()
        conn.close()
        
        logger.info("🎉 Analytics schema migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Schema migration failed: {e}")
        return False

def main():
    """Main migration function"""
    logger.info("🚀 JuSimples Analytics Schema Migration Tool")
    logger.info("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('retrieval.py'):
        logger.error("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    # Run the migration
    success = fix_analytics_schema()
    
    if success:
        logger.info("✅ Migration completed successfully!")
        logger.info("📝 You can now restart the Flask app to use the updated schema")
    else:
        logger.error("❌ Migration failed. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
