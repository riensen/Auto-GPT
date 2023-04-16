import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()


def send_email(recipient: str, subject: str, message: str):
    """Send an email

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email
    """
    sender = os.environ.get("EMAIL_ADDRESS")
    sender_pwd = os.environ.get("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content(message)

# send email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, sender_pwd)
        smtp.send_message(msg)
