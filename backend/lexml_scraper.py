import os
import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class LexMLScraper:
    """Scraper for collecting legal documents from LexML portal"""
    
    def __init__(self, base_url: str = "https://www.lexml.gov.br", delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_constitution(self) -> List[Dict]:
        """Scrape Brazilian Constitution articles"""
        documents = []
        
        try:
            # Constitution URL pattern
            constitution_urls = [
                "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
                "https://www.senado.leg.br/atividade/const/con1988/con1988_05.05.2016/art_5_.asp"
            ]
            
            for url in constitution_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract articles
                    articles = self._extract_constitution_articles(soup, url)
                    documents.extend(articles)
                    
                    time.sleep(self.delay)
                    
                except Exception as e:
                    logger.error(f"Error scraping {url}: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(documents)} constitution articles")
            return documents
            
        except Exception as e:
            logger.error(f"Error in scrape_constitution: {str(e)}")
            return []
    
    def scrape_civil_code(self) -> List[Dict]:
        """Scrape Civil Code articles"""
        documents = []
        
        try:
            civil_code_url = "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406.htm"
            
            response = self.session.get(civil_code_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = self._extract_civil_code_articles(soup)
            documents.extend(articles)
            
            logger.info(f"Scraped {len(documents)} civil code articles")
            return documents
            
        except Exception as e:
            logger.error(f"Error scraping civil code: {str(e)}")
            return []
    
    def scrape_labor_law(self) -> List[Dict]:
        """Scrape Labor Law (CLT) articles"""
        documents = []
        
        try:
            clt_url = "https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm"
            
            response = self.session.get(clt_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = self._extract_clt_articles(soup)
            documents.extend(articles)
            
            logger.info(f"Scraped {len(documents)} CLT articles")
            return documents
            
        except Exception as e:
            logger.error(f"Error scraping CLT: {str(e)}")
            return []
    
    def scrape_recent_laws(self, limit: int = 50) -> List[Dict]:
        """Scrape recent laws and regulations"""
        documents = []
        
        try:
            # This would need to be adapted based on actual LexML API structure
            # For now, we'll create a placeholder implementation
            
            recent_laws_data = [
                {
                    "title": "Lei Geral de Proteção de Dados - LGPD",
                    "content": "Esta Lei dispõe sobre o tratamento de dados pessoais, inclusive nos meios digitais, por pessoa natural ou por pessoa jurídica de direito público ou privado, com o objetivo de proteger os direitos fundamentais de liberdade e de privacidade e o livre desenvolvimento da personalidade da pessoa natural.",
                    "category": "proteção_dados",
                    "source": "Lei 13.709/2018",
                    "article": "Art. 1º",
                    "law_number": "Lei 13.709/2018",
                    "date": "2018-08-14"
                },
                {
                    "title": "Marco Civil da Internet",
                    "content": "Esta Lei estabelece princípios, garantias, direitos e deveres para o uso da Internet no Brasil e determina as diretrizes para atuação da União, dos Estados, do Distrito Federal e dos Municípios em relação à matéria.",
                    "category": "direito_digital",
                    "source": "Lei 12.965/2014",
                    "article": "Art. 1º",
                    "law_number": "Lei 12.965/2014",
                    "date": "2014-04-23"
                }
            ]
            
            documents.extend(recent_laws_data)
            
            logger.info(f"Scraped {len(documents)} recent laws")
            return documents
            
        except Exception as e:
            logger.error(f"Error scraping recent laws: {str(e)}")
            return []
    
    def _extract_constitution_articles(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract articles from Constitution HTML"""
        articles = []
        
        try:
            # Look for article patterns
            article_patterns = [
                r'Art\.\s*(\d+º?)',
                r'Artigo\s*(\d+º?)',
                r'§\s*(\d+º?)'
            ]
            
            # Find all paragraphs that might contain articles
            paragraphs = soup.find_all(['p', 'div', 'span'])
            
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) < 50:  # Skip very short texts
                    continue
                
                # Check if this looks like an article
                for pattern in article_patterns:
                    match = re.search(pattern, text)
                    if match:
                        article_num = match.group(1)
                        
                        # Clean up the text
                        clean_text = re.sub(r'\s+', ' ', text).strip()
                        
                        if len(clean_text) > 100:  # Only include substantial content
                            articles.append({
                                "title": f"Constituição Federal - Art. {article_num}",
                                "content": clean_text,
                                "category": "direitos_fundamentais",
                                "source": "Constituição Federal",
                                "article": f"Art. {article_num}",
                                "law_number": "CF/1988",
                                "date": "1988-10-05",
                                "url": url
                            })
                        break
            
            return articles[:20]  # Limit to first 20 articles
            
        except Exception as e:
            logger.error(f"Error extracting constitution articles: {str(e)}")
            return []
    
    def _extract_civil_code_articles(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract articles from Civil Code HTML"""
        articles = []
        
        try:
            # Similar extraction logic for Civil Code
            paragraphs = soup.find_all(['p', 'div'])
            
            for p in paragraphs:
                text = p.get_text().strip()
                
                # Look for article patterns
                if re.search(r'Art\.\s*\d+', text) and len(text) > 100:
                    article_match = re.search(r'Art\.\s*(\d+)', text)
                    if article_match:
                        article_num = article_match.group(1)
                        
                        clean_text = re.sub(r'\s+', ' ', text).strip()
                        
                        articles.append({
                            "title": f"Código Civil - Art. {article_num}",
                            "content": clean_text,
                            "category": "direito_civil",
                            "source": "Código Civil",
                            "article": f"Art. {article_num}",
                            "law_number": "Lei 10.406/2002",
                            "date": "2002-01-10"
                        })
            
            return articles[:30]  # Limit to first 30 articles
            
        except Exception as e:
            logger.error(f"Error extracting civil code articles: {str(e)}")
            return []
    
    def _extract_clt_articles(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract articles from CLT HTML"""
        articles = []
        
        try:
            paragraphs = soup.find_all(['p', 'div'])
            
            for p in paragraphs:
                text = p.get_text().strip()
                
                if re.search(r'Art\.\s*\d+', text) and len(text) > 100:
                    article_match = re.search(r'Art\.\s*(\d+)', text)
                    if article_match:
                        article_num = article_match.group(1)
                        
                        clean_text = re.sub(r'\s+', ' ', text).strip()
                        
                        articles.append({
                            "title": f"CLT - Art. {article_num}",
                            "content": clean_text,
                            "category": "direito_trabalhista",
                            "source": "CLT",
                            "article": f"Art. {article_num}",
                            "law_number": "Decreto-Lei 5.452/1943",
                            "date": "1943-05-01"
                        })
            
            return articles[:25]  # Limit to first 25 articles
            
        except Exception as e:
            logger.error(f"Error extracting CLT articles: {str(e)}")
            return []
    
    def scrape_all_legal_documents(self) -> List[Dict]:
        """Scrape all available legal documents"""
        all_documents = []
        
        logger.info("Starting comprehensive legal document scraping...")
        
        # Scrape different legal sources
        constitution_docs = self.scrape_constitution()
        all_documents.extend(constitution_docs)
        
        civil_code_docs = self.scrape_civil_code()
        all_documents.extend(civil_code_docs)
        
        labor_law_docs = self.scrape_labor_law()
        all_documents.extend(labor_law_docs)
        
        recent_laws_docs = self.scrape_recent_laws()
        all_documents.extend(recent_laws_docs)
        
        logger.info(f"Total documents scraped: {len(all_documents)}")
        
        return all_documents
    
    def save_documents_to_file(self, documents: List[Dict], filename: str = "legal_documents.json"):
        """Save scraped documents to JSON file"""
        try:
            output_path = os.path.join(os.path.dirname(__file__), filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "documents": documents,
                    "total_count": len(documents),
                    "scraped_at": datetime.utcnow().isoformat(),
                    "scraper_version": "1.0.0"
                }, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(documents)} documents to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving documents: {str(e)}")
            return None

def main():
    """Main function for testing the scraper"""
    logging.basicConfig(level=logging.INFO)
    
    scraper = LexMLScraper()
    documents = scraper.scrape_all_legal_documents()
    
    if documents:
        output_file = scraper.save_documents_to_file(documents)
        print(f"Scraping completed. {len(documents)} documents saved to {output_file}")
    else:
        print("No documents were scraped.")

if __name__ == "__main__":
    main()
