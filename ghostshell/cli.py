
import typer
from typing import Optional

from ghostshell.logger import Logger

app = typer.Typer(
    help="GhostShell - A Digital Twin content engine for LinkedIn creators",
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        # Lazy import to avoid circular dependency
        from ghostshell.ui import get_startup_banner, render_markdown

        # Display ASCII logo + version
        Logger.banner(get_startup_banner())
        
        from ghostshell.prompts import HELP_GENERAL
        render_markdown(HELP_GENERAL)
        
        Logger.newline()
        Logger.info("Run [gs.primary]ghostshell init[/gs.primary] to get started\n")


@app.command()
def init():
    from ghostshell.commands.init import init_command
    init_command()


@app.command()
def add():
    from ghostshell.commands.add import add_command
    add_command()


@app.command()
def distill():
    from ghostshell.commands.distill import distill_command
    distill_command()


@app.command()
def create():
    from ghostshell.commands.create import create_command
    create_command()




@app.command()
def help(topic: str = typer.Argument("", help="Topic to get help on")):
    from ghostshell.prompts import (
        HELP_GENERAL, HELP_INIT, HELP_ADD, HELP_DISTILL,
        HELP_CREATE
    )
    from ghostshell.ui import render_markdown

    topic = topic.lower() if topic else ""

    help_map = {
        "init": HELP_INIT,
        "add": HELP_ADD,
        "distill": HELP_DISTILL,
        "create": HELP_CREATE
    }

    if not topic:
        render_markdown(HELP_GENERAL, title="GhostShell Help")
    elif topic in help_map:
        render_markdown(help_map[topic], title=f"Help: {topic.capitalize()}")
    else:
        Logger.warning(f"No help available for '{topic}'.\n")
        Logger.info("Available topics: init, add, distill, create\n")


# === Command Aliases (hidden from help) ===
@app.command(name="a", hidden=True)
def add_alias():
    from ghostshell.commands.add import add_command
    add_command()


@app.command(name="c", hidden=True)
def create_alias():
    from ghostshell.commands.create import create_command
    create_command()


@app.command(name="d", hidden=True)
def distill_alias():
    from ghostshell.commands.distill import distill_command
    distill_command()




if __name__ == "__main__":
    app()
