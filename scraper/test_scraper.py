"""
Test scraper implementation using Books to Scrape as a safe demonstration site.
Labeled strictly as 'Test Site'.
"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.config import (
    TEST_SITE_NAME,
    TEST_SITE_BASE_URL,
    TEST_SITE_CATALOGUE_URL,
    MAX_PAGES_TO_SCRAPE
)
from scraper.http_client import fetch_page
from scraper.logger import logger


class TestScraper(BaseScraper):
    """
    Test scraper implementation using Books to Scrape.
    Used exclusively as a safe test/demo source for evaluating the scraping pipeline.
    """

    def __init__(self):
        self.source_name = TEST_SITE_NAME
        self.base_url = TEST_SITE_BASE_URL
        self.catalogue_url = TEST_SITE_CATALOGUE_URL
        self.max_pages = MAX_PAGES_TO_SCRAPE
        logger.info(f"{self.source_name} scraper initialized.")

    def search_products(self, query, max_products=20):
        """
        Search for products matching query on the Test Site.

        Args:
            query (str): Product search query keyword.
            max_products (int): Maximum number of products to collect.

        Returns:
            list[dict]: Extracted product dictionaries.
        """
        # Validate query
        if not isinstance(query, str):
            logger.warning("Search query must be a string.")
            return []

        search_term = query.strip().lower()
        if not search_term:
            logger.warning("Search query is empty or contains only whitespace.")
            return []

        # Validate max_products
        if not isinstance(max_products, int) or max_products <= 0:
            logger.warning(f"Invalid max_products: {max_products}. Must be positive integer.")
            return []

        products = []
        page_number = 1

        logger.info(f"{self.source_name} search started: '{search_term}' (limit: {max_products})")

        while len(products) < max_products and page_number <= self.max_pages:
            page_url = self.catalogue_url.format(page_number)
            logger.info(f"Fetching page {page_number}/{self.max_pages}: {page_url}")

            html = fetch_page(page_url)
            if not html:
                logger.info(f"Could not fetch page {page_number}. Ending pagination.")
                break

            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select("article.product_pod")

            if not cards:
                logger.info(f"No product cards found on page {page_number}. End of catalogue reached.")
                break

            for card in cards:
                name_tag = card.select_one("h3 a")
                if not name_tag:
                    continue

                name = name_tag.get("title") or name_tag.get_text(strip=True)
                if not name:
                    continue

                # Filter by search query
                if search_term not in name.lower():
                    continue

                # Price extraction
                price_tag = card.select_one(".price_color")
                price = price_tag.get_text(strip=True) if price_tag else None

                # Rating extraction
                rating = None
                rating_tag = card.select_one("p.star-rating")
                if rating_tag:
                    classes = rating_tag.get("class", [])
                    rating_map = {
                        "One": 1,
                        "Two": 2,
                        "Three": 3,
                        "Four": 4,
                        "Five": 5
                    }
                    for word, val in rating_map.items():
                        if word in classes:
                            rating = val
                            break

                # Availability
                avail_tag = card.select_one(".availability")
                availability = avail_tag.get_text(" ", strip=True) if avail_tag else None

                # URL
                rel_url = name_tag.get("href")
                if rel_url:
                    # Resolve relative catalogue URL
                    product_url = urljoin(page_url, rel_url)
                else:
                    product_url = None

                # Product detail extraction (category, description)
                details = self.get_product_details(product_url) if product_url else {}

                product = self.create_product(
                    name=name,
                    price=price,
                    rating=rating,
                    availability=availability,
                    url=product_url,
                    category=details.get("category"),
                    description=details.get("description"),
                    source=self.source_name
                )

                products.append(product)
                logger.info(f"Collected product ({len(products)}/{max_products}): {name}")

                if len(products) >= max_products:
                    break

            # Check if next page exists via pagination controls
            next_btn = soup.select_one("li.next a")
            if not next_btn:
                logger.info("No next page link found. Finished all available pages.")
                break

            page_number += 1

        logger.info(f"{self.source_name} search finished. Total matched: {len(products)}")
        return products[:max_products]

    def get_product_details(self, product_url):
        """
        Extract category and description from a specific product page.
        """
        if not product_url:
            return {"category": None, "description": None}

        html = fetch_page(product_url)
        if not html:
            return {"category": None, "description": None}

        soup = BeautifulSoup(html, "html.parser")

        # Category from breadcrumb
        category = None
        crumbs = soup.select(".breadcrumb li a")
        if len(crumbs) >= 3:
            category = crumbs[2].get_text(strip=True)

        # Description
        description = None
        desc_header = soup.select_one("#product_description")
        if desc_header:
            desc_p = desc_header.find_next_sibling("p")
            if desc_p:
                raw_desc = desc_p.get_text(" ", strip=True)
                # Clean up "...more" and normalize spaces
                raw_desc = raw_desc.replace("...more", "").strip()
                description = " ".join(raw_desc.split())

                # Books to Scrape sometimes repeats the lead sentence
                prefix_len = 80
                if len(description) > prefix_len * 2:
                    prefix = description[:prefix_len]
                    second_idx = description.find(prefix, prefix_len)
                    if second_idx != -1:
                        description = description[second_idx:].strip()

        return {
            "category": category,
            "description": description
        }