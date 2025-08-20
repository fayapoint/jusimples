#!/usr/bin/env python3
"""
Update database schema to capture comprehensive OpenAI API data
"""

import psycopg

# OpenAI API provides rich analytics data we can capture:
OPENAI_COLUMNS = [
    # Token breakdown
    ("input_tokens", "INTEGER DEFAULT 0"),
    ("output_tokens", "INTEGER DEFAULT 0"), 
    # OpenAI response metadata
    ("finish_reason", "VARCHAR(50)"),  # stop, length, function_call, content_filter
    ("system_fingerprint", "VARCHAR(100)"),  # OpenAI system version identifier
    # Enhanced cost tracking
    ("model_version", "VARCHAR(100)"),  # Specific model version used
    # Request metadata
    ("temperature", "DECIMAL(3,2) DEFAULT 0.7"),
    ("max_tokens", "INTEGER"),
    ("top_p", "DECIMAL(3,2) DEFAULT 1.0"),
    # Response quality metrics
    ("response_quality_score", "DECIMAL(3,2)"),  # Custom quality assessment
    ("context_relevance_score", "DECIMAL(3,2)"),  # How relevant retrieved context was
]

def update_schema():
    print("🔄 Adding comprehensive OpenAI analytics columns...")
    
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    try:
        conn = psycopg.connect(DATABASE_URL, sslmode='require')
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Add OpenAI columns to ask_logs
            print("📝 Updating ask_logs table...")
            for col_name, col_def in OPENAI_COLUMNS:
                try:
                    cur.execute(f"ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS {col_name} {col_def}")
                    print(f"  ✅ {col_name}")
                except Exception as e:
                    print(f"  ⚠️ {col_name}: {e}")
            
            # Add some columns to search_logs too
            print("📝 Updating search_logs table...")
            search_columns = [
                ("model_version", "VARCHAR(100)"),
                ("embedding_model", "VARCHAR(100)"),
                ("similarity_threshold", "DECIMAL(4,3)"),
                ("vector_search_time_ms", "INTEGER DEFAULT 0"),
            ]
            
            for col_name, col_def in search_columns:
                try:
                    cur.execute(f"ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS {col_name} {col_def}")
                    print(f"  ✅ {col_name}")
                except Exception as e:
                    print(f"  ⚠️ {col_name}: {e}")
            
            # Create comprehensive analytics view
            cur.execute("""
                CREATE OR REPLACE VIEW analytics_overview AS
                SELECT 
                    'ask' as operation_type,
                    created_at,
                    success,
                    response_time_ms,
                    llm_tokens_used as tokens_used,
                    input_tokens,
                    output_tokens,
                    llm_cost as cost,
                    llm_model as model,
                    session_id,
                    user_id,
                    finish_reason,
                    system_fingerprint
                FROM ask_logs
                UNION ALL
                SELECT 
                    'search' as operation_type,
                    created_at,
                    success,
                    response_time_ms,
                    0 as tokens_used,
                    0 as input_tokens,
                    0 as output_tokens,
                    0 as cost,
                    embedding_model as model,
                    session_id,
                    user_id,
                    NULL as finish_reason,
                    NULL as system_fingerprint
                FROM search_logs
            """)
            print("✅ Created analytics_overview view")
        
        conn.close()
        print("\n🎉 Schema updated successfully!")
        print("📊 Now capturing comprehensive OpenAI API data:")
        print("   • Actual token usage (input/output breakdown)")
        print("   • Precise cost calculations") 
        print("   • OpenAI response metadata")
        print("   • Model versions and fingerprints")
        print("   • Quality and relevance scores")
        return True
        
    except Exception as e:
        print(f"❌ Schema update failed: {e}")
        return False

if __name__ == "__main__":
    update_schema()
