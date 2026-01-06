"""
Step 2: Your First Typer Command

Typer uses Python type hints to create CLI arguments.
Watch how little code we need!

Run with:
    python step2_basic_typer.py --help
    python step2_basic_typer.py Alice
    python step2_basic_typer.py Alice --age 30
"""

import typer


def main(name: str, age: int = 25):
    """
    Greet someone by name.

    This docstring becomes the --help description!
    """
    print(f"Hello {name}, you are {age} years old!")


if __name__ == "__main__":
    typer.run(main)


# ============================================================
# THAT'S IT! Compare to step1's 50+ lines!
#
# What Typer does automatically:
# - name: str → Required positional argument
# - age: int = 25 → Optional with default, auto-converts to int
# - Docstring → --help description
# - Type validation → If age isn't a number, shows error
# - Beautiful formatting → Colored output, clean errors
# ============================================================
