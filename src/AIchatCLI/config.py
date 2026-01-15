import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

# Supported providers
PROVIDERS = Literal["groq", "openai", "anthropic", "ollama"]

def get_provider() -> PROVIDERS:
    """Get AI provider from env, default: groq (fastest/free)."""
    return os.getenv("CHAT_PROVIDER", "groq")

def get_api_key(provider: str) -> str:
    """Get API key for specific provider."""
    key_map = {
        "groq": "GROQ_API_KEY",
        "openai": "OPENAI_API_KEY", 
        "anthropic": "ANTHROPIC_API_KEY",
        "ollama": None  # Local, no key needed
    }
    
    key_var = key_map.get(provider)
    if not key_var:
        raise ValueError(f"{provider.upper()} doesn't need API key (local model)")
    
    key = os.getenv(key_var)
    if not key:
        raise ValueError(
            f"{provider.upper()}_API_KEY not set!\n"
            f"1. Copy .env.example to .env\n"
            f"2. Set {provider.upper()}_API_KEY\n"
            f"3. Or run: export CHAT_PROVIDER={provider}"
        )
    return key

def get_model(provider: str) -> str:
    """Get optimal model for each provider."""
    models = {
        "groq": os.getenv("GROQ_MODEL", "llama3-8b-8192"),      # Fastest free
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),     # Cheapest GPT
        "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
        "ollama": os.getenv("OLLAMA_MODEL", "llama3.1")         # Local
    }
    return models[provider]
