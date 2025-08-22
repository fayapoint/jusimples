# JuSimples Content Seeding Plan

## Immediate Content Priorities (Week 1)

### Family Law - União Estável Focus (Priority 1)
**Target Query**: "Em União Estável o regime será sempre de comunhão parcial de bens?"

#### Document 1: União Estável - Regime de Bens Completo
```markdown
Title: "União Estável e Regime de Bens no Brasil"
Content: 
- Definição legal de união estável (Art. 1723 CC)
- Regime legal: comunhão parcial de bens (padrão)
- Possibilidade de contrato de convivência
- Diferenças entre casamento e união estável
- Procedimentos para formalização
- Direitos patrimoniais dos companheiros
- Dissolução e partilha de bens

Category: family_law
Subcategory: stable_unions
Authority_level: 9 (Código Civil)
```

#### Document 2: Regimes de Bens Detalhados
```markdown
Title: "Regimes de Bens na União Estável"
Content:
- Comunhão parcial (regime legal padrão)
- Comunhão universal de bens
- Separação convencional de bens
- Separação obrigatória de bens
- Participação final nos aquestos
- Como alterar regime durante união
- Efeitos da escolha do regime

Category: family_law
Subcategory: property_regimes
Authority_level: 9
```

### Labor Law Foundation (Priority 2)

#### Document 3: CLT - Direitos Fundamentais do Trabalhador
```markdown
Title: "Direitos Trabalhistas Essenciais - CLT"
Content:
- Jornada de trabalho (8h/44h semanais)
- Horas extras e adicional (50%/100%)
- Férias anuais remuneradas (30 dias)
- 13º salário e gratificações
- FGTS e seguro-desemprego
- Aviso prévio e rescisão
- Licenças e afastamentos

Category: labor_law
Subcategory: worker_rights
Authority_level: 10 (CLT)
```

### Consumer Law Enhancement (Priority 3)

#### Document 4: Direitos do Consumidor Online
```markdown
Title: "Compras Online e Direitos do Consumidor"
Content:
- Direito de arrependimento (7 dias)
- Produtos defeituosos e garantia
- Publicidade enganosa ou abusiva
- Cobrança indevida e negativação
- Atendimento e SAC obrigatório
- Resolução de conflitos (Procon, Justiça)
- Contratos eletrônicos e assinatura

Category: consumer_law
Subcategory: online_commerce
Authority_level: 9 (CDC)
```

## Content Creation Scripts

