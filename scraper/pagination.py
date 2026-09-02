from urllib.parse import urljoin


def get_next_page(soup, current_url):
    """
    Find and return the URL of the next page.

    Returns:
        str: Absolute URL of the next page.
        None: If no next page exists.
    """

    if soup is None:
        return None

    next_button = soup.select_one("li.next a")

    if not next_button:
        return None

    next_url = next_button.get("href")

    if not next_url:
        return None

    return urljoin(
        current_url,
        next_url
    )