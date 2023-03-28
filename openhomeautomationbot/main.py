from openhomeautomationbot import __version__
from typing import List
import logging
import praw

def check_for_keywords(text: str) -> bool:
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


def check_if_fit_criteria(submission) -> bool:

    # Get the contents of the title
    title = submission.title

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
    False

def scrape_subreddit(reddit, subreddit_name="homeautomation")-> List[praw.models.Submission]:
    subreddit = reddit.subreddit(subreddit_name)

    # Get last x posts
    # TODO this should be based on timestamp since last visit instead
    results = [submission for submission in subreddit.new(limit=20) if check_if_fit_criteria(submission)]

    return results

def crosspost_single_post(reddit: praw.Reddit, submission: praw.models.Submission, subreddit_name="o_homeautomation_test"):
    target_subreddit = reddit.subreddit(subreddit_name)
    crosspost_title = submission.title

    crosspost = submission.crosspost(subreddit=target_subreddit, title=crosspost_title, send_replies=True)

    logging.info(f"Crossposted to {crosspost.subreddit}: {crosspost.url}")

def crosspost_posts(reddit: praw.Reddit, submissions: List[praw.models.Submission]):
    for submission in submissions:
        # TODO double check if already posted
        crosspost_single_post(reddit, submission)
        break # TODO only post single post for now

def main():
    # Set log level
    logging.basicConfig(level=logging.INFO)

    logging.info("Hello, World!")
    logging.info(f"My package version is {__version__}")

    # authenticate using praw.ini
    reddit = praw.Reddit("openhomeautomationbot")

    # Scrape posts and collect relevant ones
    submissions = scrape_subreddit(reddit)

    # Cross-post relevant posts
    crosspost_posts(reddit, submissions)

if __name__ == "__main__":
    main()
