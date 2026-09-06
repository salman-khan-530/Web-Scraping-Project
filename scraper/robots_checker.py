"""
Robots.txt compliance checker with caching.
"""

from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import requests

from scraper.config import DEFAULT_TIMEOUT, HEADERS
from scraper.logger import logger

# Cache for RobotFileParser instances by netloc (domain)
_robots_cache = {}


def get_robot_parser(target_url, timeout=DEFAULT_TIMEOUT):
    """
    Retrieve or initialize a cached RobotFileParser for the URL's domain.

    Args:
        target_url (str): Target URL to inspect.
        timeout (int): Network timeout for fetching robots.txt.

    Returns:
        RobotFileParser or None: Parsed robots rules, or None if network/URL error.
    """
    if not isinstance(target_url, str) or not target_url.strip():
        return None

    parsed_url = urlparse(target_url.strip())
    if not parsed_url.scheme or not parsed_url.netloc:
        return None

    domain_key = f"{parsed_url.scheme}://{parsed_url.netloc}"
    if domain_key in _robots_cache:
        return _robots_cache[domain_key]

    robots_url = urljoin(domain_key, "/robots.txt")
    logger.info(f"Fetching and parsing robots.txt: {robots_url}")

    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = requests.get(
            robots_url,
            headers=HEADERS,
            timeout=timeout
        )

        if response.status_code == 200:
            parser.parse(response.text.splitlines())
            _robots_cache[domain_key] = parser
            logger.info(f"Successfully loaded robots.txt for {domain_key}")
            return parser
        elif response.status_code in (404, 410):
            # Per RFC 9309 (Robots Exclusion Protocol), a 404/410 means no restrictions exist
            parser.parse([])
            _robots_cache[domain_key] = parser
            logger.info(f"No robots.txt found ({response.status_code}); unrestricted access allowed for {domain_key}")
            return parser
        else:
            # Conservative/fail-closed: Disallow when server returns 401, 403, 5xx
            logger.warning(
                f"robots.txt returned HTTP {response.status_code} for {domain_key}. "
                f"Applying conservative fail-closed policy."
            )
            parser.parse(["User-agent: *", "Disallow: /"])
            _robots_cache[domain_key] = parser
            return parser

    except requests.exceptions.RequestException as e:
        logger.error(
            f"Could not fetch robots.txt for {domain_key} ({e}). "
            f"Applying conservative fail-closed policy."
        )
        # Conservative/fail-closed policy: treat as disallowed when robots.txt cannot be reached
        parser.parse(["User-agent: *", "Disallow: /"])
        _robots_cache[domain_key] = parser
        return parser
    except Exception as e:
        logger.error(f"Unexpected error parsing robots.txt for {domain_key}: {e}")
        return None


def can_fetch(target_url, user_agent="*"):
    """
    Check whether a URL is allowed to be crawled according to robots.txt.

    Args:
        target_url (str): The URL we intend to access.
        user_agent (str): User-agent string or token to evaluate against.

    Returns:
        bool: True if crawling is explicitly allowed or unrestricted; False otherwise.
    """
    if not isinstance(target_url, str) or not target_url.strip():
        logger.error(f"Invalid URL provided to can_fetch: {target_url}")
        return False

    target_url = target_url.strip()
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        logger.error(f"Invalid URL structure: {target_url}")
        return False

    parser = get_robot_parser(target_url)
    if parser is None:
        logger.warning(f"Unable to verify robots.txt for {target_url}; denying access (fail-closed).")
        return False

    allowed = parser.can_fetch(user_agent, target_url)
    if allowed:
        logger.debug(f"robots.txt allows: {target_url}")
    else:
        logger.warning(f"robots.txt disallows: {target_url}")

    return allowed


def clear_robots_cache():
    """Clear cached robots.txt parsers (useful for testing)."""
    global _robots_cache
    _robots_cache.clear()