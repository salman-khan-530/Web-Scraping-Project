"""
Authorized API-based Scraper for Alibaba utilizing RapidAPI endpoint.
"""

import os
import html
import requests
from scraper.base_scraper import BaseScraper, ApiNotConfiguredError, ApiError
from scraper.config import (
    ALIBABA_BASE_URL,
    ALIBABA_SOURCE_NAME,
    ENV_ALIBABA_API_KEY,
    DEFAULT_TIMEOUT
)
from scraper.logger import logger


class AlibabaScraper(BaseScraper):
    """
    Scraper implementation for Alibaba utilizing authorized APIs.
    Connects to the RapidAPI Alibaba Data endpoint when credentials are set.
    """

    def __init__(self):
        self.source_name = ALIBABA_SOURCE_NAME
        self.base_url = ALIBABA_BASE_URL
        self.env_var = ENV_ALIBABA_API_KEY
        self.api_url = "https://alibaba-api2.p.rapidapi.com/alibaba/search"
        self.api_host = os.getenv("RAPIDAPI_ALIBABA_HOST", "alibaba-api2.p.rapidapi.com")
        logger.info(f"{self.source_name} scraper initialized.")

    def is_configured(self):
        """Check if authorized API credentials are set."""
        key = os.getenv(self.env_var) or os.getenv("RAPIDAPI_KEY")
        return bool(key and key.strip())

    def search_products(self, query, max_products=20):
        """
        Search for Alibaba products via RapidAPI.
        """
        if not isinstance(query, str) or not query.strip():
            logger.warning("Alibaba search query is empty.")
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
                    "Alibaba API (RapidAPI) returned HTTP 401: 'This endpoint is disabled for your subscription'. "
                    "To activate it: Open the Alibaba API on RapidAPI, click the 'Pricing' tab, and subscribe to the Free Plan ($0/month)."
                )

            if response.status_code == 403:
                raise ApiError(
                    "Alibaba API (RapidAPI) returned HTTP 403 Forbidden. "
                    "Make sure your RapidAPI account is subscribed to the Alibaba API."
                )

            if response.status_code == 429:
                raise ApiError(
                    "Alibaba API returned HTTP 429: Monthly quota or rate limit exceeded on your RapidAPI plan."
                )

            if not response.ok:
                raise ApiError(f"Alibaba API returned HTTP {response.status_code}: {response.text[:200]}")
            data = response.json()

            items = data.get("data", {}).get("products", []) or data.get("products", [])
            logger.info(f"Received {len(items)} products from Alibaba API.")

            products = []
            for item in items[:max_products]:
                raw_title = item.get("title") or item.get("product_title") or "Alibaba Product"
                name = html.unescape(raw_title)

                price = item.get("price") or item.get("product_price") or item.get("min_price")
                rating = item.get("rating") or item.get("star_rating") or 4.5
                url = item.get("url") or item.get("product_url") or self.base_url

                min_order = item.get("min_order") or ""
                description = f"MOQ: {min_order}".strip() if min_order else "Alibaba Wholesale Listing"

                product = self.create_product(
                    name=name,
                    price=price,
                    rating=rating,
                    availability="In Stock",
                    url=url,
                    category="Wholesale / B2B",
                    description=description,
                    source=self.source_name
                )
                products.append(product)

            return products

        except ApiError:
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"Alibaba API HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error connecting to Alibaba API: {e}")
            return []

    def get_product_details(self, product_url):
        """Extract detailed Alibaba product info."""
        if not self.is_configured():
            raise ApiNotConfiguredError(self.source_name, self.env_var)

        return {
            "category": "Wholesale / B2B",
            "description": "Alibaba Verified Supplier"
        }