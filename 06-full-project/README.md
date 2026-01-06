# Module 6: Putting It All Together

## What You'll Learn

By now you've learned all the individual pieces:
- **Module 1**: How to call Claude's API and manage conversations
- **Module 2**: How to define and validate data with Pydantic
- **Module 3**: How to manage configuration safely
- **Module 4**: How to build beautiful CLIs with Typer
- **Module 5**: How to craft prompts for structured AI responses

Now it's time to see how they **all connect** in a real project!

---

## The Big Picture

The `contextual-task-cli` project combines everything you've learned:

```
User runs:  task-cli plan "Build a REST API"
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│  main.py (Typer)                                                │
│  - Parses CLI arguments                                         │
│  - Loads config                                                 │
│  - Runs conversation loop                                       │
│  - Formats and displays output                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  config.py (pydantic-settings)                                  │
│  - Reads API key from environment                               │
│  - Provides settings to other modules                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  conversation.py (Claude API)                                   │
│  - Manages the Q&A with Claude                                  │
│  - Uses prompts.py for system prompts                           │
│  - Parses JSON responses into models.py structures              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  models.py (Pydantic)                                           │
│  - Defines Task, TaskPlan, ClarifyingQuestion                   │
│  - Validates all data flowing through the app                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  formatters.py                                                  │
│  - Converts TaskPlan to Markdown or JSON                        │
│  - Output displayed via Rich console                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## File-by-File Breakdown

### 1. `models.py` - The Data Foundation

**Module Used:** Module 2 (Pydantic)

This file defines *what data looks like* in the application:

```python
from pydantic import BaseModel, Field
from enum import Enum

# Enum for fixed choices (you learned this!)
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# A single task (nested inside TaskPlan)
class Task(BaseModel):
    title: str = Field(description="Short, actionable task title")
    description: str
    priority: Priority = Priority.MEDIUM
    estimated_hours: float | None = None
    dependencies: list[str] = Field(default_factory=list)

# The main output - contains a list of Tasks
class TaskPlan(BaseModel):
    title: str
    summary: str
    tasks: list[Task]  # Nested models!
    assumptions: list[str] = Field(default_factory=list)
```

**Key Patterns from Module 2:**
- `Field()` for defaults and descriptions
- `str Enum` for fixed choices that serialize nicely
- Nested models (`TaskPlan` contains `list[Task]`)
- `default_factory=list` to avoid the mutable default bug

---

### 2. `config.py` - Safe Configuration

**Module Used:** Module 3 (Environment Variables)

This file manages settings from environment variables:

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # SecretStr hides the API key in logs
    anthropic_api_key: SecretStr

    # Defaults for other settings
    model_name: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    max_questions: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TASK_CLI_",  # All vars start with TASK_CLI_
    )

# Singleton pattern - load settings once
_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

**Key Patterns from Module 3:**
- `BaseSettings` automatically reads from environment
- `SecretStr` protects sensitive values
- `env_prefix` namespaces your variables
- Singleton pattern for efficiency

---

### 3. `prompts.py` - AI Instructions

**Module Used:** Module 5 (Prompt Engineering)

This file contains the system prompts that tell Claude how to behave:

```python
# System prompt with template variable
SYSTEM_PROMPT = """You are a task planning assistant.

## Response Format During Conversation
When asking questions, respond with JSON:
{{
    "status": "questioning",
    "questions": [
        {{
            "question": "Your question here?",
            "context": "Why you're asking"
        }}
    ]
}}

When ready to create a plan:
{{
    "status": "ready",
    "summary": "What you understand"
}}

Ask a MAXIMUM of {max_questions} questions total.
"""

def get_system_prompt(max_questions: int = 5) -> str:
    return SYSTEM_PROMPT.format(max_questions=max_questions)
```

**Key Patterns from Module 5:**
- System prompt sets Claude's behavior
- Template variables (`{max_questions}`) for dynamic prompts
- Double braces `{{}}` for literal braces in output
- Clear JSON structure with examples

---

### 4. `conversation.py` - The AI Brain

**Module Used:** Module 1 (Core Concepts) + Module 5 (Prompt Engineering)

This is the heart of the application - where AI conversations happen:

```python
from anthropic import Anthropic
from .config import get_settings
from .models import ClarifyingQuestion, TaskPlan
from .prompts import get_system_prompt

