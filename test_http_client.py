from http_client import fetch_page


url = "https://books.toscrape.com/"

html = fetch_page(url)

if html:
    print("\nFirst 500 characters:\n")
    print(html[:500])