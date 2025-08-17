#!/usr/bin/env python3
"""
Test script for JuSimples RAG system
Tests the legal document retrieval and AI question answering
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_functionality():
    """Test basic system functionality without AI"""
    logger.info("Testing basic functionality...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            assert response.status_code == 200
            data = response.get_json()
            logger.info(f"Health check: {data['status']}")
            
            # Test legal data endpoint
            response = client.get('/api/legal-data')
            assert response.status_code == 200
            data = response.get_json()
            logger.info(f"Legal data: {data['total']} documents available")
            
            # Test search endpoint
            response = client.post('/api/search', 
                                 json={'query': 'constituição'})
            assert response.status_code == 200
            data = response.get_json()
            logger.info(f"Search results: {data['total']} documents found")
            
        logger.info("✓ Basic functionality tests passed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Basic functionality test failed: {str(e)}")
        return False

def test_rag_system():
    """Test RAG system functionality"""
    logger.info("Testing RAG system...")
    
    try:
        from app import rag_system
        
        # Test vector store initialization
        if rag_system.vectorstore is None:
            logger.warning("Vector store not initialized - testing in fallback mode")
            return test_fallback_mode()
        
        # Test document addition
        test_docs = [
            {
                "title": "Test Document",
                "content": "Este é um documento de teste sobre direitos fundamentais na Constituição Federal brasileira.",
                "category": "test",
                "source": "Test",
                "article": "Test Art. 1",
                "law_number": "Test/2024"
            }
        ]
        
        success = rag_system.add_legal_documents(test_docs)
        if success:
            logger.info("✓ Document addition successful")
        else:
            logger.warning("Document addition failed")
        
        # Test semantic search
        if rag_system.vectorstore:
            docs = rag_system.vectorstore.similarity_search("direitos fundamentais", k=3)
            logger.info(f"✓ Semantic search returned {len(docs)} documents")
        
        # Test question answering
        test_questions = [
            "O que são direitos fundamentais?",
            "Quais são os direitos dos trabalhadores?",
            "Como funciona o Código Civil?"
        ]
        
        for question in test_questions:
            try:
                result = rag_system.query_legal_documents(question)
                logger.info(f"Question: {question}")
                logger.info(f"Answer preview: {result['answer'][:100]}...")
                logger.info(f"Confidence: {result['confidence']}")
                logger.info(f"Sources: {len(result['sources'])}")
                logger.info("-" * 40)
            except Exception as e:
                logger.error(f"Error answering question '{question}': {str(e)}")
        
        logger.info("✓ RAG system tests completed")
        return True
        
    except Exception as e:
        logger.error(f"✗ RAG system test failed: {str(e)}")
        return False

def test_fallback_mode():
    """Test system in fallback mode (without AI)"""
    logger.info("Testing fallback mode...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test ask endpoint in fallback mode
            response = client.post('/api/ask', 
                                 json={'question': 'O que são direitos fundamentais?'})
            
            if response.status_code == 200:
                data = response.get_json()
                logger.info("✓ Fallback mode working")
                logger.info(f"Answer: {data['answer'][:100]}...")
                return True
            else:
                logger.error(f"✗ Fallback mode failed: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"✗ Fallback mode test failed: {str(e)}")
        return False

def test_data_collection():
    """Test legal data collection"""
    logger.info("Testing data collection...")
    
    try:
        from data_collector import LegalDataCollector
        
        collector = LegalDataCollector()
        
        # Test document collection (limited for testing)
        documents = collector._get_additional_legal_content()
        logger.info(f"✓ Collected {len(documents)} additional legal documents")
        
        # Test data file operations
        if documents:
            output_file = collector.scraper.save_documents_to_file(documents, "test_documents.json")
            if output_file and os.path.exists(output_file):
                logger.info("✓ Document saving successful")
                # Clean up test file
                os.remove(output_file)
            else:
                logger.warning("Document saving failed")
        
        logger.info("✓ Data collection tests completed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Data collection test failed: {str(e)}")
        return False

def generate_test_report():
    """Generate a comprehensive test report"""
    logger.info("Generating test report...")
    
    report = {
        "test_timestamp": datetime.utcnow().isoformat(),
        "system_info": {
            "python_version": sys.version,
            "platform": sys.platform
        },
        "tests": {}
    }
    
    # Run all tests
    tests = [
        ("basic_functionality", test_basic_functionality),
        ("rag_system", test_rag_system),
        ("data_collection", test_data_collection)
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            result = test_func()
            report["tests"][test_name] = {
                "status": "passed" if result else "failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            report["tests"][test_name] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    # Save report
    report_file = os.path.join(os.path.dirname(__file__), "test_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for test in report["tests"].values() if test["status"] == "passed")
    failed = sum(1 for test in report["tests"].values() if test["status"] == "failed")
    errors = sum(1 for test in report["tests"].values() if test["status"] == "error")
    
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Errors: {errors}")
    logger.info(f"Report saved to: {report_file}")
    
    return passed > 0 and failed == 0 and errors == 0

def main():
    """Main test function"""
    logger.info("JuSimples RAG System Test Suite")
    logger.info("="*50)
    
    success = generate_test_report()
    
    if success:
        logger.info("🎉 All tests passed!")
        return True
    else:
        logger.error("❌ Some tests failed. Check the report for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
