from typing import List
import praw

from openhomeautomationbot.filter import check_if_fit_criteria

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
