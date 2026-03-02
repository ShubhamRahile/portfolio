const nodemailer = require('nodemailer');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { name, email, subject, message } = req.body;

  // Validation
  if (!name || !email || !subject || !message) {
    return res.status(400).json({
      success: false,
      message: 'All fields are required'
    });
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({
      success: false,
      message: 'Invalid email address'
    });
  }

  // Create transporter
  const transporter = nodemailer.createTransporter({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    }
  });

  // Email options
  const mailOptions = {
    from: `"Portfolio Contact Form" <${process.env.EMAIL_USER}>`,
    to: process.env.EMAIL_USER,
    replyTo: email,
    subject: `Portfolio Contact: ${subject}`,
    html: `
      <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 650px; margin: 0 auto; padding: 30px; background: linear-gradient(135deg, #f0f4ff 0%, #e6f0ff 100%);">
        <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 35px; border-radius: 15px 15px 0 0; text-align: center; box-shadow: 0 8px 25px rgba(79, 70, 229, 0.3);">
          <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">📩 New Portfolio Message</h1>
          <p style="color: rgba(255, 255, 255, 0.9); margin: 10px 0 0 0; font-size: 16px;">Shubham Rahile - Portfolio Contact</p>
        </div>
        
        <div style="background: white; padding: 40px; border-radius: 0 0 15px 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);">
          <div style="background: #f8fafc; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-left: 4px solid #4f46e5;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
              <div style="background: #4f46e5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 18px;">👤</div>
              <h2 style="color: #1e293b; margin: 0; font-size: 22px;">New Message Received</h2>
            </div>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px; align-items: center; margin-bottom: 15px;">
              <div style="color: #64748b; font-weight: 600; min-width: 80px;">Name:</div>
              <div style="font-size: 18px; font-weight: 600; color: #1e293b;">${name}</div>
            </div>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px; align-items: center; margin-bottom: 15px;">
              <div style="color: #64748b; font-weight: 600; min-width: 80px;">Email:</div>
              <div>
                <a href="mailto:${email}" style="color: #4f46e5; text-decoration: none; font-size: 16px; font-weight: 500;">${email}</a>
                <span style="display: block; font-size: 13px; color: #94a3b8; margin-top: 3px;">Click to reply directly</span>
              </div>
            </div>
            
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 15px; align-items: center;">
              <div style="color: #64748b; font-weight: 600; min-width: 80px;">Subject:</div>
              <div style="font-size: 16px; color: #334155; background: #e0e7ff; padding: 8px 15px; border-radius: 20px; display: inline-block;">${subject}</div>
            </div>
          </div>
          
          <div style="margin-bottom: 30px;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
              <div style="background: #10b981; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 18px;">💬</div>
              <h3 style="color: #1e293b; margin: 0; font-size: 20px;">Message Content</h3>
            </div>
            
            <div style="background: #f1f5f9; border-radius: 12px; padding: 25px; border: 1px solid #e2e8f0;">
              <p style="margin: 0; color: #334155; line-height: 1.7; font-size: 16px; white-space: pre-wrap;">${message}</p>
            </div>
          </div>
          
          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 20px; text-align: center;">
            <p style="margin: 0; color: #0369a1; font-size: 14px; font-weight: 500;">
              📝 This message was sent from your portfolio website contact form
            </p>
            <p style="margin: 8px 0 0 0; color: #64748b; font-size: 13px;">
              Reply directly to the sender's email address above
            </p>
          </div>
        </div>
        
        <div style="text-align: center; margin-top: 25px; padding: 20px;">
          <p style="color: #64748b; font-size: 13px; margin: 0;">
            © 2026 Shubham Rahile. All rights reserved.
          </p>
          <p style="color: #94a3b8; font-size: 12px; margin: 5px 0 0 0;">
            Portfolio Contact System
          </p>
        </div>
      </div>
    `,
    text: `
New Contact Form Submission

From: ${name}
Email: ${email}
Subject: ${subject}

Message:
${message}

---
This message was sent from your portfolio website contact form.
    `
  };

  try {
    await transporter.sendMail(mailOptions);
    console.log(`✓ Email sent successfully from ${email}`);
    
    res.status(200).json({
      success: true,
      message: 'Message sent successfully!'
    });
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to send message. Please try again later.'
    });
  }
}