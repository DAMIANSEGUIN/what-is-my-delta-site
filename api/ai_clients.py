"""
AI clients for Mosaic 2.0 fallback system.
Provides OpenAI and Anthropic clients with rate limiting and error handling.
"""

import os
import time
import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
# import openai
# from anthropic import Anthropic

from .settings import get_settings

class AIClientManager:
    """Manages AI clients with rate limiting and fallback logic."""
    
    def __init__(self):
        self.settings = get_settings()
        self.openai_client = None
        self.anthropic_client = None
        self.rate_limits = {
            "openai": {"requests": 0, "last_reset": datetime.now()},
            "anthropic": {"requests": 0, "last_reset": datetime.now()}
        }
        self.max_requests_per_minute = 60
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI clients with API keys."""
        # Temporarily disabled for testing
        self.openai_client = None
        self.anthropic_client = None
        print("⚠️ AI clients temporarily disabled for testing")
    
    def _check_rate_limit(self, provider: str) -> bool:
        """Check if we're within rate limits for a provider."""
        now = datetime.now()
        rate_data = self.rate_limits[provider]
        
        # Reset counter if more than a minute has passed
        if (now - rate_data["last_reset"]).seconds >= 60:
            rate_data["requests"] = 0
            rate_data["last_reset"] = now
        
        return rate_data["requests"] < self.max_requests_per_minute
    
    def _increment_rate_limit(self, provider: str):
        """Increment rate limit counter for a provider."""
        self.rate_limits[provider]["requests"] += 1
    
    def generate_fallback_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate AI fallback response using available clients."""
        start_time = time.time()
        
        # Try OpenAI first
        if self.openai_client and self._check_rate_limit("openai"):
            try:
                response = self._call_openai(prompt, context)
                if response:
                    self._increment_rate_limit("openai")
                    return {
                        "response": response,
                        "provider": "openai",
                        "fallback_used": True,
                        "response_time_ms": int((time.time() - start_time) * 1000)
                    }
            except Exception as e:
                print(f"⚠️ OpenAI fallback failed: {e}")
        
        # Try Anthropic as fallback
        if self.anthropic_client and self._check_rate_limit("anthropic"):
            try:
                response = self._call_anthropic(prompt, context)
                if response:
                    self._increment_rate_limit("anthropic")
                    return {
                        "response": response,
                        "provider": "anthropic",
                        "fallback_used": True,
                        "response_time_ms": int((time.time() - start_time) * 1000)
                    }
            except Exception as e:
                print(f"⚠️ Anthropic fallback failed: {e}")
        
        # If all AI clients fail, return error
        return {
            "response": "AI fallback unavailable - all providers failed",
            "provider": "none",
            "fallback_used": False,
            "error": "All AI providers unavailable",
            "response_time_ms": int((time.time() - start_time) * 1000)
        }
    
    def _call_openai(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Call OpenAI API with proper error handling."""
        try:
            messages = [
                {"role": "system", "content": "You are a helpful career coach assistant. Provide thoughtful, actionable advice."}
            ]
            
            if context:
                context_str = json.dumps(context, indent=2)
                messages.append({"role": "user", "content": f"Context: {context_str}\n\nUser prompt: {prompt}"})
            else:
                messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def _call_anthropic(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Call Anthropic API with proper error handling."""
        try:
            system_prompt = "You are a helpful career coach assistant. Provide thoughtful, actionable advice."
            
            if context:
                context_str = json.dumps(context, indent=2)
                full_prompt = f"Context: {context_str}\n\nUser prompt: {prompt}"
            else:
                full_prompt = prompt
            
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all AI clients."""
        status = {
            "openai": {
                "available": self.openai_client is not None,
                "rate_limited": not self._check_rate_limit("openai"),
                "requests_this_minute": self.rate_limits["openai"]["requests"]
            },
            "anthropic": {
                "available": self.anthropic_client is not None,
                "rate_limited": not self._check_rate_limit("anthropic"),
                "requests_this_minute": self.rate_limits["anthropic"]["requests"]
            }
        }
        
        status["any_available"] = any([
            status["openai"]["available"] and not status["openai"]["rate_limited"],
            status["anthropic"]["available"] and not status["anthropic"]["rate_limited"]
        ])
        
        return status

# Global AI client manager instance
ai_client_manager = AIClientManager()

def get_ai_fallback_response(prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get AI fallback response using the global client manager."""
    return ai_client_manager.generate_fallback_response(prompt, context)

def get_ai_health_status() -> Dict[str, Any]:
    """Get AI clients health status."""
    return ai_client_manager.get_health_status()
