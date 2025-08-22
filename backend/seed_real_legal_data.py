#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed JuSimples Database with Real Brazilian Legal Data
Replaces mock data with comprehensive legal content
"""

import os
import uuid
import logging
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Import our new database utility module
from db_utils import get_db_manager, initialize_schema
from openai import OpenAI

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_comprehensive_legal_data() -> List[Dict]:
    """Return comprehensive Brazilian legal data to replace mock content"""
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Constituição Federal - Art. 5º - Direitos e Garantias Fundamentais",
            "content": """Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade, nos termos seguintes:
I - homens e mulheres são iguais em direitos e obrigações;
II - ninguém será obrigado a fazer ou deixar de fazer alguma coisa senão em virtude de lei;
III - ninguém será submetido a tortura nem a tratamento desumano ou degradante;
IV - é livre a manifestação do pensamento, sendo vedado o anonimato;
V - é assegurado o direito de resposta, proporcional ao agravo;""",
            "category": "direitos_fundamentais",
            "keywords": ["direitos fundamentais", "igualdade", "liberdade", "vida", "segurança", "propriedade", "constituição"],
            "source": "Constituição Federal de 1988",
            "article": "Art. 5º",
            "law_type": "constitucional",
            "relevance_score": 1.0
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Código Civil - Personalidade Jurídica e Capacidade Civil",
            "content": """Art. 1º Toda pessoa é capaz de direitos e deveres na ordem civil.
Art. 2º A personalidade civil da pessoa começa do nascimento com vida; mas a lei põe a salvo, desde a concepção, os direitos do nascituro.
Art. 3º São absolutamente incapazes de exercer pessoalmente os atos da vida civil os menores de 16 anos.
Art. 4º São incapazes, relativamente a certos atos ou à maneira de os exercer: I - os maiores de dezesseis e menores de dezoito anos; II - os ébrios habituais e os viciados em tóxicos; III - aqueles que, por causa transitória ou permanente, não puderem exprimir sua vontade.""",
            "category": "direito_civil",
            "keywords": ["personalidade civil", "capacidade", "nascimento", "nascituro", "incapacidade", "menores"],
            "source": "Código Civil - Lei 10.406/2002",
            "article": "Arts. 1º a 4º",
            "law_type": "civil",
            "relevance_score": 0.9
        },
        {
            "id": str(uuid.uuid4()),
            "title": "CLT - Direitos Trabalhistas Fundamentais",
            "content": """Art. 7º São direitos dos trabalhadores urbanos e rurais, além de outros que visem à melhoria de sua condição social:
I - relação de emprego protegida contra despedida arbitrária ou sem justa causa;
II - seguro-desemprego, em caso de desemprego involuntário;
IV - salário mínimo, fixado em lei, nacionalmente unificado;
VI - irredutibilidade do salário, salvo o disposto em convenção ou acordo coletivo;
XIII - décimo terceiro salário com base na remuneração integral;
XV - repouso semanal remunerado, preferencialmente aos domingos;
XVII - gozo de férias anuais remuneradas com, pelo menos, um terço a mais do que o salário normal.""",
            "category": "direito_trabalhista",
            "keywords": ["trabalho", "emprego", "salário", "férias", "demissão", "CLT", "trabalhador", "direitos trabalhistas"],
            "source": "Consolidação das Leis do Trabalho - Decreto-Lei 5.452/1943",
            "article": "Art. 7º",
            "law_type": "trabalhista",
            "relevance_score": 0.95
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Código de Defesa do Consumidor - Direitos Básicos",
            "content": """Art. 6º São direitos básicos do consumidor:
I - a proteção da vida, saúde e segurança contra os riscos provocados por práticas no fornecimento de produtos e serviços considerados perigosos ou nocivos;
II - a educação e divulgação sobre o consumo adequado dos produtos e serviços;
III - a informação adequada e clara sobre os diferentes produtos e serviços;
IV - a proteção contra a publicidade enganosa e abusiva;
V - a proteção contratual;
VI - a prevenção e a reparação de danos patrimoniais e morais, individuais, coletivos e difusos;
VII - o acesso aos órgãos judiciários e administrativos com vistas à prevenção ou reparação de danos.""",
            "category": "direito_consumidor",
            "keywords": ["consumidor", "proteção", "publicidade enganosa", "produto defeituoso", "garantia", "CDC", "direitos do consumidor"],
            "source": "Código de Defesa do Consumidor - Lei 8.078/1990",
            "article": "Art. 6º",
            "law_type": "consumidor",
            "relevance_score": 0.9
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Direito de Família - Alimentos e Pensão Alimentícia",
            "content": """Art. 1.694. Podem os parentes, os cônjuges ou companheiros pedir uns aos outros os alimentos de que necessitem para viver de modo compatível com a sua condição social, inclusive para atender às necessidades de educação.
