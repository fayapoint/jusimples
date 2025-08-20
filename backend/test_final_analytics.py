#!/usr/bin/env python3
"""
Final test: Verify end-to-end analytics with proper API calls
"""

import requests
import psycopg
import time

def test_analytics():
    print("🧪 Testing analytics with proper API calls...")
    
    # Database connection
    db_url = "postgresql://postgres.ugbplcahdqjgercuqvsr:5bNVhwx5%24z%23%3FL%3Fw@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
    
    # Get initial counts
    conn = psycopg.connect(db_url, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM search_logs')
    initial_search = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM ask_logs')
    initial_ask = cur.fetchone()[0]
    conn.close()
    
    print(f"📊 Before tests: search_logs={initial_search}, ask_logs={initial_ask}")
    
    # Test 1: Search with valid query
    print("\n🔍 Testing search endpoint...")
    try:
        response = requests.post('http://localhost:5000/api/search', 
                               json={
                                   'query': 'direito do trabalho férias remuneração CLT',
                                   'top_k': 5,
                                   'min_relevance': 0.6
                               },
                               headers={
                                   'X-Session-ID': 'final_test_session',
                                   'X-User-ID': 'final_test_user'
                               },
                               timeout=10)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Results: {len(data.get('results', []))} documents found")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Search failed: {e}")
    
    time.sleep(1)
    
    # Test 2: Ask with proper question
    print("\n🤖 Testing ask endpoint...")
    try:
        response = requests.post('http://localhost:5000/api/ask',
                               json={
                                   'question': 'Quais são os principais direitos do trabalhador brasileiro em relação às férias anuais? Explique detalhadamente os períodos de gozo e como é calculada a remuneração das férias.',
                                   'top_k': 5
                               },
                               headers={
                                   'X-Session-ID': 'final_test_session',
                                   'X-User-ID': 'final_test_user'
                               },
                               timeout=25)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            print(f"   Answer length: {len(answer)} characters")
            print(f"   Sources: {len(data.get('sources', []))} documents")
            print(f"   Answer preview: {answer[:120]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Ask failed: {e}")
    
    time.sleep(3)  # Allow time for async logging
    
    # Verify analytics data was captured
    print("\n📊 Verifying analytics data capture...")
    conn = psycopg.connect(db_url, sslmode='require')
    cur = conn.cursor()
    
    # Final counts
    cur.execute('SELECT COUNT(*) FROM search_logs')
    final_search = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM ask_logs')
    final_ask = cur.fetchone()[0]
    
    print(f"After tests: search_logs={final_search}, ask_logs={final_ask}")
    print(f"New records: search={final_search - initial_search}, ask={final_ask - initial_ask}")
    
    # Show latest test records
    cur.execute("""
        SELECT query, search_type, success, response_time_ms, context_found, session_id
        FROM search_logs 
        WHERE session_id = 'final_test_session'
        ORDER BY created_at DESC LIMIT 1
    """)
    search_record = cur.fetchone()
    
    cur.execute("""
        SELECT question, llm_model, llm_tokens_used, input_tokens, output_tokens, 
               llm_cost, finish_reason, success, response_time_ms, session_id
        FROM ask_logs 
        WHERE session_id = 'final_test_session'
        ORDER BY created_at DESC LIMIT 1
    """)
    ask_record = cur.fetchone()
    
    if search_record:
        print(f"\n📈 SEARCH Analytics Captured:")
        print(f"   Query: '{search_record[0]}'")
        print(f"   Type: {search_record[1]}, Success: {search_record[2]}")
        print(f"   Response: {search_record[3]}ms, Results: {search_record[4]}")
    
    if ask_record:
        print(f"\n🤖 ASK Analytics Captured (OpenAI API Data):")
        print(f"   Question: '{ask_record[0][:60]}...'")
        print(f"   Model: {ask_record[1]}")
        print(f"   Tokens: {ask_record[2]} total ({ask_record[3]} input + {ask_record[4]} output)")
        print(f"   Cost: ${ask_record[5]:.6f}")
        print(f"   Finish: {ask_record[6]}, Success: {ask_record[7]}")
        print(f"   Response time: {ask_record[8]}ms")
    
    conn.close()
    
    # Success check
    success = (final_search > initial_search and final_ask > initial_ask and 
               search_record is not None and ask_record is not None)
    
    if success:
        print(f"\n🎉 ANALYTICS LOGGING CONFIRMED WORKING!")
        print(f"✅ Search and Ask APIs are capturing comprehensive data")
        print(f"✅ OpenAI token usage, costs, and metadata being stored")
        print(f"✅ Session tracking and performance metrics working")
        print(f"\n💡 Your admin dashboard will now show real analytics data!")
    else:
        print(f"\n⚠️ Some analytics data may not be capturing correctly")
        print(f"Check Flask app logs for any errors")
    
    return success

if __name__ == "__main__":
    test_analytics()
