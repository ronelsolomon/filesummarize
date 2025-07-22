"""Utility functions for interacting with language models."""
import json
import logging
from typing import Any, Dict, List, Optional, Union

from ollama import Client
from pydantic import BaseModel

from ..config import settings

logger = logging.getLogger(__name__)


class LLMResponse(BaseModel):
    """Structured response from LLM."""
    content: str
    model: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.dict()
    
    @classmethod
    def from_ollama_response(cls, response: Dict[str, Any]) -> "LLMResponse":
        """Create from Ollama response."""
        return cls(
            content=response.get("message", {}).get("content", ""),
            model=response.get("model", ""),
            prompt_tokens=response.get("prompt_eval_count"),
            completion_tokens=response.get("eval_count"),
            total_tokens=(response.get("prompt_eval_count", 0) + 
                         response.get("eval_count", 0))
        )


class LLMClient:
    """Client for interacting with language models."""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        """Initialize the LLM client.
        
        Args:
            base_url: Base URL of the Ollama server
            model: Default model to use
        """
        self.base_url = base_url or str(settings.OLLAMA_HOST)
        self.default_model = model or settings.OLLAMA_MODEL
        self.client = Client(host=self.base_url)
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        format: str = "json",
        **kwargs
    ) -> LLMResponse:
        """Generate text from a prompt.
        
        Args:
            prompt: The prompt to send to the model
            model: Model to use (defaults to the instance default)
            system_prompt: System prompt to set the behavior of the assistant
            format: Format of the response ('json' or 'text')
            **kwargs: Additional arguments to pass to the Ollama API
            
        Returns:
            LLMResponse object with the generated content and metadata
        """
        model = model or self.default_model
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat(
                model=model,
                messages=messages,
                stream=False,
                format=format,
                **kwargs
            )
            return LLMResponse.from_ollama_response(response)
        except Exception as e:
            logger.error(f"Error generating text with model {model}: {e}")
            raise
    
    def generate_json(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate and parse JSON response from the model.
        
        Args:
            prompt: The prompt to send to the model
            model: Model to use (defaults to the instance default)
            system_prompt: System prompt to set the behavior of the assistant
            **kwargs: Additional arguments to pass to the Ollama API
            
        Returns:
            Parsed JSON response as a dictionary
            
        Raises:
            json.JSONDecodeError: If the response is not valid JSON
        """
        response = self.generate(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            format="json",
            **kwargs
        )
        return json.loads(response.content)


def get_llm_client() -> LLMClient:
    """Get a configured LLM client."""
    return LLMClient()
