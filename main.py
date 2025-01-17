import re
from datetime import datetime as dt

TAKE_NOTES = "Take notes on"
DELIMITER = "-"
my_path = "./clippings/My Clippings_0.2.txt"
book_to_filter = "Clean Architecture"


def clean_path(path) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]", DELIMITER, path).strip()


def save_to_md(clippings, filename, suffix):
    with open(
        f"./highlights/{clean_path(filename)}{DELIMITER}{suffix}.md", "w"
    ) as md_file:
        for _, clipping in enumerate(clippings):
            md_file.write(f"{clipping['highlight']}\n\n")


def extract_clipping(data):
    meta0 = data[0]
    br_pts0 = [i for i, x in enumerate(meta0) if x == "("]
    num_pages = ""
    location = ""
    entry_date = ""

    if len(br_pts0) == 0:
        book_title = meta0
        author = "Unknown"
    else:
        br0 = br_pts0[-1]
        book_title = meta0[:br0]
        author = meta0[br0 + 1 : -1]

        if "," in author:
            parts = author.split(",")
            author = parts[1][1:] + " " + parts[0]

        if ";" in author:
            author = author.split(";")

    meta1 = data[1].split("|")
    if len(meta1) == 3:
        num_pages = meta1[0][meta1[0].find("p") + 5 : -1]
        location = meta1[1][1:-1]
        br1 = meta1[2].find(",")
        entry_date = dt.strptime(meta1[2][br1 + 2 :], "%B %d, %Y %I:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif len(meta1) == 2:
        num_pages = "Unknown"
        location = meta1[0][meta1[0].find("on") + 3 : -1]
        br1 = meta1[1].find(",")
        entry_date = dt.strptime(meta1[1][br1 + 2 :], "%B %d, %Y %I:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    highlight = data[3]
    if highlight == "":
        highlight = f"{TAKE_NOTES} {location}!"

    return {
        "book_title": book_title,
        "author": author,
        "num_pages": num_pages,
        "location": location,
        "entry_date": entry_date,
        "highlight": highlight,
    }


with open(my_path, "r") as file:
    everything = file.read()
    everything = everything.replace("\ufeff", "")
    sections = everything.split("==========\n")

clippings_list = []
for i, clip in enumerate(sections[:-1]):
    data = clip.split("\n")
    extract = extract_clipping(data)
    clippings_list.append(extract)

filtered_clippings = []
filtered_notes = []
for i, clip in enumerate(clippings_list):
    if clip["book_title"].startswith(book_to_filter):
        if not clip["highlight"].startswith(TAKE_NOTES):
            filtered_clippings.append(clip)
        else:
            filtered_notes.append(clip)


save_to_md(filtered_clippings, book_to_filter, "highlights")
save_to_md(filtered_notes, book_to_filter, "notes")
