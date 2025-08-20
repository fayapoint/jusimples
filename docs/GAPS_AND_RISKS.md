# Gaps and Risks vs Best Practices (JuSimples RAG)

This document contrasts the current implementation with 2024–2025 RAG best practices and lists prioritized fixes.

## Baseline (current)
- Retrieval: keyword search in `backend/app.py` → `search_legal_knowledge()` over `LEGAL_KNOWLEDGE` (5 docs).
- Generation: `generate_ai_response()` calls OpenAI Chat; fails without `OPENAI_API_KEY`.
- Ingestion: `backend/data_collector.py` + `backend/lexml_scraper.py` exist but not wired to a vector index.
- Observability: logging only; no traces/evals.

## Gaps
- __Retrieval__
  - No embeddings/vector DB; no semantic recall.
  - No hybrid retrieval (dense + sparse/BM25/SPLADE).
  - No reranking (e.g., cross‑encoder like Jina v2).
  - No chunking strategy; KB is not normalized or scalable.
- __Prompting/Answers__
  - Citations are shown as titles in `sources`, but answers in `generate_ai_response()` are not constrained to quote spans or emit machine‑readable citations/IDs.
  - No dynamic context sizing or de‑duplication/compression.
- __Ingestion & Schema__
  - Scraper outputs JSON, but there’s no normalization to a stable `LEGAL_DOC_SCHEMA` or chunk pipeline.
  - No deduplication or content hashing; no reindex/versioning.
- __Observability & Evaluation__
  - No tracing (Langfuse/LangSmith), no metrics for retrieval/faithfulness/latency.
  - CI/CD is not gating deploys on evals (RAGAS/DeepEval).
- __Security & Compliance__
  - Admin/test endpoints exist but no auth/rate limiting indicated.
  - No PII redaction, audit logs, or LGPD safeguards in the pipeline.
- __Infra & Config__
  - `OPENAI_API_KEY` missing in deployment; default `OPENAI_MODEL` = `gpt-5-nano` may not exist in tenant.
  - No caching layer; no cost monitoring; no feature flags for retrieval variants.
- __Testing__
  - Tests reference semantic search behaviors but vector stack not installed (`backend/requirements.txt` minimal).

## Risks
- __Hallucination__ due to weak retrieval and unconstrained generation.
- __Data quality__ from scraping without schema/normalization/dedup.
- __Operational instability__ without tracing/evals; regressions undetected.
- __Compliance__ exposure (LGPD) without redaction and access controls.
- __Vendor lock‑in/cost__ if adopting managed vector DBs without abstraction.

## Recommended Fixes (Prioritized)
1. __MVP Semantic Retrieval__
   - Add embeddings (OpenAI `text-embedding-3-small`); store in __pgvector__ (managed Postgres on Railway).
   - Implement chunking (500–1,000 tokens, 10–20% overlap) and metadata schema.
   - Switch `/api/ask` to semantic top‑k.
2. __Observability & Evals__
   - Instrument Langfuse traces and token/latency metrics.
   - Nightly RAGAS/DeepEval over gold QA; gate deploy on thresholds.
3. __Hybrid + Rerank__
   - Add BM25 index; combine with dense results; rerank top‑k with Jina Reranker v2 (lite for RT).
4. __Ingestion Hardening__
   - Normalize to `docs/LEGAL_DOC_SCHEMA.md`; add hashing/dedup; reindex versioning.
   - Ingest LexML + DataJud + DOU incrementally with backfills.
5. __Security & Compliance__
   - Protect admin endpoints; add rate limiting; PII redaction and audit logs.
6. __Cost/Latency Controls__
   - Add caching; consider smaller gen models; batch embeddings; monitor spend.

## References
- Best practices: `docs/RAG_BEST_PRACTICES_2025.md`
- Vector DB evaluation: `docs/VECTOR_DB_EVAL.md`
- Sources: Qdrant Hybrid, Langfuse + RAGAS guides listed in the above docs.
