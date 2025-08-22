#!/usr/bin/env python3
"""
OpenAI API utilities for JuSimples
Handles API key management, token/cost tracking, and provides centralized API access
"""
import os
import json
import time
import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openai_utils")

# OpenAI model configurations with cost tracking
MODEL_CONFIGS = {
    "gpt-4o": {
        "input_cost_per_1k": 0.005,  # $0.005 per 1K input tokens
        "output_cost_per_1k": 0.015,  # $0.015 per 1K output tokens
        "supports_json_mode": True,
        "max_tokens": 128000,
        "display_name": "GPT-4o"
    },
    "gpt-4o-mini": {
        "input_cost_per_1k": 0.00015,  # $0.00015 per 1K input tokens
        "output_cost_per_1k": 0.0006,  # $0.0006 per 1K output tokens
        "supports_json_mode": True,
        "max_tokens": 128000,
        "display_name": "GPT-4o Mini"
    },
    "gpt-3.5-turbo": {
        "input_cost_per_1k": 0.0005,   # $0.0005 per 1K input tokens
        "output_cost_per_1k": 0.0015,  # $0.0015 per 1K output tokens
        "supports_json_mode": True,
        "max_tokens": 16385,
        "display_name": "GPT-3.5 Turbo"
    },
    "gpt-5-nano": {  # Use this as default since it might be renamed gpt-4o-mini
        "input_cost_per_1k": 0.00015,
        "output_cost_per_1k": 0.0006,
        "supports_json_mode": True,
        "max_tokens": 128000,
        "display_name": "GPT-5 Nano (alias for gpt-4o-mini)"
    }
}

# Default fallback model order
FALLBACK_MODELS = ["gpt-5-nano", "gpt-4o-mini", "gpt-3.5-turbo"]

