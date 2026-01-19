from scraper import get_months, get_content, get_events
from filter import drop_twenclub_topten
from storage import load_hashes, save_events, custom_hash
from notifier import send_mail

def main():
    """
    Main entry point for the event scraper script.
    """
    print("Running script")

    # get all events from website
    events = []
    months = get_months(4)
    for month in months:
        soup = get_content('https://www.tanzschule-wernecke.de/veranstaltungen.html?month=', month)
        events += get_events(soup)

    events = drop_twenclub_topten(events)

    # load old events
    events_file = "events.txt"
    old_events_hashes = load_hashes(events_file)

    # check for new events
    new_events = [event for event in events if custom_hash(event[0] + event[1]) not in old_events_hashes]

    if new_events:
        print("New events found")
        send_mail(new_events)
    else:
        print("No new events found")

    # save all events
    save_events(events_file, events)

if __name__ == "__main__":
    main()
