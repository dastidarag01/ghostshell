import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


def get_data_dir() -> Path:
    data_dir = os.getenv("GHOSTSHELL_DATA_DIR", "./ghostshell-data")
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