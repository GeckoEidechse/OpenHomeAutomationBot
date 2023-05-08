import logging
import praw
from typing import List


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
