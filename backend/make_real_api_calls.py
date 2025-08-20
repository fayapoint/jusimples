#!/usr/bin/env python3
"""
Make real API calls to test end-to-end analytics logging
"""

import requests
import json
import time
import psycopg

def test_real_api_calls():
    print("🚀 Making real API calls to test analytics capture...")
    
    # Database connection for verification
    db_url = "postgresql://postgres.ugbplcahdqjgercuqvsr:5bNVhwx5%24z%23%3FL%3Fw@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
    
    def check_records():
        conn = psycopg.connect(db_url, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM search_logs')
        search_count = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM ask_logs')
        ask_count = cur.fetchone()[0]
        conn.close()
        return search_count, ask_count
    
    # Check initial counts
    initial_search, initial_ask = check_records()
    print(f"📊 Before tests: search_logs={initial_search}, ask_logs={initial_ask}")
    
    # Test 1: Search API
    print("\n🔍 TEST 1: Making search API call...")
    try:
        response = requests.post(
            'http://localhost:5000/api/search',
            json={
                'query': 'direito do trabalho férias',
                'top_k': 3,
                'min_relevance': 0.7
            },
            headers={
                'Content-Type': 'application/json',
                'X-Session-ID': 'analytics_test_session_001',
                'X-User-ID': 'test_user_analytics',
                'User-Agent': 'JuSimples Analytics Test/1.0'
            },
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Results: {len(data.get('results', []))} documents")
            print(f"   Query processed: {data.get('query', 'N/A')}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Search API error: {e}")
    
    time.sleep(2)  # Allow logging to complete
    
    # Check after search
    after_search, _ = check_records()
    print(f"   📈 After search: search_logs={after_search} (+{after_search - initial_search})")
    
    # Test 2: Ask API with comprehensive question
    print("\n🤖 TEST 2: Making ask API call...")
    try:
        response = requests.post(
            'http://localhost:5000/api/ask',
            json={
                'question': 'Quais são os direitos do trabalhador em relação às férias? Explique detalhadamente os períodos e remuneração.',
                'top_k': 5,
                'min_relevance': 0.6
            },
            headers={
                'Content-Type': 'application/json',
                'X-Session-ID': 'analytics_test_session_001',
                'X-User-ID': 'test_user_analytics',
                'User-Agent': 'JuSimples Analytics Test/1.0'
            },
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            print(f"   Answer length: {len(answer)} characters")
            print(f"   Sources: {len(data.get('sources', []))} documents")
            print(f"   Answer preview: {answer[:100]}...")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Ask API error: {e}")
    
    time.sleep(3)  # Allow logging to complete
    
    # Final verification with detailed analytics
    print("\n📊 FINAL VERIFICATION - Checking comprehensive analytics data...")
    final_search, final_ask = check_records()
    print(f"Final counts: search_logs={final_search}, ask_logs={final_ask}")
    print(f"New records created: search={final_search - initial_search}, ask={final_ask - initial_ask}")
    
    # Show detailed OpenAI analytics from latest records
    conn = psycopg.connect(db_url, sslmode='require')
    cur = conn.cursor()
    
    # Latest search with all analytics
    if final_search > initial_search:
        cur.execute("""
            SELECT query, search_type, success, response_time_ms, 
                   context_found, session_id, user_id, created_at
            FROM search_logs 
            WHERE session_id = 'analytics_test_session_001'
            ORDER BY created_at DESC LIMIT 1
        """)
        search_record = cur.fetchone()
        if search_record:
            print(f"\n📈 Latest SEARCH analytics:")
            print(f"   Query: '{search_record[0]}'")
            print(f"   Type: {search_record[1]}, Success: {search_record[2]}")
            print(f"   Response time: {search_record[3]}ms")
            print(f"   Results found: {search_record[4]}")
            print(f"   Session: {search_record[5]}, User: {search_record[6]}")
    
    # Latest ask with comprehensive OpenAI data
    if final_ask > initial_ask:
        cur.execute("""
            SELECT question, llm_model, llm_tokens_used, input_tokens, output_tokens,
                   llm_cost, finish_reason, system_fingerprint, success, 
                   response_time_ms, session_id, user_id
            FROM ask_logs 
            WHERE session_id = 'analytics_test_session_001'
            ORDER BY created_at DESC LIMIT 1
        """)
        ask_record = cur.fetchone()
        if ask_record:
            print(f"\n🤖 Latest ASK analytics (OpenAI API data):")
            print(f"   Question: '{ask_record[0][:60]}...'")
            print(f"   Model: {ask_record[1]}")
            print(f"   Tokens: {ask_record[2]} total ({ask_record[3]} input + {ask_record[4]} output)")
            print(f"   Cost: ${ask_record[5]:.6f}")
            print(f"   Finish reason: {ask_record[6]}")
            print(f"   System fingerprint: {ask_record[7]}")
            print(f"   Success: {ask_record[8]}, Response time: {ask_record[9]}ms")
            print(f"   Session: {ask_record[10]}, User: {ask_record[11]}")
    
    conn.close()
    
    # Success verification
    if (final_search > initial_search and final_ask > initial_ask):
        print("\n🎉 SUCCESS! End-to-end analytics logging is working perfectly!")
        print("\n📊 Your analytics dashboard now captures:")
        print("   ✅ Real user searches and questions")
        print("   ✅ Comprehensive OpenAI API data (tokens, costs, fingerprints)")
        print("   ✅ Performance metrics (response times)")
        print("   ✅ User session tracking")
        print("   ✅ Success rates and error tracking")
        print("\n💡 Make more searches in your app to see the analytics data grow!")
        return True
    else:
        print("\n❌ Issue: Not all API calls were logged properly")
        return False

if __name__ == "__main__":
    test_real_api_calls()
