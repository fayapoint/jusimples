# JuSimples RAG Architecture & Implementation Guide

## RAG Pipeline Architecture

### Current Implementation Flow
```
User Query → Query Processing → Embedding Generation → Vector Search → Context Filtering → AI Generation → Response
```

### Detailed Component Analysis

#### 1. Query Processing (`/api/ask`)
**Current State**: Basic text processing
```python
# Location: backend/app.py:734
- Input validation and sanitization
- Parameter extraction (top_k, min_relevance)
- Question length validation (>10 characters)
```

**Optimization Opportunities**:
- Query expansion using legal synonyms
- Intent classification (question types)
- Legal domain detection
- Query complexity scoring

#### 2. Embedding Generation
**Current State**: OpenAI text-embedding-3-small
```python
# Location: backend/retrieval.py
- Model: text-embedding-3-small (1536 dimensions)
- Batch processing capability
- Error handling with retries
```

**Performance Metrics**:
- Embedding time: ~0.5-0.8 seconds per query
- Cost: $0.00002 per 1K tokens
- Accuracy: High semantic understanding

#### 3. Vector Search
**Current State**: Supabase pgvector with cosine similarity
```sql
-- Current query structure
SELECT *, (embedding <=> query_embedding) as distance
FROM legal_chunks
ORDER BY embedding <=> query_embedding
LIMIT top_k;
```

**Critical Issue Identified**: Relevance threshold too strict
```python
# Problem in app.py:796
relevant_context = [it for it in relevant_context if it.get("relevance", 0.0) >= min_relevance]
# Default min_relevance = 0.5, but results score 0.3-0.4
```

#### 4. Context Filtering & Ranking
**Current Issues**:
- Static threshold causes context loss
- No hybrid search (semantic + keyword)
- Missing query-document relevance boosting

**Solutions Implemented**:
```python
# Dynamic threshold adjustment
if len(relevant_context) == 0 and pre_filter_count > 0:
    fallback_threshold = max(0.2, min_relevance * 0.6)
    relevant_context = [it for it in normalized_context if it.get("relevance", 0.0) >= fallback_threshold]
```

#### 5. AI Generation
**Current State**: OpenAI gpt-4o-mini with legal prompting
```python
# Prompt structure in app.py:601
system_message = "Você é um assistente jurídico especializado em direito brasileiro"
prompt = f"""
PERGUNTA DO USUÁRIO: {question}
CONTEXTO JURÍDICO RELEVANTE: {context_text}
INSTRUÇÕES: [Detailed legal response guidelines]
"""
```

**Performance**: 
- Response time: 1-2 seconds
- Token usage: 200-600 tokens average
- Cost: $0.00006-0.0002 per query

## Optimization Strategies

### 1. Immediate Fixes (Priority 1)
```python
# Fix relevance threshold issues
- Implement dynamic thresholds
- Add relevance score logging
- Create fallback strategies

# Enhance context quality
- Improve document chunking
- Add metadata enrichment
- Implement hybrid search
```

### 2. Knowledge Base Expansion (Priority 1)
```python
# Content strategy
- Add 50+ legal documents immediately
- Implement systematic LexML integration
- Create content validation pipeline
```

### 3. Query Processing Enhancement (Priority 2)
```python
# Advanced query handling
- Add legal term expansion
- Implement question classification
- Build user intent detection
```

### 4. Performance Optimization (Priority 3)
```python
# Caching and speed improvements
- Implement embedding caching
- Add query result caching
- Optimize database queries
```

## LexML API Integration Architecture

### Current LexML Implementation
```python
# Location: backend/lexml_api.py
- Basic document search functionality
- Metadata extraction
- Content processing pipeline
```

### Systematic Integration Strategy

#### 1. Automated Content Ingestion
```python
# Proposed implementation
class LexMLContentManager:
    def daily_update_cycle(self):
        - Check for new legislation
        - Process court decisions
        - Update existing documents
        - Validate content quality
    
    def process_document(self, doc):
        - Extract legal text
        - Generate embeddings
        - Store in vector database
        - Update search indices
```

#### 2. Content Quality Pipeline
```python
# Quality assurance process
def validate_legal_content(content):
    - Check authenticity against official sources
    - Validate legal citations
    - Score content relevance
    - Flag potential errors
```

#### 3. Update Management
```python
# Version control for legal content
- Track legislative changes
- Maintain historical versions
- Update affected documents
- Notify users of changes
```

## Database Schema Optimization

### Current Schema
```sql
CREATE TABLE legal_chunks (
    id UUID PRIMARY KEY,
    title TEXT,
    content TEXT,
    category TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Enhanced Schema
```sql
CREATE TABLE legal_documents (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    subcategory TEXT,
    source_type TEXT, -- 'legislation', 'court_decision', 'regulation'
    authority_level INTEGER, -- 1-10 authority ranking
    last_updated TIMESTAMP,
    lexml_id TEXT UNIQUE,
    metadata JSONB,
    embedding VECTOR(1536),
    content_hash TEXT -- For deduplication
);

CREATE TABLE legal_chunks (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES legal_documents(id),
    chunk_text TEXT NOT NULL,
    chunk_order INTEGER,
    chunk_type TEXT, -- 'article', 'section', 'paragraph'
    embedding VECTOR(1536),
    INDEX ON embedding USING ivfflat (embedding vector_cosine_ops)
);

CREATE TABLE query_logs (
    id UUID PRIMARY KEY,
    query_text TEXT,
    user_session TEXT,
    results_count INTEGER,
    avg_relevance FLOAT,
    response_time_ms INTEGER,
    created_at TIMESTAMP
);
```

## Performance Monitoring

### Key Metrics to Track
```python
# Query Performance
- Average response time: <2 seconds target
- Query success rate: >85% target
- Context relevance: >0.6 average
- User satisfaction: >4.5/5 rating

# System Performance
- Database query time: <500ms
- Embedding generation: <800ms
- AI generation time: <1.5s
- Cache hit rate: >70%

# Content Quality
- Document coverage: >500 documents
- Domain expertise: >90% legal areas
- Content freshness: <30 days average age
- Accuracy rate: >95% validated responses
```

### Monitoring Implementation
```python
# Real-time monitoring
class RAGMonitor:
    def log_query_performance(self, query, response_time, relevance_scores):
        # Track performance metrics
        
    def analyze_content_gaps(self, failed_queries):
        # Identify missing knowledge areas
        
    def optimize_relevance_thresholds(self, historical_data):
        # Dynamic threshold adjustment
```

## Deployment & Scaling Strategy

### Current Infrastructure
- **Backend**: Railway deployment with health checks
- **Database**: Supabase PostgreSQL with pgvector
- **Frontend**: Netlify with React
- **APIs**: OpenAI integration with robust error handling

### Scaling Recommendations
```python
# Phase 1: Foundation (Current)
- Fix RAG pipeline issues
- Expand knowledge base to 50+ documents
- Implement dynamic thresholds

# Phase 2: Growth (Month 1)
- Scale to 500+ documents
- Implement caching systems
- Add comprehensive monitoring

# Phase 3: Enterprise (Month 2)
- Multi-model AI support
- Advanced query processing
- Real-time LexML integration
```

This architecture guide provides the technical foundation for building Brazil's most comprehensive legal AI platform.
