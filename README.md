# Wernecke Events Scraper

This script scrapes the _Tanzschule Wernecke_ website for upcoming events, filters out recurrent ones, and sends an email notification if new events are found. Automated via GitHub Actions.

## Environment Variables

To enable email notifications, you must set the following environment variables:

*   `SENDER_EMAIL`: The email address sending the notifications.
*   `RECEIVER_EMAIL`: The email address receiving the notifications.
*   `EMAIL_PASSWORD`: The password (or app password) for the sender email account.
*   `EMAIL_HOST`: The email providers SMTP hostname.
*   `EMAIL_PORT`: The email providers SMTP port. Optional, default: 587.


## How it Works

1.  **Scraping**: Fetch event pages for the next 4 months.
2.  **Filtering**: Remove recurrent events.
3.  **Comparison**: Compare found events against `events.txt` (using hashes).
4.  **Notification**: If new events are found, send an email via SMTP.
5.  **Persistence**: Update `events.txt` with current event hashes.
