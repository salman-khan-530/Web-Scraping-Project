from http_client import fetch_page
from parser import parse_html


url = "https://books.toscrape.com/"

html = fetch_page(url)

soup = parse_html(html)

products_data = []

if soup:
    products = soup.select(".product_pod")

    print(f"Total products found: {len(products)}")

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

        product_data = {
            "name": name,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": product_url
        }

        products_data.append(product_data)


print(f"\nTotal products stored: {len(products_data)}")

for product in products_data:
    print("\n" + "-" * 50)
    print("Name:", product["name"])
    print("Price:", product["price"])
    print("Rating:", product["rating"])
    print("Availability:", product["availability"])
    print("URL:", product["url"])