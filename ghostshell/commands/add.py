
import typer
from rich.panel import Panel

from ghostshell.logger import Logger, get_console
from ghostshell.models import Memory
from ghostshell.services import memory
from ghostshell.prompts import MSG_ADD_WELCOME, MSG_FILE_SAVED
from ghostshell.commands._utils import require_init, create_llm_client, read_multiline_input


def add_command() -> None:
    Logger.title(MSG_ADD_WELCOME)

    require_init()
    
    Logger.newline()
    instructions = Panel(
        "Paste your LinkedIn post content.\n[dim]Press Ctrl+D when done.[/dim]",
        title="[gs.bold_primary]Add Memory Crystal[/gs.bold_primary]",
        border_style="gs.primary",
        padding=(0,1)
    )
    get_console().print(instructions)

    user_input = read_multiline_input()
    if not user_input:
        Logger.warning("No input provided\n")
        raise typer.Exit(1)

    client = create_llm_client()

    parsed = client.parse_add_memory(user_input)

    mem = Memory(
        content=parsed.get('content', ''),
        topic=parsed.get('topic', '')
    )

    filepath = memory.save(mem)
    Logger.success(MSG_FILE_SAVED.format(filepath=filepath) + "\n")
