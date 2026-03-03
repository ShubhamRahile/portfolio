"""
Quick script to check what's in .env file
"""
from dotenv import load_dotenv
import os

load_dotenv()

print("Environment Variables:")
print(f"EMAIL_USER: {os.getenv('EMAIL_USER', 'NOT SET')}")
print(f"EMAIL_PASS: {os.getenv('EMAIL_PASS', 'NOT SET')}")
print(f"PORT: {os.getenv('PORT', 'NOT SET')}")

# Try reading .env file directly
print("\nReading .env file directly:")
with open('.env', 'r') as f:
    content = f.read()
    print(content)
