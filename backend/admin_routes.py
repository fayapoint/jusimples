"""
Admin Routes for JuSimples
Handles all admin panel endpoints
"""
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_cors import cross_origin
import logging
from datetime import datetime, timedelta
import json
from query_storage import query_storage
from retrieval import (
    admin_list_legal_chunks, admin_list_search_logs, 
    admin_list_ask_logs, admin_update_legal_chunk,
    admin_get_database_status
)
from db_utils import get_db_manager
import openai
import os
import requests

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    """Main admin dashboard"""
    try:
        # Get database status
        db_status = admin_get_database_status()
        
        # Get recent query stats
        stats = query_storage.get_query_stats(days=7)
        
        # Get recent queries
        recent_queries = query_storage.get_recent_queries(limit=10)
        
        return render_template('admin_dashboard.html',
                             db_status=db_status,
                             stats=stats,
                             recent_queries=recent_queries)
    except Exception as e:
        logger.error(f"Admin dashboard error: {e}")
        return render_template('admin_dashboard.html', error=str(e))

@admin_bp.route('/query-analytics')
def query_analytics():
    """Query analytics page"""
    try:
        # Get time range from query params
        days = int(request.args.get('days', 30))
        limit = int(request.args.get('limit', 50))
        
        # Get top queries
        top_queries = query_storage.get_top_queries(limit=limit, days=days)
        
        # Get recent queries with details
        recent_queries = query_storage.get_recent_queries(limit=limit)
        
        # Get comprehensive stats
        stats = query_storage.get_query_stats(days=days)
        
        return render_template('query_analytics.html',
                             top_queries=top_queries,
                             recent_queries=recent_queries,
                             stats=stats,
                             days=days,
                             limit=limit)
    except Exception as e:
        logger.error(f"Query analytics error: {e}")
        return render_template('query_analytics.html', error=str(e))

@admin_bp.route('/knowledge-base')
def knowledge_base():
    """Knowledge base management page"""
    try:
        # Get filter parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        category = request.args.get('category', None)
        search = request.args.get('search', None)
        
        # Get legal chunks from database
        chunks = admin_list_legal_chunks(
            page=page,
            per_page=per_page,
            category=category,
            search=search
        )
        
        # Calculate pagination
        total_pages = (chunks['total'] + per_page - 1) // per_page if chunks else 0
        
        return render_template('knowledge_base.html',
                             chunks=chunks.get('chunks', []),
                             total=chunks.get('total', 0),
                             page=page,
                             per_page=per_page,
                             total_pages=total_pages,
                             category=category,
                             search=search)
    except Exception as e:
        logger.error(f"Knowledge base error: {e}")
        return render_template('knowledge_base.html', error=str(e))

