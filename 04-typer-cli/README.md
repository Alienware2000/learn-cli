# Module 4: Typer CLI

## What You'll Learn

By the end of this module, you'll understand:
- Why CLI frameworks exist (vs manual parsing)
- How to create commands with Typer
- Arguments vs Options (flags)
- Multiple commands (subcommands)
- Beautiful output with Rich

---

## Step 1: The Problem

**File:** `step1_no_framework.py`

Without a framework, parsing CLI arguments is painful:

```python
import sys

args = sys.argv[1:]
# Now manually parse --name, --age, handle errors, etc.
# 50+ lines just for 2 arguments!
```

**Problems:**
- Tons of boilerplate code
- Manual type conversion
- No automatic --help
- Inconsistent error handling

---

## Step 2: Your First Typer Command

**File:** `step2_basic_typer.py`

```python
import typer

def main(name: str, age: int = 25):
    """Greet someone by name."""
    print(f"Hello {name}, you are {age} years old!")

if __name__ == "__main__":
    typer.run(main)
```

**That's it!** Typer uses type hints to understand:
- `name: str` → Required argument
- `age: int = 25` → Optional, default 25, must be integer

### Run It

```bash
python step2_basic_typer.py --help
python step2_basic_typer.py Alice
python step2_basic_typer.py Alice --age 30
```

### The Magic

| Type Hint | CLI Behavior |
|-----------|--------------|
| `name: str` | Required positional argument |
| `age: int = 25` | Optional `--age`, defaults to 25 |
| Docstring | Becomes `--help` description |

---

## Step 3: Options (Flags)

**File:** `step3_options.py`

Options are named flags like `--name` or `-n`:

```python
from typing import Annotated
import typer

def main(
    name: Annotated[str, typer.Option("--name", "-n", help="Person to greet")] = "World",
    loud: Annotated[bool, typer.Option("--loud", "-l", help="Greet loudly")] = False,
):
    message = f"Hello, {name}!"
    if loud:
        message = message.upper()
    print(message)
```

### Run It

```bash
python step3_options.py --help
python step3_options.py --name Alice
python step3_options.py -n Bob --loud
python step3_options.py -n Bob -l
```

### Arguments vs Options

| Type | Syntax | Example |
|------|--------|---------|
| Argument | Positional | `greet Alice` |
| Option | With flag | `greet --name Alice` |

### typer.Option()

```python
typer.Option(
    "--long-name",    # Long form (required)
    "-s",             # Short form (optional)
    help="...",       # Description
    min=1, max=10,    # Validation (for numbers)
)
```

---

## Step 4: Multiple Commands

**File:** `step4_multiple_commands.py`

Real CLIs have subcommands (like `git commit`, `git push`):

```python
import typer

app = typer.Typer(help="My CLI tool")

@app.command()
def greet(name: str):
    """Say hello."""
    print(f"Hello, {name}!")

@app.command()
def add(a: int, b: int):
    """Add two numbers."""
    print(f"{a} + {b} = {a + b}")

if __name__ == "__main__":
    app()
```

### Run It

```bash
python step4_multiple_commands.py --help
python step4_multiple_commands.py greet Alice
python step4_multiple_commands.py add 5 3
```

### Pattern

1. Create app: `app = typer.Typer()`
2. Add commands: `@app.command()`
3. Run app: `app()`

---

## Step 5: Beautiful Output with Rich

**File:** `step5_rich_output.py`

Typer includes Rich for pretty terminal output:

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Colored text
console.print("[green]Success![/green]")
console.print("[bold red]Error![/bold red]")

# Panels
console.print(Panel("Content here", title="My Panel"))

# Tables
table = Table(title="Tasks")
table.add_column("Task")
table.add_column("Status")
table.add_row("Buy milk", "Done")
console.print(table)
```

### Color Tags

| Tag | Effect |
|-----|--------|
| `[red]...[/red]` | Red text |
| `[bold]...[/bold]` | Bold text |
| `[italic]...[/italic]` | Italic text |
| `[green on white]...[/green on white]` | Green text on white background |

---

## How This Connects to the Real Project

In `contextual-task-cli/main.py`:

```python
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(name="task-cli", help="AI-powered task planning")
console = Console()

@app.command()
def plan(
    task: Annotated[Optional[str], typer.Argument(...)] = None,
    output_format: Annotated[OutputFormat, typer.Option("--format", "-f")] = OutputFormat.MARKDOWN,
):
    """Create a task plan through AI conversation."""
    console.print(Panel("Welcome!", title="Task CLI"))
    # ... rest of the code
```

---

## Summary

| Step | Concept | Key Code |
|------|---------|----------|
| 1 | The problem | Manual sys.argv parsing is painful |
| 2 | Basic Typer | `typer.run(main)` |
| 3 | Options | `Annotated[str, typer.Option("--flag")]` |
| 4 | Multiple commands | `@app.command()` |
| 5 | Rich output | `console.print("[green]...[/green]")` |

## Quick Reference

```python
# Simple CLI (one function)
import typer

def main(name: str, count: int = 1):
    """Description for --help."""
    for _ in range(count):
        print(f"Hello {name}")

typer.run(main)
```

```python
# Multi-command CLI
import typer

app = typer.Typer()

@app.command()
def cmd1(): ...

@app.command()
def cmd2(): ...

app()
```

---

## Exercises (Optional)

1. Create a CLI that takes a filename and prints its contents
2. Add a `--lines` option to limit how many lines to print
3. Create a multi-command CLI with `read` and `write` commands
4. Add Rich output with colored status messages

---

## What's Next?

In [Module 5: Prompt Engineering](../05-prompt-engineering/), you'll learn how to get Claude to respond in structured formats (like JSON) that your code can parse!
