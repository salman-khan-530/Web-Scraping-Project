import time

import requests

from scraper.config import (
    DEFAULT_TIMEOUT,
    REQUEST_DELAY,
    HEADERS
)

from scraper.logger import logger

from scraper.robots_checker import can_fetch


# Create a reusable HTTP session
session = requests.Session()

session.headers.update(
    HEADERS
)


def fetch_page(
    url,
    timeout=DEFAULT_TIMEOUT
):
    """
    Fetch HTML content from a webpage.

    Before making the request, robots.txt is checked
    to determine whether the URL can be accessed.

    A request delay is also applied to avoid sending
    requests too quickly.

    Args:
        url (str): Webpage URL.
        timeout (int): Request timeout in seconds.

    Returns:
        str: HTML content if the request succeeds.
        None: If the request fails or access is not allowed.
    """

    try:

        # Validate URL
        if not url:

            logger.error(
                "Cannot fetch an empty URL."
            )

            return None

        # Check robots.txt permission
        if not can_fetch(url):

            logger.warning(
                f"Access blocked by robots.txt: "
                f"{url}"
            )

            return None

        # Respect request delay
        time.sleep(
            REQUEST_DELAY
        )

        # Send HTTP request
        response = session.get(
            url,
            timeout=timeout
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        logger.info(
            f"Request successful: "
            f"{response.status_code} - {url}"
        )

        return response.text

    except requests.exceptions.Timeout:

        logger.error(
            f"Request timed out: {url}"
        )

    except requests.exceptions.ConnectionError:

        logger.error(
            f"Connection error: {url}"
        )

    except requests.exceptions.HTTPError as e:

        logger.error(
            f"HTTP error: {e}"
        )

    except requests.exceptions.RequestException as e:

        logger.error(
            f"Request error: {e}"
        )

    return None