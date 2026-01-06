"""
Step 3: Arguments vs Options

In CLIs:
- Arguments are positional: `greet Alice`
- Options use flags: `greet --name Alice` or `greet -n Alice`

Run with:
    python step3_options.py --help
    python step3_options.py --name Alice
    python step3_options.py --name Alice --greeting "Good morning"
    python step3_options.py -n Bob -g "Hey there"
    python step3_options.py --name Alice --loud
"""

from typing import Annotated
import typer


def main(
    # Option with short flag (-n)
    name: Annotated[str, typer.Option("--name", "-n", help="The person to greet")] = "World",

    # Option with default
    greeting: Annotated[str, typer.Option("--greeting", "-g", help="The greeting to use")] = "Hello",

    # Boolean flag (no value needed)
    loud: Annotated[bool, typer.Option("--loud", "-l", help="Greet loudly")] = False,

    # Number with validation
    times: Annotated[int, typer.Option("--times", "-t", help="Times to repeat", min=1, max=10)] = 1,
):
    """
    Greet someone with customizable options.
    """
    message = f"{greeting}, {name}!"

    if loud:
        message = message.upper()

    for _ in range(times):
        print(message)


if __name__ == "__main__":
    typer.run(main)


# ============================================================
# KEY CONCEPTS:
#
# 1. Annotated[type, typer.Option(...)]
#    This is how you define options (flags)
#
# 2. typer.Option("--long", "-s", help="...")
#    - First arg: long form (--name)
#    - Second arg: short form (-n)
#    - help: description for --help
#
# 3. Boolean options
#    bool with default False → flag that sets it True
#    --loud means loud=True
#
# 4. Validation
#    min=1, max=10 → enforced automatically
# ============================================================
