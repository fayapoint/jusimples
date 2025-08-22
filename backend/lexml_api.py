#!/usr/bin/env python3
"""
LexML API Integration for JuSimples
Provides access to LexML (Brazil's legal information API) for enhanced recommendation functionality
"""
import os
import json
import time
import logging
import requests
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lexml_api")

# LexML API configuration
LEXML_BASE_URL = "https://www.lexml.gov.br/busca/api/v1"
DEFAULT_TIMEOUT = 10  # seconds

class LexMLAPI:
    """Interface for LexML API operations"""
    
    def __init__(self, base_url: str = None):
        """Initialize the LexML API client"""
        self.base_url = base_url or LEXML_BASE_URL
        self.last_error = None
        self.last_request_time = None
        self.last_response_time = None
        self.request_count = 0
        self.error_count = 0
        
    def search(
        self, 
        query: str, 
        max_results: int = 10,
        document_type: str = None,
        sort_by: str = "relevance",
        locale: str = "pt_BR"
    ) -> Dict[str, Any]:
        """
        Search for legal documents using LexML API
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            document_type: Filter by document type (lei, decreto, etc)
            sort_by: Sort method - relevance, date, title
            locale: Language locale (pt_BR by default)
            
        Returns:
            Dictionary with search results and metadata
        """
        self.last_request_time = time.time()
        
        # Build query parameters
        params = {
            "q": query,
            "maxResults": max_results,
            "format": "json",
            "orderBy": sort_by,
            "locale": locale
        }
        
        # Add document type filter if provided
        if document_type:
            params["tipo"] = document_type
            
        # Initialize result structure
        result = {
            "success": False,
            "query": query,
            "results": [],
            "total_found": 0,
            "execution_time_ms": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "error": None
        }
        
        try:
            # Build URL
            url = f"{self.base_url}/consulta"
            
            # Make the request
            logger.info(f"🔍 LexML API search for: '{query[:50]}...'")
            response = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
            self.last_response_time = time.time()
            self.request_count += 1
            
            # Calculate execution time
            execution_time = self.last_response_time - self.last_request_time
            result["execution_time_ms"] = int(execution_time * 1000)
            
            # Check if request was successful
            if response.status_code == 200:
                # Parse response
                data = response.json()
                
                # Extract results
                result["success"] = True
                result["total_found"] = data.get("metadados", {}).get("totalEncontrado", 0)
                
                # Process each document
                for item in data.get("documentos", []):
                    result["results"].append({
                        "id": item.get("urn", ""),
                        "type": item.get("tipo", ""),
                        "title": item.get("titulo", ""),
                        "description": item.get("ementa", ""),
                        "date": item.get("data", ""),
                        "authority": item.get("autoridade", ""),
                        "url": item.get("url", ""),
                        "score": item.get("relevancia", 0),
                        "status": item.get("situacao", "")
                    })
                    
                logger.info(f"✅ LexML search found {result['total_found']} results in {execution_time:.2f}s")
            else:
                # Handle error
                self.error_count += 1
                result["error"] = f"HTTP error {response.status_code}: {response.text}"
                logger.error(f"❌ LexML API error: {result['error']}")
                
        except requests.Timeout:
            # Handle timeout
            self.error_count += 1
            result["error"] = f"Request timed out after {DEFAULT_TIMEOUT} seconds"
            logger.error(f"⏱️ LexML API timeout: {result['error']}")
            
        except requests.RequestException as e:
            # Handle request exception
            self.error_count += 1
            result["error"] = f"Request error: {str(e)}"
            logger.error(f"❌ LexML API request error: {result['error']}")
            
        except Exception as e:
            # Handle unexpected exceptions
            self.error_count += 1
            result["error"] = f"Unexpected error: {type(e).__name__}: {str(e)}"
            logger.error(f"❌ LexML API unexpected error: {result['error']}")
            
        # Store last error if any
        self.last_error = result["error"]
        
        return result
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """
        Get document details by its ID (URN)
        
        Args:
            document_id: Document URN identifier
            
        Returns:
            Dictionary with document details
        """
        self.last_request_time = time.time()
        
        # Initialize result structure
        result = {
            "success": False,
            "document": None,
            "execution_time_ms": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "error": None
        }
        
        try:
            # Encode document ID
            encoded_id = quote_plus(document_id)
            
            # Build URL
            url = f"{self.base_url}/documento/{encoded_id}"
            
            # Make the request
            logger.info(f"📄 LexML API fetching document: {document_id}")
            response = requests.get(url, params={"format": "json"}, timeout=DEFAULT_TIMEOUT)
            self.last_response_time = time.time()
            self.request_count += 1
            
            # Calculate execution time
            execution_time = self.last_response_time - self.last_request_time
            result["execution_time_ms"] = int(execution_time * 1000)
            
            # Check if request was successful
            if response.status_code == 200:
                # Parse response
                data = response.json()
                
                # Extract document details
                result["success"] = True
                result["document"] = {
                    "id": data.get("urn", ""),
                    "type": data.get("tipo", ""),
                    "title": data.get("titulo", ""),
                    "description": data.get("ementa", ""),
                    "full_text": data.get("textoIntegral", ""),
                    "date": data.get("data", ""),
                    "authority": data.get("autoridade", ""),
                    "url": data.get("url", ""),
                    "status": data.get("situacao", ""),
                    "related_docs": []
                }
                
                # Extract related documents
                for related in data.get("relacionados", []):
                    result["document"]["related_docs"].append({
                        "id": related.get("urn", ""),
                        "type": related.get("tipo", ""),
                        "title": related.get("titulo", ""),
                        "relationship": related.get("tipoRelacao", "")
                    })
                    
                logger.info(f"✅ LexML document fetched in {execution_time:.2f}s")
            else:
                # Handle error
                self.error_count += 1
                result["error"] = f"HTTP error {response.status_code}: {response.text}"
                logger.error(f"❌ LexML API error: {result['error']}")
                
        except requests.Timeout:
            # Handle timeout
            self.error_count += 1
            result["error"] = f"Request timed out after {DEFAULT_TIMEOUT} seconds"
            logger.error(f"⏱️ LexML API timeout: {result['error']}")
            
        except requests.RequestException as e:
            # Handle request exception
            self.error_count += 1
            result["error"] = f"Request error: {str(e)}"
            logger.error(f"❌ LexML API request error: {result['error']}")
            
        except Exception as e:
            # Handle unexpected exceptions
            self.error_count += 1
            result["error"] = f"Unexpected error: {type(e).__name__}: {str(e)}"
            logger.error(f"❌ LexML API unexpected error: {result['error']}")
            
        # Store last error if any
        self.last_error = result["error"]
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the LexML API client"""
        return {
            "base_url": self.base_url,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "last_error": self.last_error,
            "last_request_time": self.last_request_time,
            "timestamp": datetime.utcnow().isoformat()
        }

# Singleton instance
lexml_api = LexMLAPI()

# Convenience functions
def search_legal_documents(query: str, **kwargs) -> Dict[str, Any]:
    """Search for legal documents using the LexML API"""
    return lexml_api.search(query=query, **kwargs)

def get_legal_document(document_id: str) -> Dict[str, Any]:
    """Get document details by its ID (URN)"""
    return lexml_api.get_document(document_id)

def get_lexml_status() -> Dict[str, Any]:
    """Get the current status of the LexML API client"""
    return lexml_api.get_status()

# API status endpoint handler (for app.py integration)
def handle_lexml_status_request():
    """Handle LexML API status request for integration with Flask"""
    # Perform a simple search to test the API
    test_query = "código civil"
    test_result = None
    
    try:
        test_result = lexml_api.search(
            query=test_query,
            max_results=1
        )
    except Exception:
        pass
        
    return {
        "status": lexml_api.get_status(),
        "test_query": test_query,
        "test_result": test_result
    }
