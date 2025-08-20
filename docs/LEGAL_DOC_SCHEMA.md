# Target Schema for Legal Documents and Chunks

A normalized, retrieval‑friendly schema for laws, jurisprudence, and official publications.

## Base Document (common fields)
- `id`: stable canonical ID
- `source`: lexml | senado | camara | stf | stj | cnj_datajud | dou | other
- `doc_type`: law | decree | constitution | jurisprudence | summary | decision | publication
- `title`: human‑readable title
- `jurisdiction`: BR | state | municipality
- `court_or_body`: e.g., STF, STJ, TJSP, Senado, Câmara
- `number`: e.g., Lei 8.078/1990; process/acórdão number for cases
- `date_published`: ISO8601
- `date_effective`: ISO8601 (when applicable)
- `language`: pt-BR
- `subjects`: [strings]
- `keywords`: [strings]
- `citations`: [{ target_id, text, span }]
- `urls`: { canonical, source, mirror }
- `hash`: content hash for dedup
- `raw_text`: full text (optional if chunked stored separately)
- `metadata`: free‑form JSON for source‑specific fields

## Law‑specific
- `structure`: { book, title, chapter, section, article, paragraph }
- `consolidation_info`: e.g., revocations, amendments

## Jurisprudence‑specific
- `case_number`
- `class`: e.g., RE, ARE, AgRg
- `parties`: anonymized as needed
- `rapporteur`
- `summary` (ementa)
- `decision_text`
- `decision_date`

## Chunk Schema
- `chunk_id`: unique
- `parent_id`: reference to document `id`
- `order`: integer for sequence
- `text`: chunk content
- `tokens`: token count
- `char_count`: length
- `section_path`: e.g., CF/88 > Art. 5º > Inciso X
- `spans`: [{ start, end, label }]
- `embedding_dense`: optional vector ID or inline float[] (store ID if using external vector DB)
- `embedding_sparse`: optional sparse representation (token->weight)
- `metadata`: { law_number, article, court, class, date, … }

## Indexing & Retrieval Metadata
- `index_version`: for reindexing audits
- `embedding_model`: e.g., text-embedding-3-large
- `sparse_model`: e.g., BM25/SPLADE

## Example (JSON)
```json
{
  "id": "lei-8078-1990",
  "source": "senado",
  "doc_type": "law",
  "title": "Código de Defesa do Consumidor",
  "jurisdiction": "BR",
  "number": "8.078/1990",
  "date_published": "1990-09-11",
  "language": "pt-BR",
  "subjects": ["consumidor"],
  "urls": {"canonical": "https://www.planalto.gov.br/", "source": "https://www12.senado.leg.br/"}
}
```
