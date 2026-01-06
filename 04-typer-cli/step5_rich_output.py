"""
Step 5: Beautiful Output with Rich

Typer includes Rich for beautiful terminal output:
- Colors
- Panels
- Tables
- Progress bars
- And more!

Run with:
    python step5_rich_output.py
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

# Create a Rich console for output
console = Console()


def main():
    """Demonstrate Rich formatting capabilities."""

    # === Colored Text ===
    console.print("\n[bold blue]===  Rich Text Formatting ===[/bold blue]\n")

    console.print("[green]This is green text[/green]")
    console.print("[bold red]This is bold red[/bold red]")
    console.print("[italic yellow]This is italic yellow[/italic yellow]")
    console.print("[underline]This is underlined[/underline]")
    console.print("[bold magenta]You can [underline]combine[/underline] styles![/bold magenta]")

    # === Panels ===
    console.print("\n[bold blue]=== Panels ===[/bold blue]\n")

    console.print(Panel(
        "This is content inside a panel.\nPanels are great for highlighting information!",
        title="My Panel",
        border_style="green"
    ))

    console.print(Panel(
        "[red]Error:[/red] Something went wrong!",
        title="Error",
        border_style="red"
    ))

    # === Tables ===
    console.print("\n[bold blue]=== Tables ===[/bold blue]\n")

    table = Table(title="Task List")
    table.add_column("ID", style="cyan")
    table.add_column("Task", style="white")
    table.add_column("Priority", style="magenta")
    table.add_column("Status", style="green")

    table.add_row("1", "Buy groceries", "High", "Pending")
    table.add_row("2", "Call mom", "Medium", "Done")
    table.add_row("3", "Fix bug", "Critical", "In Progress")

    console.print(table)

    # === Interactive Prompts ===
    console.print("\n[bold blue]=== Interactive Prompts ===[/bold blue]\n")

    name = Prompt.ask("What is your name", default="Anonymous")
    console.print(f"Hello, [bold]{name}[/bold]!")

    if Confirm.ask("Do you want to see a secret?"):
        console.print("[bold yellow]The secret is: Typer + Rich = Amazing CLIs![/bold yellow]")
    else:
        console.print("Okay, keeping the secret safe!")

    # === Summary ===
    console.print("\n")
    console.print(Panel(
        "[bold]Rich Features Used:[/bold]\n"
        "• Colored text with [green][tags][/green]\n"
        "• Panels for highlighted content\n"
        "• Tables for structured data\n"
        "• Prompts for user input\n"
        "• Confirmation dialogs",
        title="Summary",
        border_style="blue"
    ))


if __name__ == "__main__":
    typer.run(main)


# ============================================================
# KEY CONCEPTS:
#
# 1. Console
#    console = Console()
#    console.print("[green]colored[/green]")
#
# 2. Color/Style Tags
#    [red], [bold], [italic], [underline]
#    [bold red], [italic yellow on blue]
#
# 3. Panel
#    Panel("content", title="Title", border_style="color")
#
# 4. Table
#    table = Table(title="...")
#    table.add_column("Name", style="...")
#    table.add_row("value1", "value2")
#
# 5. Prompts
#    Prompt.ask("Question", default="...")
#    Confirm.ask("Yes/no question?")
# ============================================================
