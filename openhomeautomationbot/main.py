import os
import json

from openhomeautomationbot.database_management import read_database, update_database
from openhomeautomationbot.filter import check_if_fit_criteria
from openhomeautomationbot.posting import crosspost_posts
from openhomeautomationbot import __version__
from typing import List
import logging
import praw



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
