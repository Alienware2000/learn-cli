# Module 7: Build Your Own Project

## Congratulations!

You've completed the curriculum! You now understand:
- How to call the Claude API
- How to structure data with Pydantic
- How to manage configuration safely
- How to build CLIs with Typer
- How to craft effective prompts
- How all these pieces connect in a real project

Now it's time to **build something yourself!**

---

## Project Ideas

Here are some AI-powered CLI tools you could build:

### Beginner Level

**1. Smart Commit Message Generator**
```bash
git-ai commit
# Analyzes staged changes
# Generates a descriptive commit message
# Asks for confirmation before committing
```

**2. Code Explainer**
```bash
explain code.py
# Reads a file
# Sends to Claude with "explain this code" prompt
# Outputs beginner-friendly explanation
```

**3. Daily Journal Prompter**
```bash
journal new
# Asks about your day
# Generates follow-up questions
# Saves entries to markdown files
```

### Intermediate Level

**4. README Generator**
```bash
readme-ai generate ./my-project
# Scans project structure
# Identifies language, framework
# Generates README.md with sections
```

**5. Study Flashcard Creator**
```bash
flashcards create "Python decorators"
# Asks what you want to learn
# Generates Q&A flashcards
# Saves as JSON for review
```

**6. Meeting Notes Summarizer**
```bash
meeting-ai summarize notes.txt
# Reads meeting transcript
# Extracts action items
# Generates summary with owners and deadlines
```

### Advanced Level

**7. Code Review Assistant**
```bash
review-ai check ./src
# Analyzes code files
# Identifies potential issues
# Suggests improvements
```

**8. Documentation Generator**
```bash
docs-ai generate ./module.py
# Reads Python file
# Generates docstrings for functions
# Creates API documentation
```

---

## Project Template

Use this structure for your project:

```
my-cli-project/
├── pyproject.toml          # Project config & dependencies
├── .env.example            # Template for environment variables
├── .gitignore              # Ignore .env and __pycache__
├── README.md               # Project documentation
└── my_cli/
    ├── __init__.py         # Package marker + version
    ├── __main__.py         # Enables: python -m my_cli
    ├── main.py             # CLI commands (Typer)
    ├── config.py           # Settings (pydantic-settings)
    ├── models.py           # Data structures (Pydantic)
    ├── prompts.py          # System prompts
    └── ai.py               # Claude API logic
```

---

## Step-by-Step Guide

### Step 1: Set Up the Project

```bash
# Create project directory
mkdir my-ai-cli
cd my-ai-cli

# Create package directory
mkdir my_ai_cli
touch my_ai_cli/__init__.py
```

### Step 2: Create pyproject.toml

```toml
[project]
name = "my-ai-cli"
version = "0.1.0"
description = "My AI-powered CLI tool"
requires-python = ">=3.10"
dependencies = [
    "anthropic>=0.18.0",
    "typer[all]>=0.9.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
my-cli = "my_ai_cli.main:app"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

### Step 3: Create config.py

```python
"""Configuration from environment variables."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MY_CLI_",
    )


_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

### Step 4: Create models.py

```python
"""Data models for your CLI."""

from pydantic import BaseModel, Field


class YourModel(BaseModel):
    """Define your data structure here."""

    title: str = Field(description="A short title")
    content: str = Field(description="The main content")
    # Add more fields as needed
```

### Step 5: Create prompts.py

```python
"""Prompts for Claude."""

SYSTEM_PROMPT = """You are a helpful assistant for [YOUR USE CASE].

When responding, use this JSON format:
{
    "field1": "value",
    "field2": "value"
}

