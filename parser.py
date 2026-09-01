from bs4 import BeautifulSoup

def parse_html(html):
    """
    Parse HTML content using BeautifulSoup.
    
    Args:
        html (str): HTML content.
    
    Returns:
        BeautifulSoup: Parsed HTML document.
        None: If HTML is empty.
    """

    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    return soup