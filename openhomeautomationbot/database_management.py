import json
import os
import praw
from typing import List

def read_database(database_file: str = "database.json") -> dict:
    """
    Reads the data from the JSON database file and returns it as a dictionary.

    Args:
        database_file (str, optional): The path to the database file. Defaults to "database.json".

    Returns:
        dict: A dictionary containing the data from the database file.
    """
    if os.path.exists(database_file):
        with open(database_file, "r") as f:
            data = json.load(f)
    else:
        data = {"posts": {}, "latest_timestamp": 0}

    return data

def update_database(submissions: List[praw.models.Submission]):
    """
    Stores the list of newly posted posts in a database (just a JSON file)

    Args:
        submissions (List[praw.models.Submission]): A list of Submission objects to crosspost.

    Returns:
        None
    """
    database_file = "database.json"

    # Load existing data from the database file
    if os.path.exists(database_file):
        with open(database_file, "r") as f:
            data = json.load(f)
    else:
        data = {"posts": {}, "latest_timestamp": 0}

    # Add new submissions to the data
    for submission in submissions:
        entry = {
            "title": submission.title,
            "url": submission.url,
            "created_utc": submission.created_utc,
        }
        data["posts"][submission.id] = entry

        # Update the latest timestamp if the current submission has a newer timestamp
        if submission.created_utc > data["latest_timestamp"]:
            data["latest_timestamp"] = submission.created_utc

        # Add version field
        data["version"] = 1

    # Write updated data back to the database file
    with open(database_file, "w") as f:
        json.dump(data, f, indent=4)
