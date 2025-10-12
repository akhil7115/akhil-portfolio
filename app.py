from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Save to file
        save_contact_data(name, email, message)
        
        # Send email (optional)
        # send_email(name, email, message)
        
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

def save_contact_data(name, email, message):
    """Save contact form data to a text file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open('contact_messages.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Date: {timestamp}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Message: {message}\n")
        f.write(f"{'='*50}\n")

def send_email(name, email, message):
    """Send email notification (configure with your email)"""
    try:
        # Email configuration (update with your details)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"  # Your email
        sender_password = "your-app-password"   # Your app password
        receiver_email = "akhil.shuklathus547@gmail.com"  # Your email
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"New Contact Form Submission from {name}"
        
        body = f"""
        New contact form submission:
        
        Name: {name}
        Email: {email}
        Message: {message}
        
        Sent from your portfolio website.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
    except Exception as e:
        print(f"Email sending failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)