#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emergency Database Schema Fix for JuSimples Analytics
Adds missing columns and ensures proper query tracking
"""

import os
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_database_schema():
    """Fix all database schema issues for analytics"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found!")
        return False

    try:
        print("🔧 Connecting to database...")
        conn = psycopg.connect(db_url, sslmode='require', connect_timeout=30)
        conn.autocommit = True
        register_vector(conn)
        print("✅ Database connected")

        with conn.cursor() as cur:
            print("\n🔧 FIXING SEARCH_LOGS TABLE...")
            
            # Add missing columns to search_logs
            missing_search_columns = [
                ("user_id", "TEXT"),
                ("session_id", "TEXT"),
                ("response_time_ms", "INTEGER DEFAULT 0"),
                ("user_agent", "TEXT"),
                ("ip_address", "INET"),
                ("context_found", "INTEGER DEFAULT 0"),
                ("success", "BOOLEAN DEFAULT true")
            ]
            
            for col_name, col_type in missing_search_columns:
                try:
                    cur.execute(f"ALTER TABLE search_logs ADD COLUMN IF NOT EXISTS {col_name} {col_type}")
                    print(f"✅ Added search_logs.{col_name}")
                except Exception as e:
                    print(f"⚠️ search_logs.{col_name}: {e}")

            print("\n🔧 FIXING ASK_LOGS TABLE...")
            
            # Add missing columns to ask_logs
            missing_ask_columns = [
                ("answer", "TEXT"),
                ("user_id", "TEXT"),
                ("session_id", "TEXT"),
                ("response_time_ms", "INTEGER DEFAULT 0"),
                ("user_agent", "TEXT"),
                ("ip_address", "INET"),
                ("context_found", "INTEGER DEFAULT 0"),
                ("success", "BOOLEAN DEFAULT true"),
                ("search_type", "TEXT DEFAULT 'keyword'"),
                ("input_tokens", "INTEGER DEFAULT 0"),
                ("output_tokens", "INTEGER DEFAULT 0"),
                ("finish_reason", "TEXT"),
                ("system_fingerprint", "TEXT"),
                ("response_id", "TEXT"),
                ("created_timestamp", "INTEGER"),
                ("logprobs", "TEXT")
            ]
            
            for col_name, col_type in missing_ask_columns:
                try:
                    cur.execute(f"ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS {col_name} {col_type}")
                    print(f"✅ Added ask_logs.{col_name}")
                except Exception as e:
                    print(f"⚠️ ask_logs.{col_name}: {e}")

            print("\n🔧 CREATING ENHANCED ANALYTICS TABLES...")
            
            # User sessions tracking
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id BIGSERIAL PRIMARY KEY,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id TEXT,
                    started_at TIMESTAMPTZ DEFAULT now(),
                    last_activity TIMESTAMPTZ DEFAULT now(),
                    ip_address INET,
                    user_agent TEXT,
                    total_queries INTEGER DEFAULT 0,
                    total_time_seconds INTEGER DEFAULT 0,
                    pages_visited JSONB DEFAULT '[]'::jsonb,
                    ended_at TIMESTAMPTZ
                );
            """)
            print("✅ user_sessions table ready")

            # Query popularity and analytics
            cur.execute("""
                CREATE TABLE IF NOT EXISTS query_analytics (
                    id BIGSERIAL PRIMARY KEY,
                    query_normalized TEXT UNIQUE NOT NULL,
                    total_count INTEGER DEFAULT 1,
                    last_queried TIMESTAMPTZ DEFAULT now(),
                    avg_response_time_ms DECIMAL(10,2),
                    success_rate DECIMAL(5,2),
                    categories JSONB DEFAULT '[]'::jsonb,
                    related_queries JSONB DEFAULT '[]'::jsonb,
                    created_at TIMESTAMPTZ DEFAULT now(),
                    updated_at TIMESTAMPTZ DEFAULT now()
                );
            """)
            print("✅ query_analytics table ready")

            # OpenAI API usage tracking
            cur.execute("""
                CREATE TABLE IF NOT EXISTS openai_usage_logs (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TIMESTAMPTZ DEFAULT now(),
                    request_id TEXT,
                    model TEXT,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    total_tokens INTEGER,
                    cost DECIMAL(10,6),
                    finish_reason TEXT,
                    system_fingerprint TEXT,
                    response_time_ms INTEGER,
                    success BOOLEAN DEFAULT true,
                    error_message TEXT,
                    endpoint TEXT,
                    session_id TEXT,
                    user_id TEXT
                );
            """)
            print("✅ openai_usage_logs table ready")

            # LexML API integration tracking
            cur.execute("""
                CREATE TABLE IF NOT EXISTS lexml_api_logs (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TIMESTAMPTZ DEFAULT now(),
                    endpoint TEXT,
                    request_params JSONB,
                    response_data JSONB,
                    response_time_ms INTEGER,
                    success BOOLEAN DEFAULT true,
                    error_message TEXT,
                    documents_found INTEGER,
                    session_id TEXT,
                    user_id TEXT
                );
            """)
            print("✅ lexml_api_logs table ready")

            # Popular queries view
            cur.execute("""
                CREATE OR REPLACE VIEW popular_queries AS
                SELECT 
                    qa.query_normalized,
                    qa.total_count,
                    qa.success_rate,
                    qa.avg_response_time_ms,
                    qa.last_queried,
                    CASE 
                        WHEN qa.total_count >= 50 THEN 'Very Popular'
                        WHEN qa.total_count >= 20 THEN 'Popular'
                        WHEN qa.total_count >= 5 THEN 'Moderate'
                        ELSE 'Low'
                    END as popularity_level
                FROM query_analytics qa
                ORDER BY qa.total_count DESC, qa.last_queried DESC;
            """)
            print("✅ popular_queries view created")

            print("\n📋 VERIFYING SCHEMA...")
            
            # Verify all tables exist
            tables_to_check = [
                'legal_chunks', 'search_logs', 'ask_logs', 'user_sessions',
                'query_analytics', 'openai_usage_logs', 'lexml_api_logs'
            ]
            
            for table in tables_to_check:
                try:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cur.fetchone()[0]
                    print(f"✅ {table}: {count} records")
                except Exception as e:
                    print(f"❌ {table}: {e}")

        conn.close()
        print("\n🎉 DATABASE SCHEMA FIX COMPLETED!")
        return True
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

if __name__ == "__main__":
    print("Starting database schema fix...")
    success = fix_database_schema()
    if success:
        print("\n✅ Schema fix completed successfully!")
    else:
        print("\n❌ Schema fix failed!")
        exit(1)