class OpenAIManager:
    """Manages OpenAI API interactions with error handling and usage tracking"""
    
    def __init__(self):
        """Initialize the OpenAI manager"""
        # Force reload environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
            
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.preferred_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.client = None
        self.active_model = None
        self.initialized = False
        self.last_error = None
        self.usage_stats = {
            "total_tokens": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0,
            "request_count": 0,
            "error_count": 0
        }
        
        # Initialize client if possible
        self.initialize()
        
    def initialize(self) -> bool:
        """Initialize the OpenAI client with key validation"""
        self.last_error = None
        self.initialized = False
        
        # Validate API key
        if not self._validate_api_key():
            self.last_error = "Invalid API key"
            logger.warning(f"❌ OpenAI API key validation failed: {self.last_error}")
            return False
            
        try:
            # Create client
            self.client = OpenAI(api_key=self.api_key.strip())
            self.active_model = self.preferred_model
            self.initialized = True
            logger.info(f"✅ OpenAI client initialized with model: {self.active_model}")
            return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ Failed to initialize OpenAI client: {type(e).__name__}: {str(e)}")
            return False
    
    def _validate_api_key(self) -> bool:
        """Validate the API key format"""
        if not self.api_key:
            logger.warning("No API key found")
            return False
        if self.api_key == 'your_openai_api_key_here':
            logger.warning("Placeholder API key detected")
            return False
        
        api_key = self.api_key.strip()
        if len(api_key) < 20:  # Most keys are longer
            logger.warning(f"API key too short: {len(api_key)} characters")
            return False
            
        # Valid prefixes include both sk- and sk-proj- formats
        valid_prefixes = ['sk-', 'sk-proj-']
        if not any(api_key.startswith(prefix) for prefix in valid_prefixes):
            logger.warning(f"API key has unusual format. Expected to start with sk- or sk-proj-, got: {api_key[:10]}...")
            # Still return True as it might be a valid key with different format
            
        logger.info("API key validation passed")
        return True
    
    def is_ready(self) -> bool:
        """Check if the OpenAI client is initialized and ready"""
        return self.initialized and self.client is not None
        
    def test_connection(self) -> Tuple[bool, str, Optional[str]]:
        """Test the connection to OpenAI API with a simple request"""
        if not self.is_ready():
            return False, f"Client not initialized: {self.last_error}", None
            
        try:
            # Simple model list request to test connection
            start_time = time.time()
            response = self.client.models.list()
            duration = time.time() - start_time
            
            # Check if models were returned
            if not response.data:
                return False, "No models returned", None
                
            # Find if preferred model exists
            available_models = [model.id for model in response.data]
            preferred_model_available = self.preferred_model in available_models
            fallback_available = any(model in available_models for model in FALLBACK_MODELS)
            
            if preferred_model_available:
                return True, f"Connection successful! Preferred model '{self.preferred_model}' available", self.preferred_model
            elif fallback_available:
                # Find first available fallback model
                for model in FALLBACK_MODELS:
                    if model in available_models:
                        return True, f"Connection successful! Using fallback model '{model}'", model
            
            # No suitable models found
            return False, f"No suitable models available. Available models: {', '.join(available_models[:5])}...", None
            
        except Exception as e:
            self.last_error = str(e)
            return False, f"Connection test failed: {type(e).__name__}: {str(e)}", None
    
    def generate_completion(
        self, 
        prompt: str,
        system_message: str = "Você é um assistente jurídico brasileiro útil, preciso e conciso.",
        model: str = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        json_mode: bool = False
    ) -> Dict[Any, Any]:
        """
        Generate a completion using OpenAI API with comprehensive error handling
        and detailed response metrics
        """
        start_time = time.time()
        model = model or self.active_model or self.preferred_model
        
        # Initialize result structure
        result = {
            "success": False,
            "content": None,
            "error": None,
            "model": model,
            "metrics": {
                "tokens": {
                    "input": 0,
                    "output": 0,
                    "total": 0
                },
                "cost": 0.0,
                "duration_ms": 0,
                "finish_reason": None,
                "created_at": datetime.utcnow().isoformat(),
                "system_fingerprint": None
            }
        }
        
        # Check if client is ready
        if not self.is_ready():
            result["error"] = f"OpenAI client not initialized: {self.last_error}"
            return result
            
        try:
            # Prepare the chat completion request
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            
            # Make the API request
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"} if json_mode else None
            )
            
            # Process successful response
            result["success"] = True
            result["content"] = response.choices[0].message.content
            
            # Extract metrics
            if response.usage:
                result["metrics"]["tokens"]["input"] = response.usage.prompt_tokens
                result["metrics"]["tokens"]["output"] = response.usage.completion_tokens
                result["metrics"]["tokens"]["total"] = response.usage.total_tokens
                
                # Calculate cost
                model_config = MODEL_CONFIGS.get(model, MODEL_CONFIGS.get("gpt-4o-mini"))
                input_cost = (response.usage.prompt_tokens * model_config["input_cost_per_1k"]) / 1000
                output_cost = (response.usage.completion_tokens * model_config["output_cost_per_1k"]) / 1000
                result["metrics"]["cost"] = input_cost + output_cost
                
            # Extract additional metadata
            if hasattr(response.choices[0], "finish_reason"):
                result["metrics"]["finish_reason"] = response.choices[0].finish_reason
                
            if hasattr(response, "system_fingerprint"):
                result["metrics"]["system_fingerprint"] = response.system_fingerprint
                
            # Update usage stats
            self._update_usage_stats(result)
            
        except RateLimitError as e:
            result["error"] = f"Rate limit exceeded: {str(e)}"
            self.usage_stats["error_count"] += 1
            logger.error(f"❌ OpenAI rate limit error: {str(e)}")
            
        except APIConnectionError as e:
            result["error"] = f"Connection error: {str(e)}"
            self.usage_stats["error_count"] += 1
            logger.error(f"❌ OpenAI connection error: {str(e)}")
            
        except APIError as e:
            result["error"] = f"API error: {str(e)}"
            self.usage_stats["error_count"] += 1
            logger.error(f"❌ OpenAI API error: {str(e)}")
            
        except Exception as e:
            result["error"] = f"Error: {type(e).__name__}: {str(e)}"
            self.usage_stats["error_count"] += 1
            logger.error(f"❌ Unexpected error during OpenAI request: {str(e)}")
            
        finally:
            # Calculate duration
            result["metrics"]["duration_ms"] = int((time.time() - start_time) * 1000)
            
        return result
    
    def _update_usage_stats(self, result: Dict[Any, Any]) -> None:
        """Update internal usage statistics from a request result"""
        self.usage_stats["request_count"] += 1
        
        if result["success"]:
            self.usage_stats["total_tokens"] += result["metrics"]["tokens"]["total"]
            self.usage_stats["input_tokens"] += result["metrics"]["tokens"]["input"]
            self.usage_stats["output_tokens"] += result["metrics"]["tokens"]["output"]
            self.usage_stats["total_cost"] += result["metrics"]["cost"]
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get the current API usage statistics"""
        return {
            **self.usage_stats,
            "active_model": self.active_model,
            "preferred_model": self.preferred_model,
            "api_configured": self.is_ready(),
            "last_error": self.last_error,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def reset_usage_stats(self) -> None:
        """Reset the usage statistics"""
        self.usage_stats = {
            "total_tokens": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0,
            "request_count": 0,
            "error_count": 0
        }
        
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get a list of available models with their configurations"""
        if not self.is_ready():
            return []
        
        try:
            response = self.client.models.list()
            available_models = []
            
            for model in response.data:
                config = MODEL_CONFIGS.get(model.id, {
                    "input_cost_per_1k": 0.0,
                    "output_cost_per_1k": 0.0,
                    "supports_json_mode": False,
                    "max_tokens": 0,
                    "display_name": model.id
                })
                
                available_models.append({
                    "id": model.id,
                    "display_name": config.get("display_name", model.id),
                    "owned_by": model.owned_by,
                    "input_cost_per_1k": config.get("input_cost_per_1k", 0),
                    "output_cost_per_1k": config.get("output_cost_per_1k", 0),
                    "supports_json_mode": config.get("supports_json_mode", False),
                    "max_tokens": config.get("max_tokens", 0),
                    "is_preferred": model.id == self.preferred_model,
                    "is_active": model.id == self.active_model
                })
            
            return available_models
            
        except Exception as e:
            logger.error(f"❌ Failed to list models: {str(e)}")
            return []

