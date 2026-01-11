
from datetime import datetime
import typer

from ghostshell.logger import Logger
from ghostshell.models import Blueprint
from ghostshell.services import memory, blueprint
from ghostshell.prompts import (
    MSG_DISTILL_WELCOME,
    ERR_NO_MEMORIES, ERR_ADD_POSTS_FIRST,
)
from ghostshell.commands._utils import require_init, create_llm_client
from ghostshell.ui import render_completion_animation


def distill_command() -> None:
    Logger.title(MSG_DISTILL_WELCOME)

    require_init()

    # Load memories
    memories = memory.load_all()
    if not memories:
        Logger.warning(ERR_NO_MEMORIES)
        Logger.dim(ERR_ADD_POSTS_FIRST + "\n")
        raise typer.Exit(1)

    with Logger.status("[gs.magic]Distilling your voice...[/gs.magic]"):
        posts_summary = memory.get_summary(memories)
        
        # Calling API
        client = create_llm_client()
        analysis = client.analyze_voice(posts_summary, len(memories))
        
        # Create technical topics list for deduplication
        all_topics = sorted({mem.topic for mem in memories if mem.topic})
        
        # Create flattened Blueprint from analysis
        bp = Blueprint(
            voice=analysis.get('voice', ''),
            core_philosophy=analysis.get('core_philosophy', ''),
            target_audience=analysis.get('target_audience', ''),
            niche=analysis.get('niche', ''),
            intellectual_positioning=analysis.get('intellectual_positioning', ''),
            topic_flavour=analysis.get('topic_flavour', ''),
            linguistic_markers=analysis.get('linguistic_markers', ''),
            stylistic_fingerprint=analysis.get('stylistic_fingerprint', ''),
            opening_hook_psychology=analysis.get('opening_hook_psychology', ''),
            narrative_architecture=analysis.get('narrative_architecture', ''),
            pacing_and_density=analysis.get('pacing_and_density', ''),
            anti_patterns=analysis.get('anti_patterns', ''),
            existing_topics=all_topics,
            last_distilled=datetime.now()
        )
        
        blueprint.save(bp)
        
        # Completion feedback
        render_completion_animation("Voice Distillation Successful")
        blueprint.display(bp)
