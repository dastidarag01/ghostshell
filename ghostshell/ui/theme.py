
from rich.theme import Theme

# Semantic color palette
COLORS = {
    "primary": "cyan",              # Main accent
    "success": "green",             # Success states
    "error": "bright_red",          # Errors and alerts
    "warning": "yellow",            # Warnings
    "info": "bright_blue",          # Information
    "muted": "dim white",           # Less important text
    "highlight": "bright_cyan",     # Special highlights
    "magic": "bright_magenta",      # AI operations
}

# Native Rich Theme definition
# Using 'gs.' prefix to avoid collisions with standard Rich styles
GS_THEME = Theme({
    "gs.primary": COLORS["primary"],
    "gs.success": COLORS["success"],
    "gs.error": COLORS["error"],
    "gs.warning": COLORS["warning"],
    "gs.info": COLORS["info"],
    "gs.muted": COLORS["muted"],
    "gs.highlight": COLORS["highlight"],
    "gs.magic": COLORS["magic"],
    
    # Combined styles
    "gs.bold_primary": f"bold {COLORS['primary']}",
    "gs.bold_success": f"bold {COLORS['success']}",
    "gs.bold_error": f"bold {COLORS['error']}",
})
