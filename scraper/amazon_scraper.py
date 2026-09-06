"""
Authorized API-based Scraper for Amazon utilizing RapidAPI endpoint.
"""

import os
import html
import requests
from scraper.base_scraper import BaseScraper, ApiNotConfiguredError
from scraper.config import (
    AMAZON_BASE_URL,
    AMAZON_SOURCE_NAME,
    ENV_AMAZON_API_KEY,
    DEFAULT_TIMEOUT
)
from scraper.logger import logger


class AmazonScraper(BaseScraper):
    """
    Scraper implementation for Amazon utilizing authorized APIs.
    Connects to the RapidAPI Real-Time Amazon Data endpoint when credentials are set.
    """

    def __init__(self):
        self.source_name = AMAZON_SOURCE_NAME
        self.base_url = AMAZON_BASE_URL
        self.env_var = ENV_AMAZON_API_KEY
        self.api_url = "https://real-time-amazon-data.p.rapidapi.com/search"
        self.api_host = os.getenv("RAPIDAPI_AMAZON_HOST", "real-time-amazon-data.p.rapidapi.com")
        logger.info(f"{self.source_name} scraper initialized.")

    def is_configured(self):
        """Check if authorized API credentials are set."""
        key = os.getenv(self.env_var) or os.getenv("RAPIDAPI_KEY")
        return bool(key and key.strip())

    def search_products(self, query, max_products=20):
        """
        Search for Amazon products via authorized API.

        Raises:
            ApiNotConfiguredError: If AMAZON_API_KEY is not configured.
        """
        if not isinstance(query, str) or not query.strip():
            logger.warning("Amazon search query is empty.")
            return []

        if max_products <= 0:
            logger.warning("Maximum products must be greater than zero.")
            return []

        if not self.is_configured():
            logger.warning(
                f"{self.source_name} data source is not configured. "
                f"Missing environment variable: {self.env_var}"
            )
            raise ApiNotConfiguredError(self.source_name, self.env_var)

        api_key = os.getenv(self.env_var) or os.getenv("RAPIDAPI_KEY")
        logger.info(f"Querying authorized {self.source_name} API for '{query}' (limit: {max_products}).")

        headers = {
            "x-rapidapi-key": api_key.strip(),
            "x-rapidapi-host": self.api_host
        }

        params = {
            "query": query.strip(),
            "page": "1",
            "country": "US"
        }

        try:
            response = requests.get(
                self.api_url,
                headers=headers,
                params=params,
                timeout=DEFAULT_TIMEOUT
            )

            response.raise_for_status()
            data = response.json()

            items = data.get("data", {}).get("products", [])
            logger.info(f"Received {len(items)} products from Amazon API.")

            products = []
            for item in items[:max_products]:
                raw_title = item.get("product_title") or "Unknown Product"
                name = html.unescape(raw_title)

                price = item.get("product_price") or item.get("product_minimum_offer_price")
                rating = item.get("product_star_rating")
                url = item.get("product_url") or f"https://www.amazon.com/dp/{item.get('asin', '')}"

                delivery = item.get("delivery") or ""
                photo = item.get("product_photo") or ""
                description = f"{delivery}".strip() if delivery else "Amazon listing"

                product = self.create_product(
                    name=name,
                    price=price,
                    rating=rating,
                    availability="In Stock" if price else "Check Listing",
                    url=url,
                    category="Electronics / General",
                    description=description,
                    source=self.source_name
                )
                products.append(product)

            return products

        except requests.exceptions.HTTPError as e:
            logger.error(f"Amazon API HTTP error: {e}")
            if response.status_code == 403:
                logger.error("RapidAPI returned 403 Forbidden. Check your subscription to the API.")
            return []
        except Exception as e:
            logger.error(f"Error connecting to Amazon API: {e}")
            return []

    def get_product_details(self, product_url):
        """
        Extract detailed product info via authorized Amazon API.
        """
        if not self.is_configured():
            raise ApiNotConfiguredError(self.source_name, self.env_var)

        return {
            "category": "Electronics / General",
            "description": "Amazon Verified Listing"
        }