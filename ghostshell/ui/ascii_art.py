
from pathlib import Path

# ASCII logo art (plain text, no color markup)
# Using backslash after opening quotes to prevent leading newline
LOGO_ART = """\
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗███████╗██╗  ██╗███████╗██╗     ██╗
 ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██║     ██║
 ██║  ███╗███████║██║   ██║███████╗   ██║   ███████╗███████║█████╗  ██║     ██║
 ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ╚════██║██╔══██║██╔══╝  ██║     ██║
 ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ███████║██║  ██║███████╗███████╗███████╗
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝"""

TAGLINE = "Digital Twin for LinkedIn Creators"


def get_version() -> str:
    try:
        # Python 3.11+ has tomllib built-in
        import tomllib
    except ImportError:
        # Fallback for Python 3.9-3.10
        try:
            import tomli as tomllib
        except ImportError:
            return "unknown"

    try:
        # Navigate from current file to repo root to pyproject.toml
        repo_root = Path(__file__).parent.parent.parent
        pyproject_path = repo_root / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        version = data.get("tool", {}).get("poetry", {}).get("version", "unknown")
        return version
    except Exception:
        # If anything fails, return unknown (version is cosmetic)
        return "unknown"


def get_startup_banner() -> str:
    version = get_version()

    # Split logo into lines and apply gradient colors
    lines = LOGO_ART.split('\n')
    gradient_colors = [
        'cyan',
        'bright_cyan',
        'blue',
        'magenta',
        'bright_magenta',
        'magenta',
    ]

    colored_lines = []
    for i, line in enumerate(lines):
        # Use corresponding gradient color, fall back to last color if needed
        color = gradient_colors[i] if i < len(gradient_colors) else gradient_colors[-1]
        colored_lines.append(f"[{color}]{line}[/{color}]")

    logo_with_gradient = '\n'.join(colored_lines)

    # Combine logo, tagline, and version
    return f"{logo_with_gradient}\n\n[dim]{TAGLINE}[/dim]\n[dim]v{version}[/dim]\n"
