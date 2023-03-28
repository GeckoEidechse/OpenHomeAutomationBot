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


def check_if_fit_criteria(submission) -> bool:
    """
    Check if the given submission fits the criteria for cross-posting.

    :param submission: The submission to check.
    :type submission: praw.models.Submission
    :return: True if the submission fits the criteria, False otherwise.
    :rtype: bool
    """
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
    return False


def scrape_subreddit(
    reddit: praw.Reddit, subreddit_name: str = "homeautomation"
) -> List[praw.models.Submission]:
    """
    Scrape the given subreddit for relevant posts.

    :param reddit: The Reddit instance to use for the API requests.
    :type reddit: praw.Reddit
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
        if check_if_fit_criteria(submission)
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

    # Scrape posts and collect relevant ones
    submissions = scrape_subreddit(reddit)

    # Cross-post relevant posts
    crosspost_posts(reddit, submissions)


if __name__ == "__main__":
    main()
