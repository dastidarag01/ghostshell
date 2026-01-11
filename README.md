# GhostShell

A Digital Twin content engine for LinkedIn creators.

## Installation

**Requirements:**
- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)
- Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

**Install:**
```bash
# Install dependencies
poetry install

# Run GhostShell
poetry run ghostshell init
```

## Quick Start

```bash
# 1. Initialize (first time only)
poetry run ghostshell init

# 2. Add your existing posts
poetry run ghostshell add

# 3. Analyze your voice (after adding posts)
poetry run ghostshell distill

# 4. Create new content
poetry run ghostshell create
```

## How It Works

GhostShell learns your unique LinkedIn voice by analyzing your past posts (stored as "Memory Crystals"). It creates a "Blueprint" - a distilled essence of your writing style, tone, and topics. When you create new content, GhostShell uses this blueprint to generate posts that sound authentically like you.

## Key Features

- **🧠 Voice Blueprint:** Deep analysis of your writing style, niche, and content structure.
- **✨ Infinite Carousel:** A frictionless brainstorming workflow that generates endless ideas based on your voice.