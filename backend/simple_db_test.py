import os
import psycopg
from pgvector.psycopg import register_vector

# URGENT: Fix analytics schema to resolve dashboard errors
db_url = os.getenv("DATABASE_URL")
print(f"DATABASE_URL exists: {bool(db_url)}")

if db_url:
    try:
        conn = psycopg.connect(db_url, sslmode='require', connect_timeout=30)
        print("✅ Database connected")
        
        conn.autocommit = True
        register_vector(conn)
        
        with conn.cursor() as cur:
            print("🔧 FORCE ADDING MISSING COLUMNS...")
            
            # Force add missing columns with proper error handling
            try:
                cur.execute("ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true")
                print("✅ search_logs.success column ensured")
            except Exception as e:
                print(f"⚠️ search_logs.success: {e}")
            
            try:
                cur.execute("ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0")
                print("✅ search_logs.response_time_ms column ensured")
            except Exception as e:
                print(f"⚠️ search_logs.response_time_ms: {e}")
            
            try:
                cur.execute("ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT true")
                print("✅ ask_logs.success column ensured")
            except Exception as e:
                print(f"⚠️ ask_logs.success: {e}")
            
            try:
                cur.execute("ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS response_time_ms INTEGER DEFAULT 0")
                print("✅ ask_logs.response_time_ms column ensured")
            except Exception as e:
                print(f"⚠️ ask_logs.response_time_ms: {e}")
            
            # Verify columns exist now
            print("\n📋 VERIFYING SCHEMA:")
            for table in ['search_logs', 'ask_logs']:
                try:
                    cur.execute(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}' AND table_schema = 'public'
                        AND column_name IN ('success', 'response_time_ms')
                    """)
                    cols = [row[0] for row in cur.fetchall()]
                    print(f"✅ {table} has columns: {cols}")
                    
                    # Test query with success column
                    cur.execute(f"SELECT COUNT(*) FROM {table} WHERE success IS NOT NULL")
                    count = cur.fetchone()[0]
                    print(f"✅ {table} success column working: {count} records")
                    
                except Exception as e:
                    print(f"❌ {table} verification failed: {e}")
        
        conn.close()
        print("\n🎉 SCHEMA FIX COMPLETED - RESTART FLASK APP!")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
else:
    print("❌ No DATABASE_URL found!")
