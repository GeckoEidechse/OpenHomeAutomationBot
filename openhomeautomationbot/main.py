import os
import json

from openhomeautomationbot.database_management import read_database, update_database
from openhomeautomationbot.scraping import scrape_subreddit
from openhomeautomationbot.posting import crosspost_posts
from openhomeautomationbot import __version__
import logging
import praw


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
