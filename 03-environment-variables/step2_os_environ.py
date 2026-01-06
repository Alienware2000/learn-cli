"""
Step 2: Reading Environment Variables with os.environ

Environment variables are values stored in your shell/system,
NOT in your code. Your code reads them at runtime.
"""

import os

print("=== Reading Environment Variables ===\n")

# Method 1: os.environ.get() - Returns None if not set
api_key = os.environ.get("MY_API_KEY")
print(f"MY_API_KEY = {api_key}")
print("  (None because we haven't set it yet)\n")

# Method 2: os.environ.get() with a default
api_key = os.environ.get("MY_API_KEY", "default-value")
print(f"MY_API_KEY with default = {api_key}\n")

# Method 3: os.environ[] - Raises error if not set
print("Trying os.environ['MY_API_KEY'] (without .get()):")
try:
    api_key = os.environ["MY_API_KEY"]
except KeyError:
    print("  KeyError! The variable doesn't exist.\n")


print("=== Some Variables That DO Exist ===\n")

# These are standard environment variables on most systems
print(f"USER = {os.environ.get('USER', 'unknown')}")
print(f"HOME = {os.environ.get('HOME', 'unknown')}")
print(f"PATH = {os.environ.get('PATH', 'unknown')[:50]}...")  # Truncated


print("\n" + "="*50)
print("HOW TO SET ENVIRONMENT VARIABLES")
print("="*50)
print()
print("Option 1: In your terminal (temporary, for this session)")
print("  $ export MY_API_KEY=sk-ant-xxx")
print("  $ python step2_os_environ.py")
print()
print("Option 2: Inline when running (temporary, for this command)")
print("  $ MY_API_KEY=sk-ant-xxx python step2_os_environ.py")
print()
print("Option 3: In a .env file (see step3!)")
print()
print("Try it! Run this in your terminal:")
print("  MY_API_KEY=test-123 python step2_os_environ.py")
