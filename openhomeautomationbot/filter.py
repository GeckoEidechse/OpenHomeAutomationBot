import logging
from newspaper import Article, ArticleException
import re

def check_for_keywords(text: str) -> bool:
    """
    Check if the given text contains any of the predefined keywords or patterns.

    :param text: The text to check.
    :type text: str
    :return: True if the text contains any of the keywords or patterns, False otherwise.
    :rtype: bool
    """
    patterns = [
        r"\bopen[ -]?source\b",
        r"\bopen[ -]?hardware\b",
        r"\bfoss\b",
        r"\bfloss\b",
        r"\bhome[ -]?assistant\b",
    ]
    # Check if text contains key patterns
    text = text.lower()
    return any(re.search(pattern, text) for pattern in patterns)


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
        # Link post
        content_url = submission.url
        # Attempt parsing link content
        try:
            article = Article(content_url)
            article.download()
            article.parse()
            content = article.text

            if check_for_keywords(content):
                return True

        except ArticleException as e:
            logging.warn("Failed to extract content from the link: %s" % content_url)
            logging.exception(e)

    return False
