
import re
from pathlib import Path
from typing import List
import frontmatter
import uuid as uuid_lib

from ghostshell.models.memory import Memory
from ghostshell.utils import get_memories_dir
from ghostshell.logger import Logger
from ghostshell.prompts import ERR_COULD_NOT_LOAD_FILE


def load_all() -> List[Memory]:
    memories_dir = get_memories_dir()
    if not memories_dir.exists():
        return []

    memories = []
    for md_file in memories_dir.glob("*.md"):
        try:
            if not md_file.is_file():
                continue

            post = frontmatter.load(md_file)

            if not post.content:
                Logger.warning(
                    ERR_COULD_NOT_LOAD_FILE.format(
                        filename=md_file.name,
                        error="Empty content"
                    )
                )
                continue

            memory = Memory(
                topic=post.metadata.get('topic', ''),
                content=post.content
            )
            memories.append(memory)
        except Exception as e:
            Logger.warning(
                ERR_COULD_NOT_LOAD_FILE.format(filename=md_file.name, error=str(e))
            )

    return memories


def save(memory: Memory) -> Path:
    memories_dir = get_memories_dir()
    memories_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r'[^a-z0-9]+', '-', memory.topic.lower()).strip('-')
    filename = f"{slug}.md" if slug else f"memory-{uuid_lib.uuid4().hex[:8]}.md"

    # Handle duplicate filenames
    filepath = memories_dir / filename
    counter = 1
    while filepath.exists():
        filepath = memories_dir / f"{slug}-{counter}.md"
        counter += 1

    # Write with frontmatter
    post = frontmatter.Post(memory.content)
    post.metadata = {'topic': memory.topic} if memory.topic else {}

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    return filepath


def get_summary(memories: List[Memory]) -> str:
    posts = []
    for i, m in enumerate(memories):
        posts.append(f"POST {i + 1}:\nTopic: {m.topic or 'none'}\n\nContent:\n{m.content}")

    return "\n\n---\n\n".join(posts)
