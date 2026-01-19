# Wernecke Events Scraper

This script scrapes the Tanzschule Wernecke website for upcoming events, filters out specific ones, and sends an email notification if new events are found.

## Project Structure

The project is structured as follows:

```
.
├── src/
│   ├── main.py       # Entry point
│   ├── scraper.py    # Logic for fetching and parsing the website
│   ├── filter.py     # Logic for filtering events
│   ├── storage.py    # Logic for loading/saving event hashes
│   └── notifier.py   # Logic for sending email notifications
├── events.txt        # Stores hashes of known events (created on first run)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Installation

1.  **Clone the repository**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script using Python:

```bash
python src/main.py
```

## Environment Variables

To enable email notifications, you must set the following environment variables:

*   `SENDER_EMAIL`: The email address sending the notifications.
*   `RECEIVER_EMAIL`: The email address receiving the notifications.
*   `EMAIL_PASSWORD`: The password (or app password) for the sender email account.

Example:

```bash
export SENDER_EMAIL="your_email@gmx.de"
export RECEIVER_EMAIL="receiver@example.com"
export EMAIL_PASSWORD="your_password"
python src/main.py
```

## How it Works

1.  **Scraping**: It fetches event pages for the next 4 months.
2.  **Filtering**: It removes events starting with "Twen-Club" or "Top-Ten".
3.  **Comparison**: It compares found events against `events.txt` using SHA-256 hashes.
4.  **Notification**: If new events are found, it sends an email via SMTP (GMX).
5.  **Persistence**: It updates `events.txt` with current event hashes.
