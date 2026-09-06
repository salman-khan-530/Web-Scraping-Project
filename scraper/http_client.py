"""
Reusable HTTP client with session management, rate limiting, and robots.txt compliance.
"""

import time
import requests

from scraper.config import (
    DEFAULT_TIMEOUT,
    REQUEST_DELAY,
    HEADERS
)
from scraper.logger import logger
from scraper.robots_checker import can_fetch


class HttpClient:
    """
    Reusable HTTP client encapsulating session, rate-limiting, and error handling.
    """

    def __init__(self, delay=REQUEST_DELAY, timeout=DEFAULT_TIMEOUT, check_robots=True):
        self.delay = delay
        self.timeout = timeout
        self.check_robots = check_robots
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.last_request_time = 0.0

    def fetch(self, url, params=None, timeout=None):
        """
        Fetch HTML content from a URL safely.

        Args:
            url (str): Target URL to fetch.
            params (dict, optional): URL query parameters.
            timeout (int, optional): Specific timeout in seconds.

        Returns:
            str or None: Webpage content if successful, None otherwise.
        """
        if not isinstance(url, str) or not url.strip():
            logger.error("URL must be a non-empty string.")
            return None

        url = url.strip()
        timeout = timeout or self.timeout

        # Check robots.txt compliance
        if self.check_robots and not can_fetch(url):
            logger.warning(f"Access denied by robots.txt: {url}")
            return None

        # Apply polite rate limiting delay
        if self.delay > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                sleep_duration = self.delay - elapsed
                logger.debug(f"Rate limiter: sleeping for {sleep_duration:.2f}s")
                time.sleep(sleep_duration)

        try:
            logger.info(f"Sending GET request: {url}")
            response = self.session.get(url, params=params, timeout=timeout)
            self.last_request_time = time.time()

            response.raise_for_status()
            logger.info(f"Response received [HTTP {response.status_code}] for {url}")
            return response.text

        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {timeout}s: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection failed for {url}: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception for {url}: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error fetching {url}: {e}")
            return None

    def close(self):
        """Close the underlying requests session."""
        self.session.close()


# Default singleton client for convenience
_default_client = HttpClient()


def fetch_page(url, timeout=DEFAULT_TIMEOUT, delay=REQUEST_DELAY, check_robots=True):
    """
    Convenience function to fetch a page using the default HTTP client.
    """
    if delay != _default_client.delay or check_robots != _default_client.check_robots:
        client = HttpClient(delay=delay, timeout=timeout, check_robots=check_robots)
        return client.fetch(url, timeout=timeout)

    return _default_client.fetch(url, timeout=timeout)