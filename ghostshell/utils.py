import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from ghostshell.constants import LLMProvider, DEFAULT_DATA_DIR


def get_data_dir() -> Path:
    data_dir = os.getenv("GHOSTSHELL_DATA_DIR", DEFAULT_DATA_DIR)
    return Path(data_dir).resolve()


def get_memories_dir() -> Path:
    return get_data_dir() / "memories"


def get_blueprint_path() -> Path:
    return get_data_dir() / "blueprint.yaml"


def load_env() -> None:
    env_path = get_data_dir() / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def get_gemini_api_key() -> Optional[str]:
    load_env()
    return os.getenv("GEMINI_API_KEY")


def get_llm_provider() -> LLMProvider:
    load_env()
    provider_val = os.getenv("GHOSTSHELL_LLM_PROVIDER", LLMProvider.GEMINI.value).lower()
    try:
        return LLMProvider(provider_val)
    except ValueError:
        return LLMProvider.GEMINI


def get_api_key(provider: LLMProvider) -> Optional[str]:
    load_env()
    if provider == LLMProvider.GEMINI:
        return os.getenv("GEMINI_API_KEY")
    return None