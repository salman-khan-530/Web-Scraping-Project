import requests

def fetch_page(url):
    """
    Fetch html content from a webpage
    Args:
    url (str): url of the page
    returns:
    str: html content if the requests is successful
    none: if the request fails
    """

    try:
        response = requests.get(url, timeout=10)

        response.raise_for_status()

        print(f"Request successful: {url}")
        print(f"Status code: {response.status_code}")

        return response.text
    except requests.exceptions.RequestException as error:
        print(f"Request faild: {error}")
        return None  