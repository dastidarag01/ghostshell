import typer
from google import genai

from ghostshell.logger import Logger
from ghostshell.utils import get_data_dir, get_llm_provider, get_api_key
from ghostshell.services.llm import LLMService
from ghostshell.constants import LLMProvider
from ghostshell.prompts import ERR_NOT_INITIALIZED, ERR_RUN_INIT_FIRST, ERR_NO_API_KEY


def require_init() -> None:
    if not get_data_dir().exists():
        Logger.warning(ERR_NOT_INITIALIZED)
        Logger.dim(ERR_RUN_INIT_FIRST + "\n")
        raise typer.Exit(1)


def require_api_key() -> str:
    provider = get_llm_provider()
    api_key = get_api_key(provider)
    if not api_key:
        Logger.error(ERR_NO_API_KEY + "\n")
        raise typer.Exit(1)
    return api_key


def create_llm_client() -> LLMService:
    provider = get_llm_provider()
    api_key = require_api_key()
    
    try:
        if provider == LLMProvider.GEMINI:
            client = genai.Client(api_key=api_key)
            return LLMService(client, provider)
        else:
            Logger.error(f"Unsupported LLM provider: {provider}\n")
            raise typer.Exit(1)
    except Exception as e:
        Logger.error(f"{str(e)}\n")
        raise typer.Exit(1)


