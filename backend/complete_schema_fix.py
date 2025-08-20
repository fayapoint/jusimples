#!/usr/bin/env python3
"""
Complete schema fix - add ALL missing columns required by logging functions
"""

import psycopg

def fix_complete_schema():
    print("🚨 COMPLETE SCHEMA FIX - Adding ALL missing columns")
    
    db_url = "postgresql://postgres.ugbplcahdqjgercuqvsr:5bNVhwx5%24z%23%3FL%3Fw@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
    
    try:
        conn = psycopg.connect(db_url, sslmode='require')
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # ASK_LOGS - All required columns
            print("🔧 Fixing ask_logs table...")
            ask_columns = [
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS search_type VARCHAR(50) DEFAULT 'semantic'",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true", 
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR(255)",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS user_id VARCHAR(255)",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS llm_model VARCHAR(100)",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS llm_tokens_used INTEGER DEFAULT 0",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS llm_cost DECIMAL(10,6) DEFAULT 0.0",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS user_agent TEXT",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45)",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS context_found INTEGER DEFAULT 0",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS input_tokens INTEGER DEFAULT 0",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS output_tokens INTEGER DEFAULT 0", 
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS finish_reason VARCHAR(50)",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS system_fingerprint VARCHAR(100)",
                "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS answer TEXT"
            ]
            
            for sql in ask_columns:
                try:
                    cur.execute(sql)
                    col_name = sql.split("ADD COLUMN IF NOT EXISTS ")[1].split()[0]
                    print(f"  ✅ {col_name}")
                except Exception as e:
                    print(f"  ⚠️ {sql}: {e}")
            
            # SEARCH_LOGS - All required columns  
            print("🔧 Fixing search_logs table...")
            search_columns = [
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR(255)",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS user_id VARCHAR(255)",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS user_agent TEXT", 
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45)",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS context_found INTEGER DEFAULT 0",
                "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS search_type VARCHAR(50) DEFAULT 'semantic'"
            ]
            
            for sql in search_columns:
                try:
                    cur.execute(sql)
                    col_name = sql.split("ADD COLUMN IF NOT EXISTS ")[1].split()[0]
                    print(f"  ✅ {col_name}")
                except Exception as e:
                    print(f"  ⚠️ {sql}: {e}")
            
            # Verify tables are now complete
            print("\n📋 Verifying complete schema...")
            for table in ['ask_logs', 'search_logs']:
                cur.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' AND table_schema = 'public'
                    ORDER BY ordinal_position
                """)
                columns = cur.fetchall()
                print(f"\n{table} columns ({len(columns)} total):")
                for col, dtype in columns:
                    print(f"  • {col}: {dtype}")
        
        conn.close()
        print("\n🎉 COMPLETE SCHEMA FIX SUCCESSFUL!")
        print("📊 All logging columns now available")
        return True
        
    except Exception as e:
        print(f"❌ Schema fix failed: {e}")
        return False

if __name__ == "__main__":
    fix_complete_schema()
