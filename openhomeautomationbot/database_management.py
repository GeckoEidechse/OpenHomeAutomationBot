import json
import os

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
