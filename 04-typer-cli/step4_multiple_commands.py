"""
Step 4: Multiple Commands (Subcommands)

Real CLIs have multiple commands:
    git status
    git commit
    git push

Typer makes this easy with app.command()

Run with:
    python step4_multiple_commands.py --help
    python step4_multiple_commands.py greet Alice
    python step4_multiple_commands.py add 5 3
    python step4_multiple_commands.py info
"""

import typer

# Create the app
app = typer.Typer(
    name="demo",
    help="A demo CLI with multiple commands"
)


@app.command()
def greet(name: str):
    """Say hello to someone."""
    print(f"Hello, {name}!")


@app.command()
def add(a: int, b: int):
    """Add two numbers together."""
    result = a + b
    print(f"{a} + {b} = {result}")


@app.command()
def info():
    """Show information about this CLI."""
    print("Demo CLI v1.0")
    print("This is a learning example for Typer")
    print()
    print("Available commands:")
    print("  greet  - Say hello")
    print("  add    - Add numbers")
    print("  info   - Show this info")


if __name__ == "__main__":
    app()


# ============================================================
# KEY CONCEPTS:
#
# 1. Create an app
#    app = typer.Typer(name="...", help="...")
#
# 2. Add commands with decorator
#    @app.command()
#    def command_name(...):
#        ...
#
# 3. Run the app
#    app()  (not typer.run())
#
# 4. Usage
#    python script.py COMMAND [ARGS]
#    python script.py greet Alice
#    python script.py add 1 2
# ============================================================
