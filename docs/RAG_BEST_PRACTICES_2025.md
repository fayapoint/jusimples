# RAG Best Practices (2024–2025)

This summarizes widely adopted patterns for production RAG in 2024–2025 with sources.

## Retrieval & Indexing
- __Hybrid retrieval__: combine dense vectors with sparse (BM25/SPLADE) for exact term sensitivity and semantic coverage.
- __Chunking__: semantic/structure‑aware chunking; target ~500–1,000 tokens; 10–20% overlap. Preserve titles/IDs.
- __Metadata__: robust filters (jurisdiction, court, law_number, article, topic, date, source, language).
- __Vector settings__: cosine similarity; HNSW or IVF/HNSW per store; product quantization only when needed (trade accuracy for cost).

## Query Understanding
- __Query rewriting__: multi‑query, HyDE, or simple paraphrases to improve recall.
- __Domain expansions__: add legal synonyms/aliases; normalize citations (e.g., “CF/88 art. 5º”).

## Reranking
- __Cross‑encoders__: Jina Reranker v2 (multilingual), Cohere Rerank v3, Voyage rerank‑2; apply on top‑k retrieved (k≈20–100) to re‑order.
- __Latency__: prefer lite variants for realtime, batch heavy rerankers offline.

## Context Construction
- __Dedup & compress__: remove near‑duplicates; apply contextual compression (LLM summarization constrained by citations).
- __Citations__: always include source IDs and spans; render in answer.
- __Dynamic k__: adjust number of chunks based on query intent and length.

## Generation
- __Guardrails__: constrain to provided context; instruct to say “não sei” if unsupported.
- __Structure__: answer + legal basis + citations + practical steps + disclaimer.
- __Language__: PT‑BR formal but accessible.

## Evaluation
- __Automated__: Retrieval Hit@k, MRR/NDCG, Answer Faithfulness, Context Precision/Recall, Hallucination rate, Latency p95, Cost.
- __Frameworks__: RAGAS, DeepEval; connect to traces for continuous evals.
- __Datasets__: curate QA pairs with authoritative gold answers and source citations.

## Observability & Ops
- __Tracing__: Langfuse/LangSmith for spans, prompts, token/costs, user feedback.
- __Caching__: semantic+exact cache; consider Redis for request/response caching.
- __Safety & Privacy__: PII redaction, LGPD compliance, rate limiting, audit logs.

## Embeddings (pt‑BR)
- __OpenAI text‑embedding‑3-large/small__: strong multilingual performance.
- __bge‑m3 / e5‑mistral__: solid open models; consider for self‑hosted.

## References
- Hybrid search guides and Qdrant hybrid docs: https://qdrant.tech/articles/hybrid-search/
- Qdrant hybrid example (LlamaIndex): https://docs.llamaindex.ai/en/stable/examples/vector_stores/qdrant_hybrid/
- Rerankers (Jina v2): https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual
- Voyage rerank‑2: https://blog.voyageai.com/2024/09/30/rerank-2/
- RAG evaluation frameworks (RAGAS/DeepEval overviews): https://www.cohorte.co/blog/evaluating-rag-systems-in-2025-ragas-deep-dive-giskard-showdown-and-the-future-of-context
- Langfuse + RAG evals: https://langfuse.com/guides/cookbook/evaluation_of_rag_with_ragas
