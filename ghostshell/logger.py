from contextlib import contextmanager
from rich.console import Console

from ghostshell.ui.theme import GS_THEME
from ghostshell.ui.icons import CHECK, WARNING

# Initialize global console with the GhostShell theme
_console = Console(theme=GS_THEME)


def get_console() -> Console:
    return _console




class Logger:

    @staticmethod
    def info(message: str) -> None:
        _console.print(message)

    @staticmethod
    def success(message: str) -> None:
        _console.print(f"[gs.success]{CHECK}[/gs.success] {message}")

    @staticmethod
    def error(message: str) -> None:
        _console.print(f"[gs.error]{WARNING} {message}[/gs.error]")

    @staticmethod
    def warning(message: str) -> None:
        _console.print(f"[gs.warning]{message}[/gs.warning]")

    @staticmethod
    def dim(message: str) -> None:
        _console.print(f"[gs.muted]{message}[/gs.muted]")

    @staticmethod
    def bold(message: str) -> None:
        _console.print(f"[bold]{message}[/bold]")

    @staticmethod
    def title(message: str) -> None:
        _console.print(f"\n{message}\n")

    @staticmethod
    def section_title(message: str) -> None:
        rule = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        _console.print(f"[gs.primary]{rule}[/gs.primary]")
        _console.print(f"[gs.bold_primary]  {message}[/gs.bold_primary]")
        _console.print(f"[gs.primary]{rule}[/gs.primary]\n")

    @staticmethod
    @contextmanager
    def status(message: str):
        try:
            with _console.status(message) as s:
                yield s
        except Exception as e:
            # If already in a live display (like a Progress bar), 
            # console.status() raises an error. Catch it and just yield.
            if "live display" in str(e).lower():
                yield None
            else:
                raise

    @staticmethod
    def print_panel(content: str, title: str = "", border_style: str = "gs.primary") -> None:
        from rich.panel import Panel
        panel = Panel.fit(content, border_style=border_style, title=title)
        _console.print(panel)

    @staticmethod
    def newline() -> None:
        _console.print()

    @staticmethod
    def banner(content: str) -> None:
        _console.print(content)
