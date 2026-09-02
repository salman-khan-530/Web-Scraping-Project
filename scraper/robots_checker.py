from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

from scraper.logger import logger


def can_fetch(
    target_url,
    user_agent="*"
):
    """
    Check whether a URL is allowed by robots.txt.

    The website domain is automatically detected
    from the target URL.

    Args:
        target_url (str): URL we want to access.
        user_agent (str): User-agent to check.

    Returns:
        bool: True if crawling is allowed.
        False otherwise.
    """

    try:

        # Extract website information
        parsed_url = urlparse(
            target_url
        )

        # Validate URL
        if not parsed_url.scheme or not parsed_url.netloc:

            logger.error(
                f"Invalid URL: {target_url}"
            )

            return False

        # Build website base URL
        base_url = (
            f"{parsed_url.scheme}://"
            f"{parsed_url.netloc}"
        )

        # Build robots.txt URL
        robots_url = urljoin(
            base_url,
            "/robots.txt"
        )

        logger.info(
            f"Checking robots.txt: "
            f"{robots_url}"
        )

        # Create robots.txt parser
        robot_parser = RobotFileParser()

        robot_parser.set_url(
            robots_url
        )

        # Read robots.txt
        robot_parser.read()

        # Check crawling permission
        allowed = robot_parser.can_fetch(
            user_agent,
            target_url
        )

        if allowed:

            logger.info(
                f"robots.txt allows access: "
                f"{target_url}"
            )

        else:

            logger.warning(
                f"robots.txt disallows access: "
                f"{target_url}"
            )

        return allowed

    except Exception as e:

        logger.error(
            f"Could not read robots.txt: {e}"
        )

        return False