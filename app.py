from flask import Flask, render_template, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# Email configuration
EMAIL_USER = os.getenv('EMAIL_USER', 'shubhamrahile31@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASS', 'kdax vvxm xecz entr')
PORT = int(os.getenv('PORT', 5000))

# Create SMTP transporter with better error handling
def create_smtp_transporter():
    """Create and return SMTP server connection"""
    try:
        print(f"Attempting to connect to SMTP server with user: {EMAIL_USER}")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        
        # Login with credentials
        try:
            server.login(EMAIL_USER, EMAIL_PASS)
            print("✓ Successfully logged in to SMTP server")
            return server
        except smtplib.SMTPAuthenticationError as auth_error:
            print(f"✗ SMTP Authentication Error: {auth_error}")
            print("Check your EMAIL_USER and EMAIL_PASS in .env file")
            return None
            
    except smtplib.SMTPConnectError as connect_error:
        print(f"✗ SMTP Connection Error: {connect_error}")
        return None
    except Exception as e:
        print(f"✗ General SMTP Error: {e}")
        return None

# Routes
@app.route('/')
def index():
    """Serve the main portfolio page"""
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style_css():
    """Serve CSS file"""
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def script_js():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/Shubham.jpeg')
def shubham_jpeg():
    """Serve profile image"""
    return send_from_directory('.', 'Shubham.jpeg')

@app.route('/Shubham Rahile CV.pdf')
def cv_pdf():
    """Serve CV PDF"""
    return send_from_directory('.', 'Shubham Rahile CV.pdf')

@app.route('/api/send-email', methods=['POST'])
def send_email():
    """Handle contact form submission and send email"""
    try:
        data = request.get_json()
        
        # Extract form data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Validation - check if all fields are provided
        if not name or not email or not subject or not message:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        # Email validation using regex
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return jsonify({
                'success': False,
                'message': 'Invalid email address'
            }), 400
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'"Portfolio Contact Form" <{EMAIL_USER}>'
        msg['To'] = EMAIL_USER
        msg['Reply-To'] = email
        msg['Subject'] = f'Portfolio Contact: {subject}'
        
        # Plain text version
        text_content = f"""
New Contact Form Submission

From: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio website contact form.
        """
        
        # HTML version with beautiful styling
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 650px; margin: 0 auto; padding: 30px; background: linear-gradient(135deg, #f0f4ff 0%, #e6f0ff 100%);">
    <!-- Header with Logo/Name -->
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 35px; border-radius: 15px 15px 0 0; text-align: center; box-shadow: 0 8px 25px rgba(79, 70, 229, 0.3);">
        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">📩 New Portfolio Message</h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 10px 0 0 0; font-size: 16px;">Shubham Rahile - Portfolio Contact</p>
    </div>
    
    <!-- Main Content -->
    <div style="background: white; padding: 40px; border-radius: 0 0 15px 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);">
        <!-- Sender Info -->
        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-left: 4px solid #4f46e5;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="background: #4f46e5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 18px;">👤</div>
                <h2 style="color: #1e293b; margin: 0; font-size: 22px;">New Message Received</h2>
            </div>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px; align-items: center; margin-bottom: 15px;">
                <div style="color: #64748b; font-weight: 600; min-width: 80px;">Name:</div>
                <div style="font-size: 18px; font-weight: 600; color: #1e293b;">{name}</div>
            </div>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px; align-items: center; margin-bottom: 15px;">
                <div style="color: #64748b; font-weight: 600; min-width: 80px;">Email:</div>
                <div>
                    <a href="mailto:{email}" style="color: #4f46e5; text-decoration: none; font-size: 16px; font-weight: 500;">{email}</a>
                    <span style="display: block; font-size: 13px; color: #94a3b8; margin-top: 3px;">Click to reply directly</span>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px; align-items: center;">
                <div style="color: #64748b; font-weight: 600; min-width: 80px;">Subject:</div>
                <div style="font-size: 16px; color: #334155; background: #e0e7ff; padding: 8px 15px; border-radius: 20px; display: inline-block;">{subject}</div>
            </div>
        </div>
        
        <!-- Message Content -->
        <div style="margin-bottom: 30px;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="background: #10b981; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 18px;">💬</div>
                <h3 style="color: #1e293b; margin: 0; font-size: 20px;">Message Content</h3>
            </div>
            
            <div style="background: #f1f5f9; border-radius: 12px; padding: 25px; border: 1px solid #e2e8f0;">
                <p style="margin: 0; color: #334155; line-height: 1.7; font-size: 16px; white-space: pre-wrap;">{message}</p>
            </div>
        </div>
        
        <!-- Action Footer -->
        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="margin: 0; color: #0369a1; font-size: 14px; font-weight: 500;">
                📝 This message was sent from your portfolio website contact form
            </p>
            <p style="margin: 8px 0 0 0; color: #64748b; font-size: 13px;">
                Reply directly to the sender's email address above
            </p>
        </div>
    </div>
    
    <!-- Footer -->
    <div style="text-align: center; margin-top: 25px; padding: 20px;">
        <p style="color: #64748b; font-size: 13px; margin: 0;">
            © 2026 Shubham Rahile. All rights reserved.
        </p>
        <p style="color: #94a3b8; font-size: 12px; margin: 5px 0 0 0;">
            Portfolio Contact System
        </p>
    </div>
</body>
</html>
        """
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        print(f"\n📧 Preparing to send email to: {EMAIL_USER}")
        print(f"From: {name} <{email}>")
        print(f"Subject: Portfolio Contact: {subject}\n")
        
        server = create_smtp_transporter()
        if server:
            try:
                print("Sending email...")
                server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())
                server.quit()
                print(f"✓ Email sent successfully from {email}")
                
                return jsonify({
                    'success': True,
                    'message': 'Message sent successfully!'
                }), 200
            except smtplib.SMTPRecipientsRefused as recipient_error:
                print(f"✗ Recipient Error: {recipient_error}")
                return jsonify({
                    'success': False,
                    'message': 'Invalid recipient email address'
                }), 500
            except smtplib.SMTPSenderRefused as sender_error:
                print(f"✗ Sender Error: {sender_error}")
                return jsonify({
                    'success': False,
                    'message': 'Sender email address refused'
                }), 500
            except Exception as send_error:
                print(f"✗ Error sending email: {send_error}")
                return jsonify({
                    'success': False,
                    'message': f'Failed to send message: {str(send_error)}'
                }), 500
        else:
            print("✗ Failed to create SMTP connection")
            return jsonify({
                'success': False,
                'message': 'Email server connection failed. Please check configuration.'
            }), 500
            
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'message': 'Flask server is running'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return send_from_directory('.', 'index.html'), 200

if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"🚀 Flask Portfolio Server Starting...")
    print(f"{'='*60}")
    print(f"📧 Email configured for: {EMAIL_USER}")
    print(f"🌐 Server will run on: http://localhost:{PORT}")
    print(f"{'='*60}\n")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=PORT)
