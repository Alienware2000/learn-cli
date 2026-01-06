"""
Step 3: Using .env Files with python-dotenv

Typing 'export VAR=value' every time is annoying.
A .env file stores your variables in a file that:
- Loads automatically
- Is NOT committed to git (add to .gitignore!)
- Is easy to edit
"""

import os
from dotenv import load_dotenv

print("=== Before Loading .env ===\n")
print(f"TASK_CLI_API_KEY = {os.environ.get('TASK_CLI_API_KEY', 'Not set')}")
print(f"TASK_CLI_MODEL = {os.environ.get('TASK_CLI_MODEL', 'Not set')}")

# Load variables from .env file into environment
# This looks for a file called ".env" in the current directory
load_dotenv()

print("\n=== After Loading .env ===\n")
print(f"TASK_CLI_API_KEY = {os.environ.get('TASK_CLI_API_KEY', 'Not set')}")
print(f"TASK_CLI_MODEL = {os.environ.get('TASK_CLI_MODEL', 'Not set')}")


print("\n" + "="*50)
print("HOW IT WORKS")
print("="*50)
print()
print("1. Create a file called '.env' (note the dot!)")
print()
print("2. Add your variables, one per line:")
print("   TASK_CLI_API_KEY=sk-ant-your-key-here")
print("   TASK_CLI_MODEL=claude-sonnet-4-5-20250929")
print()
print("3. In your code:")
print("   from dotenv import load_dotenv")
print("   load_dotenv()  # Loads .env into os.environ")
print()
print("4. Add .env to .gitignore so it's never committed!")
print()
print("="*50)
print()
print("There's a .env file in this folder for you to try.")
print("Edit it with your own values and run this again!")
