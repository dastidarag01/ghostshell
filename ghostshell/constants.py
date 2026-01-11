
from enum import Enum

class LLMProvider(str, Enum):
    GEMINI = "gemini"

# Project Constants
PROJECT_NAME = "GhostShell"
VERSION = "0.1.0"

# Defaults
DEFAULT_DATA_DIR = "./ghostshell-data"
DEFAULT_MEMORIES_SUBDIR = "memories"
DEFAULT_BLUEPRINT_FILENAME = "blueprint.yaml"
DEFAULT_ENV_FILENAME = ".env"