class ConversationManager:
    def __init__(self):
        self.settings = get_settings()
        self.client = Anthropic(
            api_key=self.settings.anthropic_api_key.get_secret_value()
        )
        self.messages = []  # Conversation history!
        self.is_ready = False

    def start(self, task: str) -> list[ClarifyingQuestion]:
        """Start conversation with initial task."""
        self.messages.append({
            "role": "user",
            "content": f"I need help planning: {task}"
        })
        return self._get_claude_response()

    def answer(self, response: str) -> list[ClarifyingQuestion]:
        """Add user's answer and get follow-up."""
        self.messages.append({
            "role": "user",
            "content": response
        })
        return self._get_claude_response()

    def _get_claude_response(self):
        """Call Claude API with full conversation history."""
        response = self.client.messages.create(
            model=self.settings.model_name,
            system=get_system_prompt(self.settings.max_questions),
            messages=self.messages  # All history!
        )
        # Parse JSON response into ClarifyingQuestion objects...
```

**Key Patterns from Modules 1 & 5:**
- Anthropic client with API key from settings
- Full conversation history sent with each call
- System prompt from prompts.py
- JSON responses parsed into Pydantic models

---

### 5. `formatters.py` - Output Conversion

**Module Used:** Module 2 (Pydantic - serialization)

This file converts `TaskPlan` objects to different formats:

```python
from .models import TaskPlan

def format_as_json(plan: TaskPlan) -> str:
    """Pydantic handles all the serialization!"""
    return plan.model_dump_json(indent=2)

def format_as_markdown(plan: TaskPlan) -> str:
    """Manual formatting for human-readable output."""
    lines = [f"# {plan.title}", ""]
    lines.append(f"## Summary\n{plan.summary}\n")

    for i, task in enumerate(plan.tasks, 1):
        lines.append(f"### {i}. {task.title}")
        lines.append(task.description)

    return "\n".join(lines)
```

**Key Pattern:** Separation of concerns - models know *what* data is, formatters know *how to display it*.

---

### 6. `main.py` - The CLI Interface

**Module Used:** Module 4 (Typer CLI)

This file brings everything together in a CLI:

```python
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .config import get_settings
from .conversation import ConversationManager
from .formatters import format_as_json, format_as_markdown

app = typer.Typer(name="task-cli", help="AI-powered task planning")
console = Console()

@app.command()
def plan(
    task: Optional[str] = None,
    output_format: OutputFormat = OutputFormat.MARKDOWN,
    output_file: Optional[str] = None,
):
    """Create a task plan through AI conversation."""

    # Step 1: Load config
    settings = get_settings()

    # Step 2: Get task if not provided
    if task is None:
        console.print(Panel("Welcome!", title="Task CLI"))
        task = Prompt.ask("What task would you like to plan?")

    # Step 3: Run conversation
    manager = ConversationManager()
    questions = manager.start(task)

    while questions and not manager.is_ready:
        for q in questions:
            console.print(Panel(q.question, title="Question"))
            answer = Prompt.ask("Your answer")
        questions = manager.answer(answer)

    # Step 4: Generate plan
    plan = manager.generate_plan()

    # Step 5: Format and output
    if output_format == OutputFormat.JSON:
        output = format_as_json(plan)
    else:
        output = format_as_markdown(plan)

    if output_file:
        with open(output_file, "w") as f:
            f.write(output)
    else:
        console.print(output)
