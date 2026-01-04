
from ghostshell.ui.icons import CHECK, WARNING

# === UI Messages ===
MSG_INIT_WELCOME = "[gs.bold_primary]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/gs.bold_primary]\n[gs.bold_primary]  GhostShell Setup[/gs.bold_primary]\n[gs.bold_primary]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/gs.bold_primary]"

MSG_ADD_WELCOME = "[gs.bold_primary]Add Memory Crystal[/gs.bold_primary]"

MSG_DISTILL_WELCOME = "[gs.bold_primary]Distilling Your Voice[/gs.bold_primary]"

MSG_CREATE_WELCOME = "[gs.bold_primary]Create New Post[/gs.bold_primary]"


MSG_INIT_COMPLETE = "[bold]Next Steps:[/bold]\n\n1. Run [gs.primary]ghostshell add[/gs.primary] to add your past posts\n2. Run [gs.primary]ghostshell create[/gs.primary] to start writing"

# === Error Messages ===
ERR_NOT_INITIALIZED = f"[gs.warning]{WARNING}  GhostShell not initialized[/gs.warning]"
ERR_RUN_INIT_FIRST = "[gs.muted]Run 'ghostshell init' first[/gs.muted]"

ERR_NO_CONTENT = f"[gs.warning]{WARNING}  No content provided[/gs.warning]"

ERR_NO_API_KEY = f"[gs.error]{WARNING}  GEMINI_API_KEY not found[/gs.error]"

ERR_NO_MEMORIES = f"[gs.warning]{WARNING}  No memories found[/gs.warning]"
ERR_ADD_POSTS_FIRST = "[gs.muted]Use 'ghostshell add' to add posts first[/gs.muted]"

ERR_NO_BLUEPRINT = f"[gs.warning]{WARNING}  Blueprint not found[/gs.warning]"
ERR_DISTILL_FIRST = "[gs.muted]Run 'ghostshell distill' to create a blueprint first[/gs.muted]"


ERR_PARSE_RESPONSE = f"[gs.error]{WARNING}  Could not parse API response[/gs.error]"

ERR_DISTILL_FAILED = f"[gs.error]{WARNING}  Distillation failed: {{error}}[/gs.error]"

ERR_ALREADY_INITIALIZED = f"[gs.warning]{WARNING}  GhostShell is already initialized at:[/gs.warning]"
ERR_EMPTY_API_KEY = f"[gs.bold_error]{WARNING}  API key cannot be empty[/gs.bold_error]"
ERR_PERMISSION_DENIED = f"[gs.bold_error]{WARNING}  Permission denied:[/gs.bold_error]"
ERR_SETUP_FAILED = f"[gs.bold_error]{WARNING}  Setup failed:[/gs.bold_error]"

ERR_COULD_NOT_LOAD_FILE = f"[gs.warning]Warning: Could not load {{filename}}: {{error}}[/gs.warning]"

ERR_COULD_NOT_LOAD_BLUEPRINT = f"[gs.warning]Warning: Could not load blueprint: {{error}}[/gs.warning]"

# === success Messages ===
MSG_FILE_SAVED = f"[gs.success]{CHECK}[/gs.success] Saved to: [gs.primary]{{filepath}}[/gs.primary]"

# === Info Messages ===
INFO_BRAINSTORMING = "[gs.primary]Brainstorming ideas...[/gs.primary]"
INFO_GENERATING = "[gs.primary]Generating post...[/gs.primary]"

# === API Key Help ===
API_KEY_HELP = "[gs.muted]Get your key at: https://makersuite.google.com/app/apikey[/gs.muted]"

# === Command Help Text ===
HELP_INIT = """[gs.bold_primary]Initialize GhostShell[/gs.bold_primary]

[bold]Usage:[/bold] [gs.primary]ghostshell init[/gs.primary]

Creates the necessary directory structure and saves your Gemini API key.
This command only needs to be run once.

[bold]Required: Gemini API Key[/bold]
  Get your free API key at: [u]https://makersuite.google.com/app/apikey[/u]

[bold]Creates:[/bold]
  • [gs.primary]ghostshell-data/memories/[/gs.primary]    (store past posts)
  • [gs.primary]ghostshell-data/.env[/gs.primary]         (API key configuration)
  • [gs.primary]ghostshell-data/blueprint.yaml[/gs.primary] (created by 'distill')
"""

HELP_ADD = """[gs.bold_primary]Add Existing Posts[/gs.bold_primary]

[bold]Usage:[/bold] [gs.primary]ghostshell add[/gs.primary]

Add past LinkedIn posts to your memory bank. These posts help train your
personal voice model for content generation.

[bold]Workflow:[/bold]
  1. Paste your post content [gs.muted](Ctrl+D when done)[/gs.muted]
  2. Post is saved to [gs.primary]memories/[/gs.primary] directory
"""

HELP_DISTILL = """[gs.bold_primary]Analyze Your Voice[/gs.bold_primary]

[bold]Usage:[/bold] [gs.primary]ghostshell distill[/gs.primary]

Analyzes all your saved posts using Gemini AI to extract your unique voice,
writing style, typical structure, niche, and anti-patterns.

[bold]Prerequisites:[/bold]
  • At least 1 post added with [gs.primary]ghostshell add[/gs.primary]

[bold]What happens:[/bold]
  1. Loads all posts from [gs.primary]memories/[/gs.primary]
  2. Sends them to Gemini for analysis
  3. Extracts: voice, structure, niche, anti-patterns
  4. Saves blueprint to [gs.primary]ghostshell-data/blueprint.yaml[/gs.primary]
"""

HELP_CREATE = """[gs.bold_primary]Create New Posts[/gs.bold_primary]

[bold]Usage:[/bold] [gs.primary]ghostshell create[/gs.primary]

Generate new posts matching your voice and style using Gemini AI.

[bold]Prerequisites:[/bold]
  • Run [gs.primary]ghostshell distill[/gs.primary] first to create blueprint

[bold]Workflow:[/bold]
  1. Brainstorm ideas based on your voice
  2. Select an idea or enter custom topic
  3. Generate initial draft post
  4. [bold]Edit Loop:[/bold] accept / edit / regenerate / discard
  5. Save to [gs.primary]memories/[/gs.primary] directory [gs.muted](ready for posting)[/gs.muted]
"""


HELP_GENERAL = """[gs.bold_primary]GhostShell - Digital Twin for LinkedIn[/gs.bold_primary]

[bold]Quick Start:[/bold]
  1. [gs.primary]ghostshell init[/gs.primary]        Initialize with your Key
  2. [gs.primary]ghostshell add[/gs.primary]         Add past posts
  3. [gs.primary]ghostshell distill[/gs.primary]     Analyze your voice
  4. [gs.primary]ghostshell create[/gs.primary]      Generate new posts

[bold]Get Your Key:[/bold] [u]https://makersuite.google.com/app/apikey[/u]
"""
