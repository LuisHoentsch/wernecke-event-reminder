import hashlib
import os
from typing import List, Tuple

def custom_hash(s: str) -> str:
    """
    Generates a SHA-256 hash for a given string.

    Args:
        s (str): The input string.

    Returns:
        str: The hexadecimal hash string.
    """
    return hashlib.sha256(s.encode()).hexdigest()

def load_hashes(filepath: str) -> List[str]:
    """
    Loads event hashes from a file.

    Args:
        filepath (str): Path to the file.

    Returns:
        List[str]: A list of hashes.
    """
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.rstrip("\n") for line in f.readlines()]
    return []

def save_events(filepath: str, events: List[Tuple[str, str]]) -> None:
    """
    Prints events and saves their hashes to a file.

    Args:
        filepath (str): Path to the file.
        events (List[Tuple[str, str]]): List of events.
    """
    with open(filepath, "w") as f:
        for event in events:
            print(f"Event: {event[0]}, {event[1]}")
            f.write(str(custom_hash(event[0] + event[1])) + "\n")
