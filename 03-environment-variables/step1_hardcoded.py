"""
Step 1: The Problem - Hardcoded Secrets

Look at this code. Can you spot the problem?
"""

# THIS IS BAD - DO NOT DO THIS IN REAL CODE!
API_KEY = "my-super-secret-api-key-DONT-DO-THIS"

print("=== The Problem with Hardcoded Secrets ===\n")

print(f"API Key: {API_KEY}")
print()

print("Why is this bad?")
print()
print("1. VERSION CONTROL")
print("   If you commit this to Git, your secret is in the history FOREVER")
print("   Even if you delete it later, it's still in old commits")
print()
print("2. SHARING CODE")
print("   You can't share your code without sharing your secret")
print("   Can't post to GitHub, can't send to a friend")
print()
print("3. DIFFERENT ENVIRONMENTS")
print("   Development vs Production might need different keys")
print("   You'd have to edit code to switch")
print()
print("4. SECURITY")
print("   Anyone who sees your code sees your secret")
print("   Hackers scan GitHub for exposed API keys!")
print()

print("="*50)
print("THE SOLUTION: Environment Variables")
print()
print("Store secrets OUTSIDE your code:")
print("- In your shell: export API_KEY=sk-ant-xxx")
print("- In a .env file (not committed to git)")
print("- In your hosting platform's settings")
print("="*50)
