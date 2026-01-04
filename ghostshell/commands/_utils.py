
import typer

from ghostshell.logger import Logger
from ghostshell.utils import get_data_dir, load_env, get_gemini_api_key
from ghostshell.services.gemini import GeminiClient
from ghostshell.prompts import ERR_NOT_INITIALIZED, ERR_RUN_INIT_FIRST, ERR_NO_API_KEY


def require_init() -> None:
    if not get_data_dir().exists():
        Logger.warning(ERR_NOT_INITIALIZED)
        Logger.dim(ERR_RUN_INIT_FIRST + "\n")
        raise typer.Exit(1)


def require_api_key() -> str:
    load_env()
    api_key = get_gemini_api_key()
    if not api_key:
        Logger.error(ERR_NO_API_KEY + "\n")
        raise typer.Exit(1)
    return api_key


def create_gemini_client(api_key: str) -> GeminiClient:
    try:
        return GeminiClient(api_key)
    except Exception as e:
        Logger.error(f"{str(e)}\n")
        raise typer.Exit(1)