Art. 1.695. São devidos os alimentos quando quem os pretende não tem bens suficientes, nem pode prover, pelo seu trabalho, à própria mantença, e aquele, de quem se reclamam, pode fornecê-los, sem desfalque do necessário ao seu sustento.
Art. 1.696. O direito à prestação de alimentos é recíproco entre pais e filhos, e extensivo a todos os ascendentes, recaindo a obrigação nos mais próximos em grau, uns em falta de outros.""",
            "category": "direito_familia",
            "keywords": ["pensão alimentícia", "família", "filhos", "divórcio", "alimentos", "obrigação alimentar", "pais"],
            "source": "Código Civil - Lei 10.406/2002",
            "article": "Arts. 1.694 a 1.696",
            "law_type": "familia",
            "relevance_score": 0.85
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Direito Penal - Crimes Contra a Pessoa",
            "content": """Art. 121. Matar alguém: Pena - reclusão, de seis a vinte anos.
§ 1º Se o agente comete o crime impelido por motivo de relevante valor social ou moral, ou sob o domínio de violenta emoção, logo em seguida a injusta provocação da vítima, o juiz pode reduzir a pena de um sexto a um terço.
Art. 129. Ofender a integridade corporal ou a saúde de outrem: Pena - detenção, de três meses a um ano.
Art. 138. Caluniar alguém, imputando-lhe falsamente fato definido como crime: Pena - detenção, de seis meses a dois anos, e multa.""",
            "category": "direito_penal",
            "keywords": ["crimes", "homicídio", "lesão corporal", "calúnia", "código penal", "penas"],
            "source": "Código Penal - Decreto-Lei 2.848/1940",
            "article": "Arts. 121, 129, 138",
            "law_type": "penal",
            "relevance_score": 0.8
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Estatuto da Criança e do Adolescente - Direitos Fundamentais",
            "content": """Art. 3º A criança e o adolescente gozam de todos os direitos fundamentais inerentes à pessoa humana, sem prejuízo da proteção integral de que trata esta Lei, assegurando-se-lhes, por lei ou por outros meios, todas as oportunidades e facilidades, a fim de lhes facultar o desenvolvimento físico, mental, moral, espiritual e social, em condições de liberdade e de dignidade.
Art. 4º É dever da família, da comunidade, da sociedade em geral e do poder público assegurar, com absoluta prioridade, a efetivação dos direitos referentes à vida, à saúde, à alimentação, à educação, ao esporte, ao lazer, à profissionalização, à cultura, à dignidade, ao respeito, à liberdade e à convivência familiar e comunitária.""",
            "category": "direito_crianca_adolescente",
            "keywords": ["criança", "adolescente", "ECA", "proteção integral", "direitos fundamentais", "família"],
            "source": "Estatuto da Criança e do Adolescente - Lei 8.069/1990",
            "article": "Arts. 3º e 4º",
            "law_type": "especial",
            "relevance_score": 0.85
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Lei Maria da Penha - Violência Doméstica",
            "content": """Art. 5º Para os efeitos desta Lei, configura violência doméstica e familiar contra a mulher qualquer ação ou omissão baseada no gênero que lhe cause morte, lesão, sofrimento físico, sexual ou psicológico e dano moral ou patrimonial:
I - no âmbito da unidade doméstica;
II - no âmbito da família;
III - em qualquer relação íntima de afeto.
Art. 7º São formas de violência doméstica e familiar contra a mulher, entre outras:
I - a violência física;
II - a violência psicológica;
III - a violência sexual;
IV - a violência patrimonial;
V - a violência moral.""",
            "category": "direito_mulher",
            "keywords": ["violência doméstica", "maria da penha", "mulher", "violência psicológica", "proteção"],
            "source": "Lei Maria da Penha - Lei 11.340/2006",
            "article": "Arts. 5º e 7º",
            "law_type": "especial",
            "relevance_score": 0.9
        },
        {
            "id": str(uuid.uuid4()),
            "title": "LGPD - Lei Geral de Proteção de Dados",
            "content": """Art. 1º Esta Lei dispõe sobre o tratamento de dados pessoais, inclusive nos meios digitais, por pessoa natural ou por pessoa jurídica de direito público ou privado, com o objetivo de proteger os direitos fundamentais de liberdade e de privacidade e o livre desenvolvimento da personalidade da pessoa natural.
Art. 5º Para os fins desta Lei, considera-se:
I - dado pessoal: informação relacionada a pessoa natural identificada ou identificável;
II - dado pessoal sensível: dado pessoal sobre origem racial ou étnica, convicção religiosa, opinião política, filiação a sindicato ou a organização de caráter religioso, filosófico ou político, dado referente à saúde ou à vida sexual, dado genético ou biométrico.""",
            "category": "direito_digital",
            "keywords": ["LGPD", "dados pessoais", "privacidade", "proteção de dados", "consentimento"],
            "source": "Lei Geral de Proteção de Dados - Lei 13.709/2018",
            "article": "Arts. 1º e 5º",
            "law_type": "especial",
            "relevance_score": 0.95
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Marco Civil da Internet",
            "content": """Art. 2º A disciplina do uso da internet no Brasil tem como fundamento o respeito à liberdade de expressão, bem como:
