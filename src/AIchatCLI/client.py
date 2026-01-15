from typing import List, Dict, Any
import os

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .config import get_provider, get_api_key, get_model

class ChatClient:
    """Universal AI client - works with Groq, OpenAI, Anthropic, Ollama."""
    
    def __init__(self):
        self.provider = get_provider()
        self.model = get_model(self.provider)
        self._client = self._init_client()
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
    
    def _init_client(self):
        """Initialize client for selected provider."""
        if self.provider == "groq":
            if not GROQ_AVAILABLE:
                raise ImportError("Install Groq: pip install groq")
            return Groq(api_key=get_api_key("groq"))
        
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("Install OpenAI: pip install openai")
            return OpenAI(api_key=get_api_key("openai"))
        
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("Install Anthropic: pip install anthropic")
            return Anthropic(api_key=get_api_key("anthropic"))
        
        elif self.provider == "ollama":
            return None  # Local Ollama handled separately
        
        raise ValueError(f"Unsupported provider: {self.provider}")
    
    def send(self, content: str) -> str:
        """Send message to selected AI provider."""
        self.messages.append({"role": "user", "content": content})
        
        if self.provider == "groq":
            return self._groq_send()
        elif self.provider == "openai":
            return self._openai_send()
        elif self.provider == "anthropic":
            return self._anthropic_send()
        elif self.provider == "ollama":
            return self._ollama_send()
        
        raise ValueError(f"Provider {self.provider} not implemented")
    
    def _groq_send(self) -> str:
        """Groq-specific API call."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
            max_tokens=2000
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
    def _openai_send(self) -> str:
        """OpenAI-compatible API call."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
            max_tokens=2000
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
    def _anthropic_send(self) -> str:
        """Anthropic API call."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": m["role"], "content": m["content"]} for m in self.messages]
        )
        reply = response.content[0].text
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
    def _ollama_send(self) -> str:
        """Local Ollama API call."""
        import requests
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": self.model,
            "messages": self.messages,
            "stream": False
        })
        reply = response.json()["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
    def clear_history(self):
        """Reset conversation."""
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