@admin_bp.route('/knowledge-base/<chunk_id>')
def knowledge_base_item(chunk_id):
    """View and edit a specific knowledge base item"""
    try:
        db_manager = get_db_manager()
        conn = db_manager.get_connection()
        
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    id, parent_id, title, content, category, 
                    metadata, created_at, updated_at,
                    LENGTH(content) as content_length,
                    embedding IS NOT NULL as has_embedding
                FROM legal_chunks
                WHERE id = %s
            """, (chunk_id,))
            
            row = cur.fetchone()
            if not row:
                flash(f"Item {chunk_id} not found", "error")
                return redirect(url_for('admin.knowledge_base'))
            
            chunk = {
                'id': row[0],
                'parent_id': row[1],
                'title': row[2],
                'content': row[3],
                'category': row[4],
                'metadata': row[5] if row[5] else {},
                'created_at': row[6].isoformat() if row[6] else None,
                'updated_at': row[7].isoformat() if row[7] else None,
                'content_length': row[8],
                'has_embedding': row[9]
            }
            
            # Get related chunks
            cur.execute("""
                SELECT id, title, category
                FROM legal_chunks
                WHERE parent_id = %s AND id != %s
                LIMIT 10
            """, (row[1] if row[1] else chunk_id, chunk_id))
            
            related = []
            for r in cur.fetchall():
                related.append({'id': r[0], 'title': r[1], 'category': r[2]})
            
            chunk['related'] = related
            
        return render_template('knowledge_base_item.html', chunk=chunk)
        
    except Exception as e:
        logger.error(f"Knowledge base item error: {e}")
        flash(f"Error loading item: {e}", "error")
        return redirect(url_for('admin.knowledge_base'))

@admin_bp.route('/knowledge-base/<chunk_id>/edit', methods=['POST'])
def edit_knowledge_base_item(chunk_id):
    """Update a knowledge base item"""
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        metadata = request.form.get('metadata', '{}')
        
        # Parse metadata JSON
        try:
            metadata_dict = json.loads(metadata)
        except:
            metadata_dict = {}
        
        success = admin_update_legal_chunk(
            chunk_id=chunk_id,
            title=title,
            content=content,
            category=category,
            metadata=metadata_dict
        )
        
        if success:
            flash("Item updated successfully", "success")
        else:
            flash("Failed to update item", "error")
            
        return redirect(url_for('admin.knowledge_base_item', chunk_id=chunk_id))
        
    except Exception as e:
        logger.error(f"Edit knowledge base item error: {e}")
        flash(f"Error updating item: {e}", "error")
        return redirect(url_for('admin.knowledge_base_item', chunk_id=chunk_id))

@admin_bp.route('/openai-dashboard')
def openai_dashboard():
    """OpenAI API dashboard"""
    try:
        # Check if API key is configured
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return render_template('openai_dashboard.html', 
                                 error="OpenAI API key not configured")
        
        # Get usage statistics from database
        db_manager = get_db_manager()
        conn = db_manager.get_connection()
        
        stats = {}
        with conn.cursor() as cur:
            # Get total usage
            cur.execute("""
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(llm_tokens_used) as total_tokens,
                    SUM(input_tokens) as total_input_tokens,
                    SUM(output_tokens) as total_output_tokens,
                    SUM(llm_cost) as total_cost,
                    AVG(response_time_ms) as avg_response_time
                FROM ask_logs
                WHERE llm_model IS NOT NULL
            """)
            
            row = cur.fetchone()
            stats['total_requests'] = row[0] or 0
            stats['total_tokens'] = row[1] or 0
            stats['total_input_tokens'] = row[2] or 0
            stats['total_output_tokens'] = row[3] or 0
            stats['total_cost'] = float(row[4]) if row[4] else 0
            stats['avg_response_time'] = float(row[5]) if row[5] else 0
            
            # Get model usage distribution
            cur.execute("""
                SELECT 
                    llm_model,
                    COUNT(*) as count,
                    SUM(llm_tokens_used) as tokens,
                    SUM(llm_cost) as cost
                FROM ask_logs
                WHERE llm_model IS NOT NULL
                GROUP BY llm_model
                ORDER BY count DESC
            """)
            
            models = []
            for row in cur.fetchall():
                models.append({
                    'model': row[0],
                    'count': row[1],
                    'tokens': row[2] or 0,
                    'cost': float(row[3]) if row[3] else 0
                })
            stats['models'] = models
            
            # Get daily usage for last 30 days
            cur.execute("""
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as requests,
                    SUM(llm_tokens_used) as tokens,
                    SUM(llm_cost) as cost
                FROM ask_logs
                WHERE created_at > now() - interval '30 days'
                    AND llm_model IS NOT NULL
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            """)
            
            daily_usage = []
            for row in cur.fetchall():
                daily_usage.append({
                    'date': row[0].isoformat() if row[0] else None,
                    'requests': row[1],
                    'tokens': row[2] or 0,
                    'cost': float(row[3]) if row[3] else 0
                })
            stats['daily_usage'] = daily_usage
            
            # Get error rate
            cur.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE success = false) * 100.0 / NULLIF(COUNT(*), 0) as error_rate
                FROM ask_logs
                WHERE llm_model IS NOT NULL
            """)
            
            row = cur.fetchone()
            stats['error_rate'] = float(row[0]) if row[0] else 0
            
        # Get current model configuration
        config = {
            'api_key_configured': bool(api_key),
            'api_key_preview': api_key[:8] + '...' + api_key[-4:] if api_key else None,
            'default_model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
            'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '1000')),
            'embedding_model': os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
        }
        
        return render_template('openai_dashboard.html',
                             stats=stats,
                             config=config)
        
    except Exception as e:
        logger.error(f"OpenAI dashboard error: {e}")
        return render_template('openai_dashboard.html', error=str(e))

@admin_bp.route('/lextml-api')
def lextml_api():
    """LexML API control page"""
    try:
        return render_template('lextml_api.html')
        
    except Exception as e:
        logger.error(f"LexML API error: {e}")
        return render_template('lextml_api.html', error=str(e))

@admin_bp.route('/lextml-api/search', methods=['POST'])
def lextml_search():
    """Search LexML for laws"""
    try:
        query = request.json.get('query', '')
        limit = request.json.get('limit', 20)
        
        # Search LexML API
        response = requests.get(
            'https://www.lexml.gov.br/busca/SRU',
            params={
                'operation': 'searchRetrieve',
                'query': query,
                'maximumRecords': limit,
                'recordSchema': 'dc'
            }
        )
        
        if response.status_code == 200:
            # Parse XML response and extract laws
            # This is a simplified example - real implementation would parse XML properly
            laws = []
            # ... XML parsing logic ...
            
            return jsonify({'success': True, 'laws': laws})
        else:
            return jsonify({'success': False, 'error': 'LexML API error'})
            
    except Exception as e:
        logger.error(f"LexML search error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/lextml-api/add', methods=['POST'])
def lextml_add():
    """Add a law from LexML to knowledge base"""
    try:
        law_data = request.json
        
        # Add to database
        db_manager = get_db_manager()
        conn = db_manager.get_connection()
        
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO legal_chunks (
                    id, title, content, category, metadata
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET title = EXCLUDED.title,
                    content = EXCLUDED.content,
                    updated_at = now()
            """, (
                law_data['id'],
                law_data['title'],
                law_data['content'],
                'lei_federal',
                json.dumps(law_data.get('metadata', {}))
            ))
            
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Law added successfully'})
        
    except Exception as e:
        logger.error(f"LexML add error: {e}")
        return jsonify({'success': False, 'error': str(e)})

# API endpoints for AJAX calls
@admin_bp.route('/api/query-stats')
@cross_origin()
def api_query_stats():
    """API endpoint for query statistics"""
    try:
        days = int(request.args.get('days', 7))
        stats = query_storage.get_query_stats(days=days)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/top-queries')
@cross_origin()
def api_top_queries():
    """API endpoint for top queries"""
    try:
        limit = int(request.args.get('limit', 20))
        days = int(request.args.get('days', 30))
        queries = query_storage.get_top_queries(limit=limit, days=days)
        return jsonify(queries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/recent-queries')
@cross_origin()
def api_recent_queries():
    """API endpoint for recent queries"""
    try:
        limit = int(request.args.get('limit', 50))
        queries = query_storage.get_recent_queries(limit=limit)
        return jsonify(queries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
