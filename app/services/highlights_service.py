import json
from bs4 import BeautifulSoup
import random
from app import Redis
import re


def handle_highlight(html):
    soup = BeautifulSoup(html, "html.parser")

    highlights = []
    note_texts = soup.find_all("div", {"class": "noteText"})
    note_headings = soup.find_all("div", {"class": "noteHeading"})

    for i in range(0, len(note_headings), 2):
        highlight = {}
        highlight["content"] = note_texts[i].text.strip()
        highlight["location"] = note_headings[i].text.strip().split(" - ")[-1]

        # Check if the next noteHeading is a Note for the current Highlight
        if i + 1 < len(note_headings) and "Note" in note_headings[i + 1].text:
            highlight["translation"] = note_texts[i + 1].text.strip()
        else:
            highlight["translation"] = None

        # remove all special syntax from the highlight content
        highlight["content"] = highlight["content"].replace("\n", " ").replace(">", " ")
        highlight["content"] = re.sub(" +", " ", highlight["content"])
        highlight["location"] = (
            highlight["location"].replace("\n", " ").replace(">", " ")
        )
        highlight["location"] = re.sub(" +", " ", highlight["location"])

        if highlight["translation"] is not None:
            highlight["translation"] = (
                highlight["translation"].replace("\n", " ").replace(">", " ")
            )
            highlight["translation"] = re.sub(" +", " ", highlight["translation"])

        highlights.append(highlight)

    # convert highlights list to JSON string
    highlights_json = json.dumps(highlights)

    # save the JSON string to Redis
    Redis.set("highlights", highlights_json)

    # get random 6 highlights from the highlights_by_section
    random_highlights = random.sample(highlights, 6)

    return random_highlights