```

**Key Patterns from Module 4:**
- `typer.Typer()` creates the app
- `@app.command()` adds commands
- `Annotated[]` with `typer.Option()` for flags
- Rich for beautiful output

---

## How Data Flows

Let's trace a complete request through the system:

### 1. User Input
```bash
task-cli plan "Build a REST API"
```

### 2. CLI Parses Arguments (main.py)
```python
# Typer parses: task="Build a REST API"
# Loads config from environment
settings = get_settings()  # → Settings object with API key
```

### 3. Conversation Starts (conversation.py)
```python
manager = ConversationManager()  # Creates Anthropic client
questions = manager.start("Build a REST API")
# → Sends message to Claude with system prompt
# → Claude responds with JSON questions
# → JSON parsed into list[ClarifyingQuestion]
```

### 4. Q&A Loop (main.py + conversation.py)
```python
while questions:
    # Display questions via Rich
    answer = Prompt.ask("Your answer")
    questions = manager.answer(answer)
    # → Answer added to messages list
    # → Full history sent to Claude
    # → New questions or "ready" signal returned
```

### 5. Plan Generation (conversation.py)
```python
plan = manager.generate_plan()
# → Builds conversation summary
# → Sends plan generation prompt (from prompts.py)
# → Claude returns JSON plan
# → JSON parsed into TaskPlan object (models.py)
```

### 6. Output Formatting (formatters.py)
```python
output = format_as_markdown(plan)
# → TaskPlan converted to markdown string
# → Displayed via Rich console
```

---

## Module Connection Map

| Module | Teaches | Used In Project |
|--------|---------|-----------------|
| 1. Core Concepts | API calls, messages list, classes | `conversation.py` |
| 2. Pydantic | Data models, validation | `models.py`, `formatters.py` |
| 3. Environment | Settings, .env files | `config.py` |
| 4. Typer | CLI commands, Rich output | `main.py` |
| 5. Prompts | System prompts, JSON format | `prompts.py` |

---

## Design Decisions Explained

### Why Separate Files?

Each file has one job (separation of concerns):
- `models.py` - Defines data shapes
- `config.py` - Manages settings
- `prompts.py` - Contains AI instructions
- `conversation.py` - Handles AI communication
- `formatters.py` - Converts output
- `main.py` - Orchestrates everything

This makes the code:
- **Easier to understand** - each file is focused
- **Easier to modify** - change prompts without touching API code
- **Easier to test** - can test each part independently

### Why a Class for Conversation?

The `ConversationManager` class holds state:
- The messages list (conversation history)
- Whether Claude is ready
- How many questions have been asked

Without a class, you'd have to pass these around as function parameters. The class bundles the data with the functions that use it.

### Why Pydantic Everywhere?

Every piece of data has a Pydantic model:
- **Settings** - Validated on load, fails early if missing
- **Questions** - Structured data, not raw strings
- **Tasks** - Validated priorities, optional fields
- **Plans** - Clean serialization to JSON

This catches errors early and makes the code self-documenting.

---

## Try It Yourself

Navigate to the contextual-task-cli project and explore:

```bash
cd /home/alienware2000/projects/contextual-task-cli

# Look at the structure
ls contextual_task_cli/

# Read files in order of data flow:
# 1. config.py    - Where settings come from
# 2. models.py    - What data looks like
# 3. prompts.py   - What we tell Claude
# 4. conversation.py - How we talk to Claude
# 5. formatters.py   - How we display results
# 6. main.py      - How it all connects
```

Try adding print statements to trace the flow:
```python
# In conversation.py, in _get_claude_response():
print(f"Sending {len(self.messages)} messages to Claude")
print(f"Messages: {self.messages}")
```

---

## Summary

You've now seen how all the modules connect:

```
┌─────────────────────────────────────────────────────────────────┐
│                     contextual-task-cli                         │
├─────────────────────────────────────────────────────────────────┤
│  Module 4 (Typer)     →  main.py          (CLI interface)       │
│  Module 3 (Env)       →  config.py        (settings)            │
│  Module 5 (Prompts)   →  prompts.py       (AI instructions)     │
│  Module 1 (API)       →  conversation.py  (AI communication)    │
│  Module 2 (Pydantic)  →  models.py        (data structures)     │
│  Module 2 (Pydantic)  →  formatters.py    (output conversion)   │
└─────────────────────────────────────────────────────────────────┘
```

Each module taught you a concept. The real project shows how they work **together**.

---

## What's Next?

In [Module 7: Build Your Own Project](../07-your-project/), you'll use everything you've learned to create your own AI-powered CLI tool!
