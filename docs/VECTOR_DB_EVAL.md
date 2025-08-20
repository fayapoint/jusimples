# Vector DB Evaluation for JuSimples

## Criteria
- __Fit with infra__: deployability on Railway, managed options, simplicity.
- __Features__: hybrid search, rich filters, HNSW/IVF, quantization, payload filtering.
- __Scale__: docs and chunks now small; plan for 100k–10M chunks.
- __Latency & cost__: p95 under ~800ms end‑to‑end; cost efficiency.

## Options

- __pgvector (PostgreSQL extension)__
  - Pros: simple ops (managed Postgres on Railway), ACID, SQL filters, joins, transactional ingestion; HNSW (newer versions), IVF; good for ≤1–5M vectors.
  - Cons: CPU‑bound; limited advanced ANN features vs specialized stores; hybrid requires extra setup (BM25 via pg_trgm or separate index).
  - Fit: Excellent for MVP with Railway Postgres.

- __Qdrant__
  - Pros: strong filters, payloads, native hybrid (dense + sparse), HNSW, quantization; Cloud or self‑host; Python/JS SDKs.
  - Cons: extra service to run/manage; cost if Cloud.
  - Fit: Great default if hybrid needed early and scale grows.

- __Pinecone__
  - Pros: fully managed serverless, easy scaling, strong reliability; enterprise features.
  - Cons: cost; vendor lock‑in; sparse/hybrid via namespaces/metadata or API features; filters decent.
  - Fit: Good when ops must be near‑zero and budget allows.

- __Weaviate__
  - Pros: hybrid search, modules, GraphQL; Cloud/Self‑host.
  - Cons: additional service; ops and query model more complex for small teams.

- __Chroma__
  - Pros: simplest local/dev; tight LangChain integration.
  - Cons: not ideal beyond small prod workloads; fewer ops tools.

## Recommendation
- __Phase 1 (MVP)__: Use __pgvector__ on Railway Postgres. Lowest ops, strong filtering via SQL, good enough performance for ≤1M chunks. Add BM25 index for hybrid if needed.
- __Phase 2 (Scale/Hybrid)__: Move/dual‑write to __Qdrant Cloud__ for native hybrid and better recall at scale. Keep Postgres for metadata and joins.
- __Pinecone path__: If team wants fully managed vectors and budget flexibility, Pinecone Serverless is viable; ensure cost monitoring.

## Sources
- Top vector DBs 2025 roundups: https://www.shakudo.io/blog/top-9-vector-databases
- Qdrant vs Pinecone overview: https://qdrant.tech/blog/comparing-qdrant-vs-pinecone-vector-databases/
- General comparisons: https://www.cloudraft.io/blog/top-5-vector-databases
