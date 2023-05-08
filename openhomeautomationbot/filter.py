import logging
from newspaper import Article, ArticleException

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
