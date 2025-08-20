# Brazilian Legal Data Sources (APIs/Datasets)

Official and reputable sources to ingest laws, decisions, and official publications.

## Laws and Legislative Data
- __LexML Portal__
  - Portal: https://www.lexml.gov.br/
  - Docs/Open Data: https://projeto.lexml.gov.br/open-data
  - Notes: provides programmatic access and XML/linked data; supports queries over the legislative corpus.
- __Senado Federal – Dados Abertos (Legislação)__
  - Legislation datasets: https://www12.senado.leg.br/dados-abertos/legislativo/legislacao/acervo-do-portal-lexml
  - General portal: https://www12.senado.leg.br/dados-abertos
- __Câmara dos Deputados – Dados Abertos__
  - Swagger: https://dadosabertos.camara.leg.br/swagger/api.html

## Judiciary Data
- __CNJ – DataJud (API Pública)__
  - Landing: https://www.cnj.jus.br/sistemas/datajud/api-publica/
  - Datasets (STJ portal mirror): https://dadosabertos.web.stj.jus.br/dataset/api-publica-datajud
  - Notes: national‑level process/decision metadata; important for jurisprudence coverage.
- __STF__
  - Portal: https://portal.stf.jus.br/
  - Notes: official portal; programmatic access limited; prefer DataJud and official datasets when available.
- __STJ – Dados Abertos__
  - Portal: https://dadosabertos.web.stj.jus.br/dataset/

## Diário Oficial da União (DOU)
- __Imprensa Nacional – Dados Abertos__
  - Base de dados DOU (XML): https://www.in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados
  - Portal: https://www.in.gov.br/acesso-a-informacao/dados-abertos

## Commercial/Third‑party (license/ToS dependent)
- Jusbrasil, etc. Note: review ToS and obtain licenses before ingestion; avoid scraping without authorization.

## Recommended Approach
- Start with __LexML__ and __Senado/Câmara__ for laws and consolidated texts.
- Use __DataJud__ and tribunal datasets for jurisprudence coverage.
- Ingest __DOU__ for official publications; normalize to schema and chunk by sections.

## Compliance
- Respect robots.txt/ToS and rate limits.
- Ensure LGPD compliance: process only necessary data; handle PII securely; maintain audit logs.
