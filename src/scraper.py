from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional

def get_months(n: int = 4) -> List[str]:
    """
    Generates a list of months in 'YYYYMM' format starting from the current month.

    Args:
        n (int): Number of months to generate. Defaults to 4.

    Returns:
        List[str]: A list of month strings.
    """
    current_date = datetime.now()
    month_list = []
    for i in range(n):
        month_list.append((current_date + relativedelta(months=+i)).strftime('%Y%m'))
    return month_list

def get_content(url: str, month: str) -> Optional[BeautifulSoup]:
    """
    Fetches the HTML content from the given URL for a specific month.

    Args:
        url (str): The base URL.
        month (str): The month string.

    Returns:
        Optional[BeautifulSoup]: The parsed HTML content, or None if the request failed.
    """
    try:
        response = requests.get(url + month)
        if response.status_code == 200:
            html_content = response.text
            return BeautifulSoup(html_content, 'html.parser')
        else:
            print(f"Failed to retrieve HTML: Status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching content: {e}")
        return None

def get_events(soup: Optional[BeautifulSoup]) -> List[Tuple[str, str]]:
    """
    Parses events from the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        List[Tuple[str, str]]: A list of events, where each event is a tuple (title, date/details).
    """
    if not soup:
        return []

    event_list = []
    for event in soup.find_all('div', class_='event cal_2 upcoming'):
        link = event.find('a')
        if link and link.get('title'):
            try:
                # Extracts title and details from the title attribute formatted as "Name (Details)"
                e = tuple(link.get('title')[:-1].rsplit(" (", 1))
                event_list.append(e)
            except Exception:
                continue
    return event_list