# Singleton instance
openai_manager = OpenAIManager()

# Convenience functions
def is_openai_available() -> bool:
    """Check if OpenAI is available and ready"""
    return openai_manager.is_ready()

def get_completion(prompt: str, system_message: str = None, **kwargs) -> Dict[Any, Any]:
    """Generate a completion using the OpenAI manager"""
    return openai_manager.generate_completion(
        prompt=prompt,
        system_message=system_message or "Você é um assistente jurídico brasileiro útil, preciso e conciso.",
        **kwargs
    )

def get_openai_status() -> Dict[str, Any]:
    """Get the current status of the OpenAI client"""
    is_ready = openai_manager.is_ready()
    status = {
        "available": is_ready,
        "status": "available" if is_ready else "unavailable",
        "active_model": openai_manager.active_model,
        "preferred_model": openai_manager.preferred_model,
        "usage": openai_manager.get_usage_stats(),
        "last_error": openai_manager.last_error,
        "error": openai_manager.last_error if not is_ready else None,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if openai_manager.is_ready():
        test_success, test_message, _ = openai_manager.test_connection()
        status["connection_test"] = {
            "success": test_success,
            "message": test_message
        }
    
    return status

# API status endpoint handler (for app.py integration)
def handle_api_status_request():
    """Handle API status request for integration with Flask"""
    return {
        "openai": get_openai_status(),
        "models": openai_manager.get_available_models() if openai_manager.is_ready() else []
    }
