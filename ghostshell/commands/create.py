
from typing import List

import typer
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.panel import Panel

from ghostshell.logger import Logger, get_console
from ghostshell.models import SuggestedIdea, Memory
from ghostshell.services.llm import LLMService
from ghostshell.services import blueprint, memory
from ghostshell.prompts import MSG_CREATE_WELCOME
from ghostshell.commands._utils import require_init, create_llm_client
from ghostshell.ui import render_idea_cards, render_post_preview, render_completion_animation, SPARKLES, CHECK, CHAT, CROSS


def create_command() -> None:
    Logger.title(MSG_CREATE_WELCOME)

    require_init()
    bp = blueprint.load()

    client = create_llm_client()
    
    Logger.newline()
    seed_prompt = Panel(
        "[cyan]💭[/cyan] Enter a topic, theme, or perspective to explore\n[dim]Press Enter to let your Voice Blueprint guide the ideas[/dim]",
        border_style="dim",
        padding=(0, 1)
    )
    get_console().print(seed_prompt)
    
    seed = inquirer.text(
        message="Your input:",
        default=""
    ).execute()
    
    if seed:
        Logger.info(f"Starting with seed: [gs.bold_primary]{seed}[/gs.bold_primary]\n")

    # Initialize in-memory session state
    current_batch: List[SuggestedIdea] = []
    ignored_topics: List[str] = []
    feedback_history: List[str] = []

    # Main workflow loop
    _carousel_loop(current_batch, ignored_topics, feedback_history, seed, client, bp)


def _carousel_loop(
    current_batch: List[SuggestedIdea],
    ignored_topics: List[str],
    feedback_history: List[str],
    seed: str,
    client: LLMService,
    blueprint
) -> None:
    while True:
        # Fetch initial batch if empty
        if not current_batch:
            _fetch_more_ideas(current_batch, ignored_topics, feedback_history, seed, client, blueprint)

        Logger.newline()
        Logger.newline()
        Logger.info(f"{SPARKLES} [gs.bold_primary]Suggested Post Ideas[/gs.bold_primary]\n")

        # Display all ideas as cards using standardized component
        render_idea_cards([{
            'topic': idea.topic,
            'hook_summary': idea.hook_summary,
            'angle': getattr(idea, 'angle', None)
        } for idea in current_batch])

        Logger.newline()

        choices = [
            Choice(value=str(i + 1), name=f"{i+1}. {idea.topic}") 
            for i, idea in enumerate(current_batch)
        ]
        choices.extend([
            Choice(value="m", name=f"{SPARKLES} Get More Ideas"),
            Choice(value="f", name=f"{CHAT} Provide Feedback"),
            Choice(value="q", name=f"{CROSS} Quit")
        ])
        
        action = inquirer.select(
            message="Choose an action or idea:",
            choices=choices,
            default="1",
        ).execute()

        if action.isdigit():
            idx = int(action) - 1
            selected_idea = current_batch[idx]

            if _drafting_loop(client, blueprint, selected_idea):
                # Draft saved, exit
                return
            else:
                # Discarded & Back
                continue

        elif action == "m":
            # Move current batch to ignored and fetch more
            _fetch_more_ideas(current_batch, ignored_topics, feedback_history, seed, client, blueprint)
            continue

        elif action == "f":
            # Provide feedback and refresh
            feedback = inquirer.text(
                message="What should we change? (e.g., 'more technical', 'less corporate')",
            ).execute()
            if feedback:
                feedback_history.append(feedback)
                _fetch_more_ideas(current_batch, ignored_topics, feedback_history, seed, client, blueprint)
            continue

        elif action == "q":
            Logger.info("[gs.muted]Exiting...[/gs.muted]\n")
            raise typer.Exit(0)


def _fetch_more_ideas(
    current_batch: List[SuggestedIdea],
    ignored_topics: List[str],
    feedback_history: List[str],
    seed: str,
    client: LLMService,
    blueprint,
) -> None:
    if current_batch:
        # Move current batch to ignored topics to avoid duplicates in next fetch
        for idea in current_batch:
            if idea.topic not in ignored_topics:
                ignored_topics.append(idea.topic)
        current_batch.clear()

    with Logger.status("[gs.magic]Brainstorming ideas...[/gs.magic]") as status:
        raw_ideas = client.brainstorm_ideas(
            blueprint=blueprint,
            seed=seed,
            feedback=feedback_history,
            ignored_topics=ignored_topics
        )
        if status:
            status.update("[gs.magic]Processing responses...[/gs.magic]")

        # Create SuggestedIdea objects
        for ri in raw_ideas:
            current_batch.append(SuggestedIdea(
                topic=ri['topic'],
                angle=ri.get('angle', ''),
                hook_summary=ri.get('hook_summary', ri.get('angle', ''))
            ))


def _drafting_loop(client: LLMService, blueprint, idea: SuggestedIdea) -> bool:
    Logger.newline()
    Logger.info(f"Topic: [gs.bold_primary]{idea.topic}[/gs.bold_primary]")
    Logger.info(f"Angle: [gs.info]{idea.angle}[/gs.info]\n")

    post_history = []
    with Logger.status("[gs.magic]Drafting post...[/gs.magic]"):
        content = client.generate_post(idea.topic, blueprint, history=post_history)

    while True:
        Logger.newline()
        render_post_preview(content)
        Logger.newline()

        action = inquirer.select(
            message="Choose an action:",
            choices=[
                Choice(value="a", name=f"{CHECK} Accept & Save"),
                Choice(value="f", name=f"{CHAT} Provide Feedback & Regenerate"),
                Choice(value="d", name=f"{CROSS} Discard & Back"),
            ],
            default="a"
        ).execute()

        if action == "a":
            # Save as memory
            Logger.newline()
            Logger.info("Saving to memories...")

            mem = Memory(
                content=content,
                topic=idea.topic
            )

            filepath = memory.save(mem)
            render_completion_animation("Post Saved to Memory Crystal")
            Logger.info(f"File: [gs.primary]{filepath}[/gs.primary]\n")
            return True

        elif action == "f":
            # Get feedback and regenerate
            feedback = inquirer.text(
                message="What should we change? (e.g., 'make it shorter', 'different hook')",
            ).execute()
            if feedback:
                post_history.append({'content': content, 'feedback': feedback})
                with Logger.status("[gs.magic]Improving post...[/gs.magic]"):
                    content = client.generate_post(idea.topic, blueprint, history=post_history)
            continue

        elif action == "d":
            Logger.info("Draft discarded. Returning to carousel...\n")
            return False