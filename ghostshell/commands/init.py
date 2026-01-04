
from pathlib import Path
from datetime import datetime

import typer
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from ghostshell.logger import Logger
from ghostshell.prompts import (
    MSG_INIT_WELCOME, MSG_INIT_COMPLETE,
    ERR_ALREADY_INITIALIZED, ERR_EMPTY_API_KEY, ERR_PERMISSION_DENIED,
    ERR_SETUP_FAILED, API_KEY_HELP
)


def _get_sample_memory() -> str:
    return """---
topic: "Leadership and Focus"
---

The best advice I ever got about productivity:

Stop optimizing your morning routine.

I spent years tweaking my wake-up time, testing different apps, trying every productivity hack.

Then I realized: I was procrastinating on the actual work.

The real productivity hack?

Just start.

Your morning routine doesn't need to be perfect. It needs to get you to your desk.

Everything else is just noise.
"""


def init_command() -> None:
    Logger.section_title("GhostShell Setup")

    # Get data directory
    data_dir_input = Prompt.ask(
        "Where should we store your content?",
        default="./ghostshell-data"
    )
    data_dir = Path(data_dir_input).resolve()

    # Check if already initialized
    env_path = data_dir / ".env"
    if env_path.exists():
        Logger.warning(f"{ERR_ALREADY_INITIALIZED} {data_dir}")
        overwrite = Confirm.ask("Overwrite existing configuration?", default=False)
        if not overwrite:
            Logger.dim("Setup cancelled.\n")
            raise typer.Exit(0)
        Logger.newline()

    # Get API key
    api_key = Prompt.ask("Gemini API Key", password=True)

    # Validate API key
    if not api_key or not api_key.strip():
        Logger.error(ERR_EMPTY_API_KEY)
        Logger.dim(API_KEY_HELP + "\n")
        raise typer.Exit(1)

    # Create directory structure
    try:
        memories_dir = data_dir / "memories"

        memories_dir.mkdir(parents=True, exist_ok=True)

        # Write .env file
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"GEMINI_API_KEY={api_key.strip()}\n")
            f.write(f"GHOSTSHELL_DATA_DIR={data_dir}\n")

        # Create sample memory
        sample_content = _get_sample_memory()
        sample_filename = f"{datetime.now().strftime('%Y-%m-%d')}-sample-post.md"
        sample_path = memories_dir / sample_filename

        with open(sample_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        # Success output
        Logger.newline()
        Logger.success("Created directory:")
        Logger.info(f"  • {memories_dir}")
        Logger.newline()
        Logger.success("Saved configuration:")
        Logger.info(f"  • {env_path}")
        Logger.newline()
        Logger.success("Created sample memory:")
        Logger.info(f"  • {sample_path}")
        Logger.newline()

        Logger.print_panel(
            MSG_INIT_COMPLETE,
            title="🎉 Setup Complete!",
            border_style="green"
        )
        Logger.newline()

    except PermissionError as e:
        Logger.error(f"{ERR_PERMISSION_DENIED} Cannot write to {data_dir}")
        raise typer.Exit(1)
    except Exception as e:
        Logger.error(f"{ERR_SETUP_FAILED} {str(e)}")
        raise typer.Exit(1)
