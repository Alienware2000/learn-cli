"""
Step 1: CLI Without a Framework

You CAN build CLIs with just sys.argv, but it's tedious.
Let's see why frameworks like Typer exist.
"""

import sys

print("=== Manual CLI Parsing ===\n")

# sys.argv is a list of command-line arguments
# argv[0] is the script name, argv[1:] are the arguments
print(f"sys.argv = {sys.argv}")
print(f"Script name: {sys.argv[0]}")
print(f"Arguments: {sys.argv[1:]}")

print("\n" + "="*50)

# Let's try to parse arguments manually
# Imagine we want: python script.py --name Alice --age 30

def parse_args():
    """Parse --name and --age from command line."""
    name = None
    age = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--name":
            if i + 1 < len(args):
                name = args[i + 1]
                i += 2
            else:
                print("Error: --name requires a value")
                sys.exit(1)
        elif args[i] == "--age":
            if i + 1 < len(args):
                try:
                    age = int(args[i + 1])
                except ValueError:
                    print("Error: --age must be a number")
                    sys.exit(1)
                i += 2
            else:
                print("Error: --age requires a value")
                sys.exit(1)
        elif args[i] == "--help":
            print("Usage: python step1_no_framework.py --name NAME --age AGE")
            sys.exit(0)
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    return name, age


name, age = parse_args()

if name and age:
    print(f"\nHello {name}, you are {age} years old!")
else:
    print("\nNo arguments provided.")
    print("Try: python step1_no_framework.py --name Alice --age 30")


print("\n" + "="*50)
print("PROBLEMS WITH MANUAL PARSING:")
print("="*50)
print()
print("1. So much code just for 2 arguments!")
print("2. No automatic --help generation")
print("3. Type conversion is manual (int(age))")
print("4. Error messages are inconsistent")
print("5. No validation built-in")
print("6. Adding new arguments = more spaghetti code")
print()
print("Typer solves all of this. See step2!")
