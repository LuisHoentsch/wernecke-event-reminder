from typing import List, Tuple

def drop_twenclub_topten(events: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Filters out 'Twen-Club' and 'Top-Ten' events.

    Args:
        events (List[Tuple[str, str]]): List of events.

    Returns:
        List[Tuple[str, str]]: Filtered list of events.
    """
    return [event for event in events if "Twen-Club - Tanzparty für Erwachsene" != event[0] and "Top-Ten - Übungsparty für Jugendliche" != event[0]]
