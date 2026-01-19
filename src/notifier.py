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

    if not sender_email or not receiver_email or not email_password:
        print("Missing email environment variables (SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD). Skipping email.")
        return

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
        server = smtplib.SMTP("mail.gmx.net", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, email_password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Close SMTP server connection
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
