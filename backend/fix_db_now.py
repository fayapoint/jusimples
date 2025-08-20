import psycopg

# Direct database fix using hardcoded connection string
DATABASE_URL = "postgresql://postgres.ugbplcahdqjgercuqvsr:5bNVhwx5%24z%23%3FL%3Fw@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"

print("🚨 EMERGENCY SCHEMA FIX")
print("=" * 50)

try:
    print("🔄 Connecting to Supabase...")
    conn = psycopg.connect(DATABASE_URL, connect_timeout=30)
    conn.autocommit = True
    print("✅ Connected!")
    
    with conn.cursor() as cur:
        # Check existing tables and columns
        print("\n📋 Checking current schema...")
        cur.execute("""
            SELECT table_name, column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name IN ('search_logs', 'ask_logs')
            ORDER BY table_name, ordinal_position
        """)
        current_schema = cur.fetchall()
        for table, col in current_schema:
            print(f"  {table}.{col}")
        
        # Add missing columns with explicit SQL
        print("\n🔧 Adding missing columns...")
        
        fixes = [
            "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true",
            "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0",
            "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR(255)",
            "ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS user_id VARCHAR(255)",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true", 
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR(255)",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS user_id VARCHAR(255)",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS llm_model VARCHAR(255)",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS llm_tokens_used INTEGER DEFAULT 0",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS llm_cost DECIMAL(10,6) DEFAULT 0.0",
            "ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS answer TEXT"
        ]
        
        for sql in fixes:
            try:
                cur.execute(sql)
                print(f"✅ {sql}")
            except Exception as e:
                print(f"⚠️ {sql} -> {e}")
        
        # Update existing records
        print("\n🔄 Updating existing records...")
        cur.execute("UPDATE search_logs SET success = true WHERE success IS NULL")
        print(f"✅ Updated {cur.rowcount} search_logs records")
        
        cur.execute("UPDATE ask_logs SET success = true WHERE success IS NULL") 
        print(f"✅ Updated {cur.rowcount} ask_logs records")
        
        # Test the exact failing query
        print("\n🧪 Testing failing queries...")
        try:
            cur.execute("""
                SELECT created_at, success, response_time_ms 
                FROM search_logs 
                WHERE created_at > now() - interval '24 hours'
                LIMIT 1
            """)
            print("✅ search_logs query fixed!")
        except Exception as e:
            print(f"❌ search_logs still failing: {e}")
        
        try:
            cur.execute("""
                SELECT created_at, success, response_time_ms 
                FROM ask_logs 
                WHERE created_at > now() - interval '24 hours'  
                LIMIT 1
            """)
            print("✅ ask_logs query fixed!")
        except Exception as e:
            print(f"❌ ask_logs still failing: {e}")
    
    conn.close()
    print("\n🎉 SCHEMA FIX COMPLETED!")
    print("📝 Next: Restart Flask app with 'python app.py'")
    
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    print("Check Supabase connection and credentials")
