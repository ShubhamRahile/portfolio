"""
Test Email Configuration Script
Run this to verify your email settings are working correctly
"""

import smtplib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER', 'shubhamrahile31@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASS', 'kdax vvxm xecz entr')

print("="*60)
print("Testing Email Configuration")
print("="*60)
print(f"\nEmail User: {EMAIL_USER}")
print(f"Email Pass: {'*' * len(EMAIL_PASS)} (hidden for security)")
print(f"Password length: {len(EMAIL_PASS)} characters")
print("\nAttempting to connect to Gmail SMTP server...\n")

try:
    # Create SMTP connection
    print("Step 1: Connecting to smtp.gmail.com:587...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    print("✓ Connection successful\n")
    
    print("Step 2: Starting TLS encryption...")
    server.starttls()
    print("✓ TLS started successfully\n")
    
    print("Step 3: Attempting login...")
    try:
        server.login(EMAIL_USER, EMAIL_PASS)
        print("✓ Login successful!\n")
        
        print("="*60)
        print("✅ EMAIL CONFIGURATION IS WORKING!")
        print("="*60)
        print("\nYour Gmail App Password is correct.")
        print("The contact form should work properly now.\n")
        
        server.quit()
        
    except smtplib.SMTPAuthenticationError as e:
        print("✗ Authentication FAILED!\n")
        print("="*60)
        print("❌ EMAIL CONFIGURATION ERROR")
        print("="*60)
        print("\nPossible issues:")
        print("1. The App Password is incorrect")
        print("2. You need to enable 2-Step Verification in Google Account")
        print("3. You need to generate a new App Password")
        print("\nTo fix:")
        print("1. Go to: https://myaccount.google.com/security")
        print("2. Enable 2-Step Verification")
        print("3. Go to: https://myaccount.google.com/apppasswords")
        print("4. Generate a new App Password for 'Mail'")
        print("5. Update .env file with the new password")
        print(f"\nError details: {e}\n")
        
except smtplib.SMTPConnectError as e:
    print("✗ Connection FAILED!\n")
    print(f"Error: {e}")
    print("\nPossible issues:")
    print("1. Internet connection problem")
    print("2. Gmail SMTP server is down")
    print("3. Firewall blocking port 587\n")
    
except Exception as e:
    print("✗ Unexpected error occurred!\n")
    print(f"Error: {e}\n")

print("="*60)
input("\nPress Enter to exit...")
