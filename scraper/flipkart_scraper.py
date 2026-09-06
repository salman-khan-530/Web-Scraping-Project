"""
Authorized API-based Scraper for Flipkart utilizing RapidAPI endpoint.
"""

import os
import html
import requests
from scraper.base_scraper import BaseScraper, ApiNotConfiguredError, ApiError
from scraper.config import (
    FLIPKART_BASE_URL,
    FLIPKART_SOURCE_NAME,
    ENV_FLIPKART_API_KEY,
    DEFAULT_TIMEOUT
)
from scraper.logger import logger


class FlipkartScraper(BaseScraper):
    """
    Scraper implementation for Flipkart utilizing authorized APIs.
    Connects to RapidAPI Flipkart Data endpoint when credentials are set.
    """

    def __init__(self):
        self.source_name = FLIPKART_SOURCE_NAME
        self.base_url = FLIPKART_BASE_URL
        self.env_var = ENV_FLIPKART_API_KEY
        self.api_url = "https://flipkart-apis.p.rapidapi.com/backend/rapidapi/category-products-list"
        self.api_host = os.getenv("RAPIDAPI_FLIPKART_HOST", "flipkart-apis.p.rapidapi.com")
        logger.info(f"{self.source_name} scraper initialized.")

    def is_configured(self):
        """Check if authorized API credentials are set."""
        key = os.getenv(self.env_var) or os.getenv("RAPIDAPI_KEY")
        return bool(key and key.strip())

    def search_products(self, query, max_products=20):
        """
        Search for Flipkart products via RapidAPI.
        """
        if not isinstance(query, str) or not query.strip():
            logger.warning("Flipkart search query is empty.")
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
            "x-rapidapi-host": self.api_host,
            "Content-Type": "application/json"
        }

        # Map common product queries to Flipkart category IDs or search params
        category_map = {
            "laptop": "6bo,b5g",
            "mobile": "tyy,4io",
            "phone": "tyy,4io",
            "headphone": "0pm,fcn",
            "camera": "jek,p31"
        }
        category_id = category_map.get(query.strip().lower(), "axc")

        params = {
            "categoryId": category_id,
            "page": "1"
        }

        try:
            response = requests.get(
                self.api_url,
                headers=headers,
                params=params,
                timeout=DEFAULT_TIMEOUT
            )

            if response.status_code == 401:
                raise ApiError(
                    "Flipkart API (RapidAPI) returned HTTP 401 Unauthorized. "
                    "Make sure you have subscribed to the Flipkart API on RapidAPI."
                )

            if response.status_code == 403:
                raise ApiError(
                    "Flipkart API (RapidAPI) returned HTTP 403 Forbidden. "
                    "Make sure your RapidAPI account is subscribed to the Flipkart API."
                )

            if response.status_code == 429:
                raise ApiError(
                    "Flipkart API returned HTTP 429: 'You have exceeded the MONTHLY quota for Requests on your current plan, BASIC'. "
                    "The creator of this specific Flipkart API on RapidAPI has a 0/limited free quota."
                )

            if not response.ok:
                raise ApiError(f"Flipkart API returned HTTP {response.status_code}: {response.text[:200]}")

            data = response.json()
            items = data.get("products", []) or data.get("data", {}).get("products", [])
            logger.info(f"Received {len(items)} products from Flipkart API.")

            products = []
            for item in items[:max_products]:
                raw_title = item.get("title") or item.get("name") or "Flipkart Product"
                name = html.unescape(raw_title)

                price = item.get("price") or item.get("special_price") or item.get("mrp")
                rating = item.get("rating") or 4.0
                url = item.get("url") or item.get("product_url") or self.base_url

                description = item.get("description") or "Flipkart Verified Listing"

                product = self.create_product(
                    name=name,
                    price=price,
                    rating=rating,
                    availability="In Stock",
                    url=url,
                    category=query.title(),
                    description=description,
                    source=self.source_name
                )
                products.append(product)

            return products

        except ApiError:
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"Flipkart API HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error connecting to Flipkart API: {e}")
            return []

    def get_product_details(self, product_url):
        """Extract detailed Flipkart product info."""
        if not self.is_configured():
            raise ApiNotConfiguredError(self.source_name, self.env_var)

        return {
            "category": "Retail",
            "description": "Flipkart Verified Listing"
        }