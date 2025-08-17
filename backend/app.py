import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
import requests
from bs4 import BeautifulSoup
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS configuration
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins)

# OpenAI configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

class LegalRAGSystem:
    """RAG system for legal document processing and question answering"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.qa_chain = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.initialize_vectorstore()
    
    def initialize_vectorstore(self):
        """Initialize the vector database with legal documents"""
        try:
            # Initialize ChromaDB for local development
            persist_directory = os.path.join(os.path.dirname(__file__), 'chroma_db')
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
            
            # Initialize QA chain
            llm = OpenAI(temperature=0.2, max_tokens=1000)
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True
            )
            
            logger.info("RAG system initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing RAG system: {str(e)}")
            self.vectorstore = None
            self.qa_chain = None
    
    def add_legal_documents(self, documents: List[Dict]):
        """Add legal documents to the vector database"""
        if not self.vectorstore:
            logger.error("Vector store not initialized")
            return False
        
        try:
            texts = []
            metadatas = []
            
            for doc in documents:
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc['content'])
                
                for chunk in chunks:
                    texts.append(chunk)
                    metadatas.append({
                        'title': doc['title'],
                        'category': doc.get('category', 'unknown'),
                        'source': doc.get('source', 'unknown'),
                        'article': doc.get('article', ''),
                        'law_number': doc.get('law_number', ''),
                        'date': doc.get('date', '')
                    })
            
            # Add to vector store
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            self.vectorstore.persist()
            
            logger.info(f"Added {len(texts)} document chunks to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            return False
    
    def query_legal_documents(self, question: str) -> Dict:
        """Query the RAG system with a legal question"""
        if not self.qa_chain:
            return {
                "answer": "Sistema de IA não disponível no momento. Tente novamente mais tarde.",
                "sources": [],
                "confidence": 0.0
            }
        
        try:
            # Enhanced prompt for Brazilian legal context
            enhanced_question = f"""
            Baseado na legislação brasileira, responda a seguinte pergunta de forma clara e precisa:
            
            {question}
            
            Forneça uma resposta estruturada que inclua:
            1. Resposta direta à pergunta
            2. Base legal aplicável
            3. Orientações práticas quando relevante
            
            Pergunta: {question}
            """
            
            result = self.qa_chain({"query": enhanced_question})
            
            # Process sources
            sources = []
            if result.get('source_documents'):
                for doc in result['source_documents']:
                    sources.append({
                        'title': doc.metadata.get('title', 'Documento Legal'),
                        'category': doc.metadata.get('category', 'unknown'),
                        'article': doc.metadata.get('article', ''),
                        'content_preview': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        'relevance': 0.8  # Placeholder - could implement actual relevance scoring
                    })
            
            return {
                "answer": result['result'],
                "sources": sources,
                "confidence": 0.85  # Placeholder - could implement confidence scoring
            }
            
        except Exception as e:
            logger.error(f"Error querying RAG system: {str(e)}")
            return {
                "answer": "Erro ao processar sua pergunta. Tente reformular ou entre em contato com o suporte.",
                "sources": [],
                "confidence": 0.0
            }

# Initialize RAG system
rag_system = LegalRAGSystem()

# Sample legal data for initial testing
initial_legal_data = [
    {
        "title": "Constituição Federal - Art. 5º",
        "content": "Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade, nos termos seguintes: I - homens e mulheres são iguais em direitos e obrigações, nos termos desta Constituição; II - ninguém será obrigado a fazer ou deixar de fazer alguma coisa senão em virtude de lei;",
        "category": "direitos_fundamentais",
        "source": "Constituição Federal",
        "article": "Art. 5º",
        "law_number": "CF/1988"
    },
    {
        "title": "Código Civil - Art. 1º",
        "content": "Toda pessoa é capaz de direitos e deveres na ordem civil. A personalidade civil da pessoa começa do nascimento com vida; mas a lei põe a salvo, desde a concepção, os direitos do nascituro.",
        "category": "direito_civil",
        "source": "Código Civil",
        "article": "Art. 1º",
        "law_number": "Lei 10.406/2002"
    },
    {
        "title": "CLT - Art. 7º",
        "content": "São direitos dos trabalhadores urbanos e rurais, além de outros que visem à melhoria de sua condição social: I - relação de emprego protegida contra despedida arbitrária ou sem justa causa, nos termos de lei complementar, que preverá indenização compensatória, dentre outros direitos; II - seguro-desemprego, em caso de desemprego involuntário;",
        "category": "direito_trabalhista",
        "source": "CLT",
        "article": "Art. 7º",
        "law_number": "Decreto-Lei 5.452/1943"
    }
]

# Add initial data to RAG system
if rag_system.vectorstore:
    rag_system.add_legal_documents(initial_legal_data)

@app.route('/')
def home():
    return jsonify({
        "message": "JuSimples Legal AI API",
        "version": "2.0.0",
        "status": "running",
        "rag_system": "initialized" if rag_system.qa_chain else "error"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "rag_system": "operational" if rag_system.qa_chain else "unavailable",
        "vector_store": "connected" if rag_system.vectorstore else "disconnected"
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400
        
        if len(question) < 10:
            return jsonify({"error": "Pergunta muito curta. Forneça mais detalhes."}), 400
        
        logger.info(f"Processing question: {question[:100]}...")
        
        # Query RAG system
        result = rag_system.query_legal_documents(question)
        
        response = {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"],
            "timestamp": datetime.utcnow().isoformat(),
            "disclaimer": "Esta resposta é baseada em IA e tem caráter informativo. Para casos complexos, consulte um advogado especializado."
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in ask_question: {str(e)}")
        return jsonify({
            "error": "Erro interno do servidor",
            "message": "Não foi possível processar sua pergunta no momento."
        }), 500

@app.route('/api/search', methods=['POST'])
def search_legal():
    try:
        data = request.get_json()
        query = data.get('query', '').lower().strip()
        
        if not query:
            return jsonify({"error": "Query não fornecida"}), 400
        
        # Use RAG system for semantic search
        if rag_system.vectorstore:
            docs = rag_system.vectorstore.similarity_search(query, k=5)
            results = []
            
            for doc in docs:
                results.append({
                    "title": doc.metadata.get('title', 'Documento Legal'),
                    "content": doc.page_content,
                    "category": doc.metadata.get('category', 'unknown'),
                    "source": doc.metadata.get('source', 'unknown'),
                    "article": doc.metadata.get('article', ''),
                    "relevance": 0.8  # Placeholder
                })
            
            return jsonify({
                "query": query,
                "results": results,
                "total": len(results),
                "search_type": "semantic"
            })
        else:
            return jsonify({
                "query": query,
                "results": [],
                "total": 0,
                "error": "Sistema de busca não disponível"
            })
            
    except Exception as e:
        logger.error(f"Error in search_legal: {str(e)}")
        return jsonify({"error": "Erro na busca"}), 500

@app.route('/api/legal-data')
def get_legal_data():
    return jsonify({
        "data": initial_legal_data,
        "total": len(initial_legal_data),
        "last_updated": datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting JuSimples API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

