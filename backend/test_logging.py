#!/usr/bin/env python3
"""
Test logging functions to see why data isn't being saved
"""

import os
import psycopg
import time
from retrieval_extensions import log_ask_advanced, log_search_advanced

def test_database_logging():
    print("🔍 Testing database logging functionality...")
    
    # Connect to database - use direct URL
    db_url = "postgresql://postgres.ugbplcahdqjgercuqvsr:5bNVhwx5%24z%23%3FL%3Fw@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
    
    if not db_url:
        print("❌ No DATABASE_URL found")
        return False
    
    try:
        conn = psycopg.connect(db_url, sslmode='require')
        print("✅ Database connected")
        
        # Check if tables exist and their structure
        with conn.cursor() as cur:
            print("\n📋 Checking table structure...")
            
            for table in ['search_logs', 'ask_logs']:
                cur.execute(f"""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' AND table_schema = 'public'
                    ORDER BY ordinal_position
                """)
                columns = cur.fetchall()
                print(f"\n{table} columns:")
                for col, dtype, nullable in columns:
                    print(f"  - {col}: {dtype} {'(nullable)' if nullable == 'YES' else ''}")
                
                # Check current record count
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"  📊 Current records: {count}")
        
        # Test manual logging
        print("\n🧪 Testing manual logging...")
        
        # Test search logging
        test_result = log_search_advanced(
            query="test query from logging test",
            top_k=5,
            min_relevance=0.7,
            result_ids=["test1", "test2"],
            search_type="semantic",
            success=True,
            session_id="test_session_123",
            user_id="test_user",
            response_time_ms=150,
            user_agent="test_agent",
            ip_address="127.0.0.1",
            context_found=2,
            conn=conn
        )
        print(f"Search logging result: {test_result}")
        
        # Test ask logging
        test_result2 = log_ask_advanced(
            question="test question from logging test",
            answer="test answer",
            top_k=5,
            min_relevance=0.7,
            result_ids=["test1", "test2"],
            search_type="semantic",
            success=True,
            session_id="test_session_123",
            user_id="test_user",
            response_time_ms=200,
            llm_model="gpt-4o-mini",
            llm_tokens_used=150,
            llm_cost=0.0025,
            user_agent="test_agent",
            ip_address="127.0.0.1",
            context_found=2,
            conn=conn
        )
        print(f"Ask logging result: {test_result2}")
        
        # Check if records were inserted
        print("\n📊 Checking if test records were inserted...")
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM search_logs WHERE query LIKE '%test query from logging test%'")
            search_count = cur.fetchone()[0]
            print(f"Test search records found: {search_count}")
            
            cur.execute("SELECT COUNT(*) FROM ask_logs WHERE question LIKE '%test question from logging test%'")
            ask_count = cur.fetchone()[0]
            print(f"Test ask records found: {ask_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_database_logging()
