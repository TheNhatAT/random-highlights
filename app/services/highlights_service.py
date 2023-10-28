import json
from bs4 import BeautifulSoup
import random
from app import Redis


def handle_highlight():
    with open(
        "./data/James Clear - Atomic Habits_ Tiny Changes, Remarkable Results-Penguin Publishing Group (2018) - Notebook.html",
        "r",
        encoding="utf-8",
    ) as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    highlights = []
    for note_heading in soup.find_all("div", {"class": "noteHeading"}):
        highlight_text = note_heading.find_next_sibling("div", {"class": "noteText"})
        location = note_heading.text.strip().split(" - ")[-1]
        highlights.append(
            {"content": highlight_text.text.strip(), "location": location}
        )

    # convert highlights list to JSON string
    highlights_json = json.dumps(highlights)

    # save the JSON string to Redis
    Redis.set("highlights", highlights_json)

    # get random 6 highlights from the list
    highlights = random.sample(highlights, 6)

    return highlights
