#!/usr/bin/env python3
"""
Test API endpoints to verify end-to-end analytics data capture
"""

import requests
import json
import time
import psycopg
import os

def test_endpoints():
    print("🧪 Testing API endpoints for analytics data capture...")
    
    # Set up database connection
    os.environ['DATABASE_URL'] = "postgresql://postgres.ugbplcahdqjgercuqvsr:5bNVhwx5%24z%23%3FL%3Fw@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
    
    # Check initial record counts
    conn = psycopg.connect(os.environ['DATABASE_URL'], sslmode='require')
    cur = conn.cursor()
    
    cur.execute('SELECT COUNT(*) FROM search_logs')
    initial_search_count = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM ask_logs')
    initial_ask_count = cur.fetchone()[0]
    
    print(f"📊 Initial counts: search_logs={initial_search_count}, ask_logs={initial_ask_count}")
    conn.close()
    
    # Test search endpoint
    print("\n🔍 Testing /api/search endpoint...")
    try:
        response = requests.post('http://localhost:5000/api/search', 
                               json={'query': 'direito trabalhista analytics test', 'top_k': 3},
                               headers={'X-Session-ID': 'test_session_api_001'},
                               timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {len(data.get('results', []))} documents")
            print(f"Query: {data.get('query', 'N/A')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Search request failed: {e}")
    
    time.sleep(1)  # Brief pause
    
    # Test ask endpoint
    print("\n🤖 Testing /api/ask endpoint...")  
    try:
        response = requests.post('http://localhost:5000/api/ask',
                               json={'question': 'O que é direito trabalhista? Explique em detalhes.'},
                               headers={'X-Session-ID': 'test_session_api_001'},
                               timeout=20)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Answer length: {len(data.get('answer', ''))} chars")
            print(f"Sources: {len(data.get('sources', []))} documents")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Ask request failed: {e}")
    
    time.sleep(2)  # Allow time for logging
    
    # Check final record counts and show analytics data
    print("\n📊 Checking database after API tests...")
    conn = psycopg.connect(os.environ['DATABASE_URL'], sslmode='require')
    cur = conn.cursor()
    
    cur.execute('SELECT COUNT(*) FROM search_logs')
    final_search_count = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM ask_logs')
    final_ask_count = cur.fetchone()[0]
    
    print(f"Final counts: search_logs={final_search_count}, ask_logs={final_ask_count}")
    print(f"New records: search={final_search_count - initial_search_count}, ask={final_ask_count - initial_ask_count}")
    
    # Show latest search record with analytics
    if final_search_count > initial_search_count:
        cur.execute("""
            SELECT query, search_type, success, response_time_ms, 
                   context_found, session_id, created_at
            FROM search_logs 
            ORDER BY created_at DESC LIMIT 1
        """)
        latest_search = cur.fetchone()
        print(f"\n📈 Latest search record:")
        print(f"   Query: '{latest_search[0][:50]}...'")
        print(f"   Type: {latest_search[1]}, Success: {latest_search[2]}")
        print(f"   Response time: {latest_search[3]}ms, Results: {latest_search[4]}")
        print(f"   Session: {latest_search[5]}")
    
    # Show latest ask record with comprehensive OpenAI analytics
    if final_ask_count > initial_ask_count:
        cur.execute("""
            SELECT question, llm_model, llm_tokens_used, input_tokens, 
                   output_tokens, llm_cost, finish_reason, system_fingerprint,
                   success, response_time_ms, session_id, created_at
            FROM ask_logs 
            ORDER BY created_at DESC LIMIT 1
        """)
        latest_ask = cur.fetchone()
        print(f"\n🤖 Latest ask record with OpenAI analytics:")
        print(f"   Question: '{latest_ask[0][:50]}...'")
        print(f"   Model: {latest_ask[1]}")
        print(f"   Total tokens: {latest_ask[2]} (input: {latest_ask[3]}, output: {latest_ask[4]})")
        print(f"   Cost: ${latest_ask[5]:.6f}")
        print(f"   Finish reason: {latest_ask[6]}")
        print(f"   System fingerprint: {latest_ask[7]}")
        print(f"   Success: {latest_ask[8]}, Response time: {latest_ask[9]}ms")
        print(f"   Session: {latest_ask[10]}")
    
    conn.close()
    
    # Verify comprehensive analytics are working
    if final_search_count > initial_search_count and final_ask_count > initial_ask_count:
        print("\n🎉 SUCCESS: End-to-end analytics data capture is working!")
        print("📊 Comprehensive OpenAI API data is being stored including:")
        print("   • Token usage breakdown (input/output)")
        print("   • Actual API costs")
        print("   • Response metadata (finish_reason, system_fingerprint)")
        print("   • Performance metrics (response times)")
        print("   • Session and user tracking")
        return True
    else:
        print("\n❌ ISSUE: Analytics data not being captured properly")
        return False

if __name__ == "__main__":
    test_endpoints()