### Automated Document Generator
```python
# backend/content_seeding.py

PRIORITY_LEGAL_CONTENT = [
    {
        "title": "União Estável e Regime de Bens no Brasil",
        "content": """
A união estável, prevista no artigo 1.723 do Código Civil, é a convivência pública, contínua e duradoura entre duas pessoas, estabelecida com o objetivo de constituição de família.

## Regime Legal de Bens

Por determinação legal (Art. 1.725 do Código Civil), na união estável aplica-se o regime da comunhão parcial de bens, salvo contrato escrito em contrário.

### Comunhão Parcial de Bens (Regime Padrão)
- **Bens comuns**: adquiridos durante a união por ambos ou qualquer dos companheiros
- **Bens particulares**: anteriores à união, recebidos por herança ou doação
- **Frutos e rendimentos**: dos bens particulares também se comunicam

### Possibilidade de Outro Regime
Os companheiros podem, mediante contrato de convivência:
- Escolher comunhão universal de bens
- Optar pela separação convencional
- Estabelecer participação final nos aquestos

### Alteração do Regime
Durante a união, é possível alterar o regime através de:
- Escritura pública
- Autorização judicial (quando há filhos menores)
- Anuência de ambos os companheiros

### Conversão em Casamento
A união estável pode ser convertida em casamento mediante:
- Requerimento ao oficial do Registro Civil
- Apresentação de documentos comprobatórios
- Mantém-se o regime de bens escolhido

**Base Legal**: Código Civil Brasileiro, Arts. 1.723 a 1.727
**Aplicação**: Todo território nacional
**Vigência**: Atual (2025)
        """,
        "category": "family_law",
        "subcategory": "stable_unions",
        "authority_level": 9,
        "legal_citations": ["CC Art. 1723", "CC Art. 1725", "CC Art. 1727"],
        "keywords": ["união estável", "regime de bens", "comunhão parcial", "contrato convivência"]
    },
    
    {
        "title": "Rescisão de Contrato de Trabalho - Direitos e Verbas",
        "content": """
A rescisão do contrato de trabalho gera direitos específicos conforme a modalidade de término, regulamentados pela CLT.

## Tipos de Rescisão

### Demissão sem Justa Causa
**Direitos do trabalhador**:
- Aviso prévio (30 dias + 3 dias por ano trabalhado)
- Saldo de salário proporcional
- Férias vencidas e proporcionais + 1/3
- 13º salário proporcional
- FGTS + multa de 40%
- Seguro-desemprego (se atender requisitos)

### Demissão por Justa Causa
**Verbas devidas**:
- Saldo de salário dos dias trabalhados
- Férias vencidas + 1/3 constitucional
- **Não há**: aviso prévio, 13º proporcional, multa FGTS

### Pedido de Demissão
**Direitos do trabalhador**:
- Saldo de salário proporcional
- Férias vencidas e proporcionais + 1/3
- 13º salário proporcional
- **Não há**: aviso prévio indenizado, multa FGTS, seguro-desemprego

### Rescisão Indireta (Justa Causa do Empregador)
Trabalhador tem os mesmos direitos da demissão sem justa causa quando:
- Empregador exige serviços superiores às forças
- Trata com rigor excessivo
- Não cumpre obrigações contratuais
- Comete ato lesivo à honra do empregado

## Cálculo das Verbas
- **Aviso prévio**: 1 salário + 3 dias por ano (máximo 90 dias)
- **Férias proporcionais**: (Salário ÷ 12) × meses trabalhados
- **13º proporcional**: (Salário ÷ 12) × meses trabalhados

**Base Legal**: CLT Arts. 477, 478, 479, 487, 488
**Prazo para pagamento**: Até 10º dia útil após rescisão
        """,
        "category": "labor_law",
        "subcategory": "contract_termination",
        "authority_level": 10,
        "legal_citations": ["CLT Art. 477", "CLT Art. 487", "CLT Art. 488"],
        "keywords": ["rescisão", "demissão", "aviso prévio", "FGTS", "verbas rescisórias"]
    },
    
    {
        "title": "Direito de Arrependimento em Compras Online",
        "content": """
O Código de Defesa do Consumidor garante direito de arrependimento nas compras realizadas fora do estabelecimento comercial.

## Prazo para Arrependimento
**7 (sete) dias corridos** contados da:
- Data de assinatura do contrato, ou
- Data de recebimento do produto

### Produtos Incluídos
- Compras online (e-commerce)
- Televendas e telemarketing  
- Vendas por catálogo
- Vendas domiciliares
- Qualquer compra fora do estabelecimento

## Como Exercer o Direito

### Procedimentos
1. **Comunicar a desistência** ao fornecedor (email, telefone, carta)
2. **Devolver o produto** nas mesmas condições recebidas
3. **Solicitar cancelamento** de cobrança no cartão/financiamento

### Responsabilidades
**Do consumidor**:
- Conservar produto em perfeitas condições
- Comunicar desistência dentro do prazo
- Devolver embalagem original

**Do fornecedor**:
- Aceitar a devolução sem questionamentos
- Restituir valores pagos
- Arcar com custos de devolução (frete reverso)

## Restituição de Valores
- **Prazo**: Imediato após solicitação
- **Forma**: Mesmo meio de pagamento usado
- **Valores incluídos**: Produto + frete de entrega
- **Juros e correção**: Aplicáveis em caso de atraso

## Exceções ao Direito
Não se aplica a:
- Produtos personalizados ou sob encomenda
- Produtos perecíveis ou de consumo imediato
- Produtos de higiene/íntimo abertos
- Conteúdo digital baixado
- Serviços já prestados com concordância

**Base Legal**: CDC Art. 49
**Multa por descumprimento**: R$ 200 a R$ 3 milhões
**Órgão fiscalizador**: Procon estadual/municipal
        """,
        "category": "consumer_law", 
        "subcategory": "online_commerce",
        "authority_level": 9,
        "legal_citations": ["CDC Art. 49", "Decreto 7962/2013"],
        "keywords": ["direito arrependimento", "compras online", "7 dias", "devolução", "e-commerce"]
    }
]

def seed_priority_content():
    """Seed high-priority legal content for immediate RAG improvement"""
    from backend.app import app
    from backend.retrieval import store_document_batch
    
    with app.app_context():
        success_count = 0
        for doc_data in PRIORITY_LEGAL_CONTENT:
            try:
                document = {
                    "id": str(uuid4()),
                    "title": doc_data["title"],
                    "content": doc_data["content"],
                    "category": doc_data["category"],
                    "subcategory": doc_data["subcategory"], 
                    "authority_level": doc_data["authority_level"],
                    "legal_citations": doc_data["legal_citations"],
                    "keywords": doc_data["keywords"],
                    "created_at": datetime.utcnow(),
                    "source": "manual_seed_priority"
                }
                
                store_document_batch([document])
                success_count += 1
                print(f"✅ Added: {doc_data['title']}")
                
            except Exception as e:
                print(f"❌ Failed to add {doc_data['title']}: {e}")
        
        print(f"\n🎉 Successfully seeded {success_count}/{len(PRIORITY_LEGAL_CONTENT)} documents")
        return success_count

if __name__ == "__main__":
    seed_priority_content()
```

## Weekly Content Schedule

### Week 1 Targets (50 documents)
- **Day 1**: Family law (união estável, regime de bens) - 5 docs
- **Day 2**: Labor law (CLT direitos básicos) - 8 docs  
- **Day 3**: Consumer law (compras online, garantias) - 7 docs
- **Day 4**: Business law (MEI, LTDA formation) - 10 docs
- **Day 5**: Civil law (contratos, responsabilidade civil) - 10 docs
- **Day 6**: Criminal law (crimes comuns, procedimentos) - 5 docs
- **Day 7**: Constitutional law (direitos fundamentais) - 5 docs

### Content Quality Standards
Each document must include:
- **Length**: 500-1000 words
- **Structure**: Clear headings and sections
- **Legal citations**: Official source references
- **Keywords**: 5-10 relevant legal terms
- **Authority level**: 1-10 ranking based on source
- **Practical examples**: Real-world applications

### Validation Process
1. **Legal accuracy check**: Compare with official sources
2. **Language accessibility**: Ensure clarity for general public
3. **Completeness**: Cover all major aspects of topic
4. **Citation verification**: Confirm all legal references
5. **SEO optimization**: Include relevant search terms

This seeding plan provides immediate content to resolve current RAG gaps and establish foundation for systematic growth.
