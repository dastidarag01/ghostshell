
import math
import time
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.box import ROUNDED

from ghostshell.ui.icons import IDEA, TARGET, SPARKLES, TROPHY, FIRE, EYES, CHAT, BOOKMARK, CHECK
from ghostshell.ui.theme import GS_THEME


def render_idea_card(number: int, topic: str, hook_summary: str, angle: Optional[str] = None) -> Panel:
    content = f"[gs.primary][bold]{topic}[/bold][/gs.primary]\n"
    content += f"[gs.muted]{hook_summary}[/gs.muted]"

    if angle:
        content += f"\n[gs.info]→ {angle}[/gs.info]"

    title = f"{IDEA} Idea {number}"
    panel = Panel(
        content,
        title=f"[gs.bold_primary]{title}[/gs.bold_primary]",
        title_align="left",
        border_style="gs.primary",
        box=ROUNDED,
        padding=(1, 2)
    )

    return panel


def render_idea_cards(ideas: List[Dict[str, str]]) -> None:
    from ghostshell.logger import get_console
    console = get_console()

    for i, idea in enumerate(ideas):
        card = render_idea_card(
            number=i + 1,
            topic=idea.get('topic', 'Untitled'),
            hook_summary=idea.get('hook_summary', ''),
            angle=idea.get('angle')
        )
        console.print(card)
        if i < len(ideas) - 1:  # Add spacing between cards
            console.print()






def create_panel_section(title: str, content: Any, icon: str = "", border_style: str = "gs.primary") -> Panel:
    panel_title = f"{icon} {title}" if icon else title

    panel = Panel(
        content,
        title=f"[gs.bold_primary]{panel_title}[/gs.bold_primary]",
        title_align="left",
        border_style=border_style,
        box=ROUNDED,
        padding=(1, 2)
    )

    return panel


def render_markdown(content: str, title: Optional[str] = None) -> None:
    from ghostshell.logger import get_console
    from rich.text import Text
    console = get_console()
    # Use Text.from_markup if we detect our theme markup or bold tags
    if "[gs." in content or "[bold]" in content:
        try:
            renderable = Text.from_markup(content)
        except Exception:
            renderable = content
    else:
        renderable = Markdown(content)
    
    if title:
        console.print(create_panel_section(title, renderable))
    else:
        console.print(renderable)


def render_completion_animation(message: str = "Operation Complete!") -> None:
    from ghostshell.logger import get_console
    console = get_console()
    console.print()
    
    icons = [SPARKLES, FIRE, TROPHY, CHECK]
    for icon in icons:
        console.print(f"[gs.magic]{icon}[/gs.magic]", end=" ")
        time.sleep(0.3)
    
    console.print(f"\n[gs.bold_primary]{message}[/gs.bold_primary]\n")


def render_post_preview(content: str, title: str = "Post Preview") -> None:
    from ghostshell.logger import get_console
    console = get_console()
    
    # Calculate metadata
    words = len(content.split())
    chars = len(content)
    # Average reading speed: 200 wpm
    read_time_secs = math.ceil(words / 200 * 60)
    
    metadata = f"[gs.muted]{words} words | {chars} chars | ~{read_time_secs}s read[/gs.muted]"
    
    # Create panel with standard branding
    panel = Panel(
        f"{content}\n\n{metadata}",
        title=f"[gs.bold_primary]{title}[/gs.bold_primary]",
        title_align="left",
        border_style="gs.magic",
        box=ROUNDED,
        padding=(1, 2)
    )
    
    console.print(panel)