Be concise and helpful.
"""

def get_system_prompt():
    return SYSTEM_PROMPT
```

### Step 6: Create ai.py

```python
"""Claude API integration."""

import json
from anthropic import Anthropic
from .config import get_settings
from .prompts import get_system_prompt


def call_claude(user_message: str) -> dict:
    """Send a message to Claude and get structured response."""

    settings = get_settings()
    client = Anthropic(
        api_key=settings.anthropic_api_key.get_secret_value()
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=get_system_prompt(),
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # Parse JSON response
    text = response.content[0].text
    return json.loads(text)
```

### Step 7: Create main.py

```python
"""CLI entry point."""

from typing import Annotated, Optional
import typer
from rich.console import Console
from rich.panel import Panel

from .ai import call_claude

app = typer.Typer(
    name="my-cli",
    help="My AI-powered CLI tool"
)
console = Console()


@app.command()
def run(
    input_text: Annotated[
        str,
        typer.Argument(help="Your input")
    ],
):
    """Run the main command."""

    console.print(f"[dim]Processing:[/dim] {input_text}")

    try:
        result = call_claude(input_text)
        console.print(Panel(
            str(result),
            title="Result",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
```

### Step 8: Create Supporting Files

**.env.example:**
```
MY_CLI_ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**.gitignore:**
```
.env
__pycache__/
*.pyc
.venv/
dist/
*.egg-info/
```

**my_ai_cli/__init__.py:**
```python
__version__ = "0.1.0"
```

**my_ai_cli/__main__.py:**
```python
from .main import app
app()
```

### Step 9: Install and Test

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode
pip install -e .

# Create .env with your API key
cp .env.example .env
# Edit .env to add your real API key

# Test it!
my-cli run "Hello world"
```

---

## Checklist for Your Project

### Planning
- [ ] Decided what your CLI will do
- [ ] Identified inputs (arguments, options, files)
- [ ] Defined outputs (JSON, Markdown, files)
- [ ] Sketched the data models you need

### Implementation
- [ ] Created project structure
- [ ] Set up pyproject.toml with dependencies
- [ ] Created config.py for settings
- [ ] Defined Pydantic models in models.py
- [ ] Wrote prompts in prompts.py
- [ ] Implemented Claude API calls in ai.py
- [ ] Built CLI commands in main.py

### Polish
- [ ] Added helpful --help descriptions
- [ ] Handled errors gracefully
- [ ] Created .env.example
- [ ] Wrote README.md
- [ ] Tested with different inputs

### Share (Optional)
- [ ] Initialized git repo
- [ ] Created GitHub repository
- [ ] Pushed your code
- [ ] Added screenshots to README

---

## Tips for Success

### Start Simple
Begin with the smallest working version:
1. One command
2. One API call
3. Print the result

Then add features incrementally.

### Test Your Prompts
Before writing code, test your prompts in the Claude web interface. Iterate until you get consistent, well-formatted responses.

### Handle Errors Gracefully
Users will provide unexpected input. Wrap API calls in try/except and show helpful error messages.

### Use Rich for Output
Rich makes your CLI look professional:
```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
console.print("[green]Success![/green]")
console.print(Panel("Content", title="Title"))
```

### Document as You Go
Add docstrings and comments. Future you will thank present you.

---

## Example: Commit Message Generator

Here's a complete simple example:

**prompts.py:**
```python
SYSTEM_PROMPT = """You are a git commit message generator.

Given a description of changes, generate a commit message following these rules:
- Start with a type: feat, fix, docs, style, refactor, test, chore
- Use imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add a body if needed for complex changes

Respond with JSON:
{
    "type": "feat|fix|docs|...",
    "subject": "Short description",
    "body": "Optional longer description"
}
"""
```

**ai.py:**
```python
def generate_commit_message(changes: str) -> dict:
    """Generate a commit message for the given changes."""

    settings = get_settings()
    client = Anthropic(
        api_key=settings.anthropic_api_key.get_secret_value()
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Generate a commit message for: {changes}"}
        ]
    )

    return json.loads(response.content[0].text)
```

**main.py:**
```python
@app.command()
def commit(
    changes: Annotated[str, typer.Argument(help="Description of your changes")]
):
    """Generate a git commit message."""

    result = generate_commit_message(changes)

    message = f"{result['type']}: {result['subject']}"
    if result.get('body'):
        message += f"\n\n{result['body']}"

    console.print(Panel(message, title="Suggested Commit Message"))

    if typer.confirm("Use this message?"):
        # Run: git commit -m "message"
        import subprocess
        subprocess.run(["git", "commit", "-m", message])
```

---

## You're Ready!

You have all the knowledge you need to build AI-powered CLI tools:

| Skill | Module | You Can Now... |
|-------|--------|----------------|
| API Calls | 1 | Talk to Claude programmatically |
| Data Models | 2 | Define and validate data structures |
| Configuration | 3 | Manage secrets and settings safely |
| CLI Building | 4 | Create professional command-line tools |
| Prompting | 5 | Get structured, useful AI responses |
| Architecture | 6 | Organize code into maintainable modules |

**Now go build something awesome!**

---

## Share Your Project

Built something cool? Consider:
- Pushing to GitHub
- Writing a blog post about what you learned
- Sharing in developer communities

The best way to learn is to build, and the best way to solidify knowledge is to teach others!
