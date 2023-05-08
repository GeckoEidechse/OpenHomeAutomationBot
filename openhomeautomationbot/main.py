import os
import json
from openhomeautomationbot import __version__
from typing import List
import logging
import praw


def check_for_keywords(text: str) -> bool:
    """
    Check if the given text contains any of the predefined keywords.

    :param text: The text to check.
    :type text: str
    :return: True if the text contains any of the keywords, False otherwise.
    :rtype: bool
    """
    # TODO regex and list in extra file
    keywords = [
        "open source",
        "open-source",
        "open",
        "foss",
        "floss",
        "home assistant",
        "home-assistant",
        "homeassistant",
    ]
    # Check if text contains key words
    return any(keyword in text.lower() for keyword in keywords)


def check_if_fit_criteria(submission, latest_timestamp: float) -> bool:
    """
    Check if the given submission fits the criteria for cross-posting.

    :param submission: The submission to check.
    :type submission: praw.models.Submission
    :param latest_timestamp: The timestamp of the latest post in the database.
    :type latest_timestamp: float
    :return: True if the submission fits the criteria, False otherwise.
    :rtype: bool
    """
    # Get the contents of the title
    title = submission.title

    # Only consider new posts
    if submission.created_utc <= latest_timestamp:
        return False

    # First only check title
    if check_for_keywords(title):
        return True

    # Get the contents of the post or URL, depending on the type of submission
    if submission.is_self:
        content = submission.selftext
        if check_for_keywords(content):
            return True

    else:
        content = submission.url
        logging.warn("Content posts not yet supported")
    return False


def scrape_subreddit(
    reddit: praw.Reddit,
    latest_timestamp: float,
    subreddit_name: str = "homeautomation",
) -> List[praw.models.Submission]:
    """
    Scrape the given subreddit for relevant posts.

    :param reddit: The Reddit instance to use for the API requests.
    :type reddit: praw.Reddit
    :param latest_timestamp: The timestamp of the latest post in the database.
    :type latest_timestamp: float
    :param subreddit_name: The name of the subreddit to scrape, defaults to "homeautomation".
    :type subreddit_name: str, optional
    :return: A list of relevant submissions.
    :rtype: List[praw.models.Submission]
    """
    subreddit = reddit.subreddit(subreddit_name)

    # Get last x posts
    # TODO this should be based on timestamp since last visit instead
    results = [
        submission
        for submission in subreddit.new(limit=20)
        if check_if_fit_criteria(submission, latest_timestamp)
    ]

    return results


def crosspost_single_post(
    reddit: praw.Reddit,
    submission: praw.models.Submission,
    subreddit_name: str = "o_homeautomation_test",
):
    """
    Cross-post a single submission to the given subreddit.

    :param reddit: The Reddit instance to use for the API requests.
    :type reddit: praw.Reddit
    :param submission: The submission to cross-post.
    :type submission: praw.models.Submission
    :param subreddit_name: The name of the subreddit to cross-post to, defaults to "o_homeautomation_test".
    :type subreddit_name: str, optional
    """
    target_subreddit = reddit.subreddit(subreddit_name)
    crosspost_title = submission.title

    crosspost = submission.crosspost(
        subreddit=target_subreddit, title=crosspost_title, send_replies=True
    )

    logging.info(f"Crossposted to {crosspost.subreddit}: {crosspost.url}")


def crosspost_posts(reddit: praw.Reddit, submissions: List[praw.models.Submission]):
    """
    Crossposts a list of submissions to a target subreddit using the provided Reddit instance.

    Args:
        reddit (praw.Reddit): An instance of the Reddit class that is authenticated to the bot's account.
        submissions (List[praw.models.Submission]): A list of Submission objects to crosspost.

    Returns:
        None
    """
    for submission in submissions:
        # TODO double check if already posted
        crosspost_single_post(reddit, submission)
        break  # TODO only post single post for now

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

def main():
    """
    The main function of the openhomeautomationbot package.

    Authenticates to the bot's Reddit account, scrapes a subreddit for relevant posts,
    and crossposts them to a target subreddit.

    Returns:
        None
    """
    # Set log level
    logging.basicConfig(level=logging.INFO)

    logging.info("Hello, World!")
    logging.info(f"My package version is {__version__}")

    # authenticate using praw.ini
    reddit = praw.Reddit("openhomeautomationbot")

    # Read data from the database
    data = read_database()

    # Get the latest timestamp from the database
    latest_timestamp = data["latest_timestamp"]

    # Scrape posts and collect relevant ones
    submissions = scrape_subreddit(reddit, latest_timestamp)

    # Cross-post relevant posts
    crosspost_posts(reddit, submissions)

    # Add posts to database of past posts
    update_database(submissions)


if __name__ == "__main__":
    main()
