import re

from scraper.base_scraper import BaseScraper

from scraper.http_client import fetch_page

from scraper.parser import (
    parse_html,
    extract_products,
    extract_product_details
)

from scraper.pagination import get_next_page

from scraper.config import BASE_URL

from scraper.logger import logger


class BooksToScrapeScraper(BaseScraper):
    """
    Scraper implementation for Books to Scrape.
    """

    def search_products(self, query, max_products=20):
        """
        Search and collect products from Books to Scrape.

        Products are collected from catalog pages and
        filtered using the product name.

        Args:
            query (str): Product search query.
            max_products (int): Maximum number of products.

        Returns:
            list: List of standardized product dictionaries.
        """

        products = []

        current_url = BASE_URL
        page_number = 1
        visited_urls = set()

        # Clean search query
        query = query.strip()

        if not query:
            logger.warning(
                "Search query is empty."
            )

            return products

        logger.info(
            f"Searching for products with query: '{query}'"
        )

        # Scrape catalog pages
        while len(products) < max_products:

            # Prevent duplicate page visits
            if current_url in visited_urls:

                logger.warning(
                    f"Page already visited: {current_url}"
                )

                break

            visited_urls.add(current_url)

            logger.info(
                f"Scraping page {page_number}: "
                f"{current_url}"
            )

            # Fetch page
            html = fetch_page(
                current_url
            )

            if html is None:

                logger.error(
                    f"Failed to fetch page: "
                    f"{current_url}"
                )

                break

            # Parse HTML
            soup = parse_html(
                html
            )

            if soup is None:

                logger.error(
                    f"Failed to parse page: "
                    f"{current_url}"
                )

                break

            # Extract products
            page_products = extract_products(
                soup,
                BASE_URL
            )

            logger.info(
                f"Products found on page "
                f"{page_number}: "
                f"{len(page_products)}"
            )

            # Filter products using exact word matching
            for product in page_products:

                name = product.get(
                    "name"
                ) or ""

                # Match the search query as a complete word.
                #
                # Example:
                # "light" matches "A Light in the Attic"
                #
                # But:
                # "light" does NOT match "Flight"

                if re.search(
                    rf"\b{re.escape(query)}\b",
                    name,
                    re.IGNORECASE
                ):

                    products.append(
                        product
                    )

                    logger.info(
                        f"Product matched query: "
                        f"{name}"
                    )

                    # Stop when maximum products are reached
                    if len(products) >= max_products:
                        break

            logger.info(
                f"Matching products collected "
                f"so far: {len(products)}"
            )

            # Stop when enough products are found
            if len(products) >= max_products:
                break

            # Find next page
            next_url = get_next_page(
                soup,
                current_url
            )

            if not next_url:

                logger.info(
                    "No next page found."
                )

                break

            current_url = next_url
            page_number += 1

        # Limit products
        products = products[
            :max_products
        ]

        logger.info(
            f"Search filtering completed. "
            f"Matching products: {len(products)}"
        )

        # Get detailed information
        standardized_products = []

        for product in products:

            product_url = product.get(
                "url"
            )

            details = {
                "category": None,
                "description": None
            }

            if product_url:

                details = self.get_product_details(
                    product_url
                )

            else:

                logger.warning(
                    f"Product URL missing: "
                    f"{product.get('name')}"
                )

            # Create standardized product
            standardized_product = self.create_product(
                name=product.get(
                    "name"
                ),
                price=product.get(
                    "price"
                ),
                rating=product.get(
                    "rating"
                ),
                availability=product.get(
                    "availability"
                ),
                url=product.get(
                    "url"
                ),
                category=details.get(
                    "category"
                ),
                description=details.get(
                    "description"
                ),
                source="Books to Scrape"
            )

            standardized_products.append(
                standardized_product
            )

        logger.info(
            f"Search completed. "
            f"Products collected: "
            f"{len(standardized_products)}"
        )

        return standardized_products

    def get_product_details(self, product_url):
        """
        Extract detailed information from a product page.

        Args:
            product_url (str): Product page URL.

        Returns:
            dict: Product category and description.
        """

        logger.info(
            f"Fetching product details: "
            f"{product_url}"
        )

        # Fetch product page
        html = fetch_page(
            product_url
        )

        if html is None:

            logger.error(
                f"Failed to fetch product page: "
                f"{product_url}"
            )

            return {
                "category": None,
                "description": None
            }

        # Parse product page
        soup = parse_html(
            html
        )

        if soup is None:

            logger.error(
                f"Failed to parse product page: "
                f"{product_url}"
            )

            return {
                "category": None,
                "description": None
            }

        # Extract product details
        details = extract_product_details(
            soup
        )

        return details