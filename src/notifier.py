import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Tuple

def send_mail(events: List[Tuple[str, str]]):
    """
    Sends an email with the list of new events.

    Args:
        events (List[Tuple[str, str]]): List of new events.
    """
    # Email credentials
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_host = os.environ.get("EMAIL_HOST")
    email_port = os.environ.get("EMAIL_PORT")

    if not sender_email or not receiver_email or not email_password or not email_host:
        print("Missing email environment variables (SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD, EMAIL_HOST). Skipping email.")
        return
    if not email_port:
        email_port = 587

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Neue Wernecke Events"

    body = ("\n\n".join([f"{event[0]}\n\t{event[1]}" for event in events]) + "\n\n\n\n"
            + "https://www.tanzschule-wernecke.de/veranstaltungen.html")
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, email_password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Close SMTP server connection
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
