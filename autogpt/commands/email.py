from autogpt.config import Config
import smtplib
import email
import imaplib
from email.message import EmailMessage
from email.header import decode_header

CFG = Config()

sender = CFG.email_address
sender_pwd = CFG.email_password

def send_email(recipient: str, subject: str, message: str) -> str:
    """Send an email

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """
    host = CFG.email_smtp_host
    port = CFG.email_smtp_port


    if not sender or not sender_pwd:
        return f"Error: email not sent. EMAIL_ADDRESS or EMAIL_PASSWORD not set in environment."

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content(message)

    # send email
    with smtplib.SMTP(host, port) as smtp:
        smtp.starttls()
        smtp.login(sender, sender_pwd)
        smtp.send_message(msg)

def read_emails(imap_folder: str = "inbox", imap_search_command: str = "ALL") -> str:
    """Read emails

    Args:
        recipient (str): The email of the recipients
        subject (str): The subject of the email
        message (str): The message content of the email

    Returns:
        str: Any error messages
    """

    port = CFG.email_smtp_port
    imap_server = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(sender, sender_pwd)
    mail.select(imap_folder)
    _, search_data = mail.search(None, imap_search_command)

    messages = []
    for num in search_data[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                body = get_email_body(msg)
                messages.append((subject, body))

    mail.logout()
    return messages






def read_emails(email_address: str, password: str, imap_server: str = "imap.gmail.com", folder: str = "inbox", filter_by: str = "ALL") -> List[Tuple[str, str]]:



def get_email_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()



def read_emails(email_address: str, password: str, imap_server: str = "imap.gmail.com", folder: str = "inbox", filter_by: str = "ALL") -> List[Dict[str, str]]:
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)
    mail.select(folder)
    _, search_data = mail.search(None, filter_by)

    messages = []
    for num in search_data[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                body = get_email_body(msg)
                messages.append({"subject": subject, "body": body})

    mail.logout()
    return messages


def get_email_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
