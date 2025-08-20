#!/usr/bin/env python3
"""
Emergency schema fix for analytics tables
This script MUST run successfully to fix the dashboard
"""

import os
import sys

def emergency_fix():
    try:
        import psycopg
        
        # Get database URL
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("❌ DATABASE_URL not found")
            return False
        
        print("🚨 EMERGENCY SCHEMA FIX STARTING...")
        
        # Connect to database
        conn = psycopg.connect(db_url, sslmode='require', connect_timeout=30)
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Check if tables exist first
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('search_logs', 'ask_logs')
            """)
            tables = [row[0] for row in cur.fetchall()]
            print(f"Found tables: {tables}")
            
            # Add columns with explicit error handling
            sql_commands = [
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0", 
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0"
            ]
            
            for sql in sql_commands:
                try:
                    cur.execute(sql)
                    print(f"✅ {sql}")
                except Exception as e:
                    print(f"⚠️ {sql} -> {e}")
            
            # Verify the fix worked
            print("\n🔍 VERIFICATION:")
            for table in ['search_logs', 'ask_logs']:
                if table in tables:
                    try:
                        # Test the success column query that's failing
                        cur.execute(f"SELECT created_at, success, response_time_ms FROM {table} LIMIT 1")
                        print(f"✅ {table} success column query works!")
                    except Exception as e:
                        print(f"❌ {table} still broken: {e}")
                        return False
        
        conn.close()
        print("\n🎉 EMERGENCY FIX COMPLETED!")
        return True
        
    except Exception as e:
        print(f"❌ EMERGENCY FIX FAILED: {e}")
        return False

if __name__ == "__main__":
    if emergency_fix():
        print("✅ SUCCESS - Restart Flask app now!")
        sys.exit(0)
    else:
        print("❌ FAILED - Check errors above")
        sys.exit(1)
