import hashlib
import os

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup


def get_months(n=4):
    current_date = datetime.now()
    month_list = []
    for i in range(n):
        month_list.append((current_date + relativedelta(months=+i)).strftime('%Y%m'))
    return month_list


def get_content(url, month):
    response = requests.get(url + month)

    if response.status_code == 200:
        html_content = response.text
        return BeautifulSoup(html_content, 'html.parser')
    else:
        print(f"Failed to retrieve HTML: Status code {response.status_code}")


def get_events(soup):
    event_list = []
    for event in soup.find_all('div', class_='event cal_2 upcoming'):
        e = tuple(event.find('a').get('title')[:-1].rsplit(" (", 1))
        event_list.append(e)
    return event_list


def drop_twenclub_topten(events):
    return [event for event in events if "Twen-Club" != event[0] and "Top-Ten" != event[0]]


def custom_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()


def send_mail(events):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Email credentials
    sender_email = os.environ["SENDER_EMAIL"]
    receiver_email = os.environ["RECEIVER_EMAIL"]

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Neue Wernecke Events"

    body = ("\n\n".join([f"{event[0]}\n\t{event[1]}" for event in events]) + "\n\n\n\n"
            + "https://www.tanzschule-wernecke.de/veranstaltungen.html")
    message.attach(MIMEText(body, "plain"))

    # Connect to SMTP server
    server = smtplib.SMTP("mail.gmx.net", 587)
    server.starttls()  # Secure the connection
    server.login(sender_email, os.environ["EMAIL_PASSWORD"])

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Close SMTP server connection
    server.quit()


def main():
    print("Running script")

    # get all events from website
    events = []
    months = get_months(4)
    for month in months:
        soup = get_content('https://www.tanzschule-wernecke.de/veranstaltungen.html?month=', month)
        events += get_events(soup)
    events = drop_twenclub_topten(events)

    # load old events
    if os.path.exists("events.txt"):
        with open("events.txt", "r") as f:
            old_events_hashes = [line.rstrip("\n") for line in f.readlines()]
    else:
        old_events_hashes = []

    # check for new events
    new_events = [event for event in events if custom_hash(event[0] + event[1]) not in old_events_hashes]
    if new_events:
        print("New events found")
        send_mail(new_events)

    # save all events
    with open("events.txt", "w") as f:
        for event in events:
            f.write(str(custom_hash(event[0] + event[1])) + "\n")


if __name__ == "__main__":
    main()
