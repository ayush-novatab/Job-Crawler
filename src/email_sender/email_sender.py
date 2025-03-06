import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import Config

def send_email(new_jobs):
    sender_email = Config.EMAIL_SENDER
    password = Config.EMAIL_PASSWORD
    recipient_email = Config.EMAIL_RECIPIENT

    msg = MIMEMultipart()
    msg["Subject"] = "🔥 New Job Alerts!"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    body = "New job openings:\n\n"
    for job in new_jobs:
        body += f"📢 {job['title']} at {job['company']}\n📍 {job['location']}\n🔗 Apply here: {job['url']}\n\n"

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)