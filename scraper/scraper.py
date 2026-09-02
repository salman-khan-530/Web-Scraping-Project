from http_client import fetch_page
from parser import parse_html
from pagination import get_next_page


def scrape_products(start_url):
    """
    Scrape products from multiple pages.

    Args:
        start_url (str): URL of the first page.

    Returns:
        list: List of product dictionaries.
    """

    products_data = []

    current_url = start_url
    page_number = 1

    while current_url:
        print(f"\nScraping page {page_number}: {current_url}")
        html = fetch_page(current_url)

        if not html:
            print("Could not fetch this page.")
            break


        soup = parse_html(html)

        if not soup:
            print("Could not parse this page.")
            break


        products = soup.select(".product_pod")

        print(f"Products found: {len(products)}")

        for product in products:
            name_element = product.select_one("h3 a")
            price_element = product.select_one(".price_color")
            rating_element = product.select_one(".star-rating")
            availability_element = product.select_one(".availability")

            name = (
                name_element.get("title")
                if name_element
                else "N/A"
            )

            price = (
                price_element.get_text(strip=True)
                if price_element
                else "N/A"
            )

            rating = (
                rating_element.get("class")
                if rating_element
                else "N/A"
            )

            availability = (
                availability_element.get_text(strip=True)
                if availability_element
                else "N/A"
            )

            product_url = (
                name_element.get("href")
                if name_element
                else "N/A"
            )

            products_data.append({
                "name": name,
                "price": price,
                "rating": rating,
                "availability": availability,
                "url": product_url
            })


        current_url = get_next_page(soup, current_url)

        page_number += 1

    return products_data