I - o reconhecimento da escala mundial da rede;
II - os direitos humanos, o desenvolvimento da personalidade e o exercício da cidadania em meios digitais;
III - a pluralidade e a diversidade;
IV - a abertura e a colaboração;
V - a livre iniciativa, a livre concorrência e a defesa do consumidor;
VI - a finalidade social da rede.
Art. 3º A disciplina do uso da internet no Brasil tem os seguintes princípios:
I - garantia da liberdade de expressão, comunicação e manifestação de pensamento;
II - proteção da privacidade;
III - proteção dos dados pessoais.""",
            "category": "direito_digital",
            "keywords": ["marco civil", "internet", "liberdade de expressão", "privacidade", "direitos digitais"],
            "source": "Marco Civil da Internet - Lei 12.965/2014",
            "article": "Arts. 2º e 3º",
            "law_type": "especial",
            "relevance_score": 0.9
        }
    ]

def get_openai_client() -> Optional[OpenAI]:
    """Initialize OpenAI client with retry logic"""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your_openai_api_key_here":
        logger.warning("⚠️ No OpenAI API key provided")
        return None
        
    try:
        client = OpenAI(api_key=api_key)
        # Quick verification test
        models = client.models.list()
        if models:
            logger.info("✅ OpenAI client initialized successfully")
            return client
        else:
            logger.warning("⚠️ OpenAI client initialized but no models found")
            return None
    except Exception as e:
        logger.error(f"❌ Failed to initialize OpenAI client: {e}")
        return None

def seed_database_with_real_data():
    """Seed the database with comprehensive Brazilian legal data"""
    try:
        # Get database manager from our new utility module
        db_manager = get_db_manager()
        
        logger.info("🌱 Starting database seeding with real legal data...")
        
        # Initialize database schema
        if not initialize_schema():
            logger.error("❌ Failed to initialize database schema")
            return False
        
        if not db_manager.is_ready():
            logger.error("❌ Database not ready for seeding")
            return False
        
        # Get a fresh connection
        conn = db_manager.get_connection(force_new=True)
        if not conn:
            logger.error("❌ Could not establish database connection")
            return False
        
        # Get comprehensive legal data
        legal_data = get_comprehensive_legal_data()
        logger.info(f"📚 Prepared {len(legal_data)} legal documents for seeding")
        
        # Clear existing mock data and seed with real data
        try:
            with conn.cursor() as cur:
                # Clear existing mock data
                cur.execute("DELETE FROM legal_chunks WHERE title LIKE '%mock%' OR title LIKE '%test%'")
                logger.info("🧹 Cleared existing mock data")
                
                # Insert real legal data
                inserted_count = 0
                openai_client = get_openai_client()
                
                for doc in legal_data:
                    try:
                        # Generate embedding if OpenAI is available
                        embedding = None
                        if openai_client:
                            try:
                                response = openai_client.embeddings.create(
                                    model="text-embedding-3-small",
                                    input=doc["content"]
                                )
                                embedding = response.data[0].embedding
                                logger.info(f"✅ Generated embedding for {doc['title'][:30]}...")
                            except Exception as e:
                                logger.warning(f"Failed to generate embedding for {doc['title'][:30]}: {e}")
                        
                        # Prepare metadata
                        metadata = {
                            "source": doc.get("source", ""),
                            "article": doc.get("article", ""),
                            "law_type": doc.get("law_type", ""),
                            "relevance_score": doc.get("relevance_score", 0.5),
                            "keywords": doc.get("keywords", [])
                        }
                        
                        # Insert document
                        cur.execute("""
                            INSERT INTO legal_chunks (id, title, content, category, metadata, embedding)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO UPDATE SET
                                title = EXCLUDED.title,
                                content = EXCLUDED.content,
                                category = EXCLUDED.category,
                                metadata = EXCLUDED.metadata,
                                embedding = EXCLUDED.embedding
                        """, (
                            doc["id"],
                            doc["title"],
                            doc["content"],
                            doc["category"],
                            metadata,
                            embedding
                        ))
                        inserted_count += 1
                        logger.info(f"✅ Inserted document: {doc['title'][:30]}...")
                        
                    except Exception as e:
                        logger.error(f"Failed to insert document {doc['title'][:30]}: {e}")
                        continue
                
                conn.commit()
                logger.info(f"✅ Successfully seeded database with {inserted_count} real legal documents")
                
                # Verify seeding
                cur.execute("SELECT COUNT(*) FROM legal_chunks")
                total_count = cur.fetchone()[0]
                logger.info(f"📊 Total documents in database: {total_count}")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Error during data seeding: {e}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Critical error during database seeding: {e}")
        return False

if __name__ == "__main__":
    print("Starting database seeding...")
    success = seed_database_with_real_data()
    if success:
        print("\n✅ Database seeding completed successfully!")
    else:
        print("\n❌ Database seeding failed!")
        exit(1)
