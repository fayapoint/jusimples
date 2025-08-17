import os
import logging
import asyncio
from typing import List, Dict
from datetime import datetime, timedelta
import json
from lexml_scraper import LexMLScraper
from app import rag_system

logger = logging.getLogger(__name__)

class LegalDataCollector:
    """Service for collecting and updating legal documents in the RAG system"""
    
    def __init__(self):
        self.scraper = LexMLScraper()
        self.last_update = None
        self.update_interval = timedelta(days=7)  # Update weekly
        self.data_file = os.path.join(os.path.dirname(__file__), 'legal_documents.json')
    
    def should_update_data(self) -> bool:
        """Check if data should be updated based on last update time"""
        if not os.path.exists(self.data_file):
            return True
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                last_update_str = data.get('scraped_at')
                
                if last_update_str:
                    last_update = datetime.fromisoformat(last_update_str.replace('Z', '+00:00'))
                    return datetime.utcnow() - last_update > self.update_interval
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking update status: {str(e)}")
            return True
    
    def collect_legal_documents(self) -> List[Dict]:
        """Collect legal documents from various sources"""
        logger.info("Starting legal document collection...")
        
        try:
            # Scrape documents from LexML and other sources
            documents = self.scraper.scrape_all_legal_documents()
            
            # Add additional curated legal content
            additional_docs = self._get_additional_legal_content()
            documents.extend(additional_docs)
            
            # Save to file
            if documents:
                self.scraper.save_documents_to_file(documents)
                logger.info(f"Collected and saved {len(documents)} legal documents")
            
            return documents
            
        except Exception as e:
            logger.error(f"Error collecting legal documents: {str(e)}")
            return []
    
    def update_rag_system(self, documents: List[Dict] = None) -> bool:
        """Update the RAG system with new legal documents"""
        try:
            if documents is None:
                # Load from file if no documents provided
                if os.path.exists(self.data_file):
                    with open(self.data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        documents = data.get('documents', [])
                else:
                    logger.warning("No documents file found, collecting new documents...")
                    documents = self.collect_legal_documents()
            
            if not documents:
                logger.error("No documents available to update RAG system")
                return False
            
            # Add documents to RAG system
            success = rag_system.add_legal_documents(documents)
            
            if success:
                logger.info(f"Successfully updated RAG system with {len(documents)} documents")
                self.last_update = datetime.utcnow()
                return True
            else:
                logger.error("Failed to update RAG system")
                return False
                
        except Exception as e:
            logger.error(f"Error updating RAG system: {str(e)}")
            return False
    
    def _get_additional_legal_content(self) -> List[Dict]:
        """Get additional curated legal content"""
        additional_content = [
            {
                "title": "Lei Maria da Penha - Lei 11.340/2006",
                "content": "Cria mecanismos para coibir a violência doméstica e familiar contra a mulher, nos termos do § 8º do art. 226 da Constituição Federal, da Convenção sobre a Eliminação de Todas as Formas de Discriminação contra as Mulheres e da Convenção Interamericana para Prevenir, Punir e Erradicar a Violência contra a Mulher; dispõe sobre a criação dos Juizados de Violência Doméstica e Familiar contra a Mulher; altera o Código de Processo Penal, o Código Penal e a Lei de Execução Penal; e dá outras providências.",
                "category": "direitos_da_mulher",
                "source": "Lei 11.340/2006",
                "article": "Art. 1º",
                "law_number": "Lei 11.340/2006",
                "date": "2006-08-07"
            },
            {
                "title": "Estatuto da Criança e do Adolescente - ECA",
                "content": "Dispõe sobre a proteção integral à criança e ao adolescente. É dever da família, da comunidade, da sociedade em geral e do poder público assegurar, com absoluta prioridade, a efetivação dos direitos referentes à vida, à saúde, à alimentação, à educação, ao esporte, ao lazer, à profissionalização, à cultura, à dignidade, ao respeito, à liberdade e à convivência familiar e comunitária.",
                "category": "direitos_da_crianca",
                "source": "Lei 8.069/1990",
                "article": "Art. 4º",
                "law_number": "Lei 8.069/1990",
                "date": "1990-07-13"
            },
            {
                "title": "Código de Defesa do Consumidor",
                "content": "O presente código estabelece normas de proteção e defesa do consumidor, de ordem pública e interesse social, nos termos dos arts. 5º, inciso XXXII, 170, inciso V, da Constituição Federal e art. 48 de suas Disposições Transitórias. Consumidor é toda pessoa física ou jurídica que adquire ou utiliza produto ou serviço como destinatário final.",
                "category": "direito_consumidor",
                "source": "Lei 8.078/1990",
                "article": "Art. 1º e 2º",
                "law_number": "Lei 8.078/1990",
                "date": "1990-09-11"
            },
            {
                "title": "Lei de Improbidade Administrativa",
                "content": "Esta lei dispõe sobre as sanções aplicáveis aos agentes públicos nos casos de enriquecimento ilícito no exercício de mandato, cargo, emprego ou função na administração pública direta, indireta ou fundacional e dá outras providências. Constitui ato de improbidade administrativa que atenta contra os princípios da administração pública qualquer ação ou omissão que viole os deveres de honestidade, imparcialidade, legalidade, e lealdade às instituições.",
                "category": "direito_administrativo",
                "source": "Lei 8.429/1992",
                "article": "Art. 1º e 11",
                "law_number": "Lei 8.429/1992",
                "date": "1992-06-02"
            },
            {
                "title": "Lei de Acesso à Informação",
                "content": "Regula o acesso a informações previsto no inciso XXXIII do art. 5º, no inciso II do § 3º do art. 37 e no § 2º do art. 216 da Constituição Federal; altera a Lei nº 8.112, de 11 de dezembro de 1990; revoga a Lei nº 11.111, de 5 de maio de 2005, e dispositivos da Lei nº 8.159, de 8 de janeiro de 1991; e dá outras providências. É dever do Estado garantir o direito de acesso à informação, que será franqueada, mediante procedimentos objetivos e ágeis, de forma transparente, clara e em linguagem de fácil compreensão.",
                "category": "transparencia_publica",
                "source": "Lei 12.527/2011",
                "article": "Art. 1º e 5º",
                "law_number": "Lei 12.527/2011",
                "date": "2011-11-18"
            }
        ]
        
        return additional_content
    
    async def periodic_update(self):
        """Periodically update legal documents"""
        while True:
            try:
                if self.should_update_data():
                    logger.info("Starting periodic legal document update...")
                    
                    # Collect new documents
                    documents = self.collect_legal_documents()
                    
                    if documents:
                        # Update RAG system
                        self.update_rag_system(documents)
                        logger.info("Periodic update completed successfully")
                    else:
                        logger.warning("No documents collected during periodic update")
                
                # Wait for next update cycle (24 hours)
                await asyncio.sleep(24 * 60 * 60)
                
            except Exception as e:
                logger.error(f"Error in periodic update: {str(e)}")
                await asyncio.sleep(60 * 60)  # Wait 1 hour before retrying
    
    def initialize_data(self):
        """Initialize the system with legal data"""
        logger.info("Initializing legal data...")
        
        try:
            # Check if we have existing data
            if os.path.exists(self.data_file):
                logger.info("Loading existing legal documents...")
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    documents = data.get('documents', [])
                
                if documents:
                    self.update_rag_system(documents)
                    logger.info(f"Loaded {len(documents)} existing documents")
                    return True
            
            # No existing data, collect new documents
            logger.info("No existing data found, collecting new documents...")
            documents = self.collect_legal_documents()
            
            if documents:
                self.update_rag_system(documents)
                return True
            else:
                logger.error("Failed to initialize legal data")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing legal data: {str(e)}")
            return False

# Global data collector instance
data_collector = LegalDataCollector()

def initialize_legal_data():
    """Initialize legal data for the application"""
    return data_collector.initialize_data()

def start_periodic_updates():
    """Start periodic updates in background"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(data_collector.periodic_update())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize data
    success = initialize_legal_data()
    
    if success:
        print("Legal data initialization completed successfully")
    else:
        print("Legal data initialization failed")
