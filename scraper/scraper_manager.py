"""
Scraper Manager to coordinate and access scrapers across supported websites.
"""

from scraper.amazon_scraper import AmazonScraper
from scraper.alibaba_scraper import AlibabaScraper
from scraper.flipkart_scraper import FlipkartScraper
from scraper.test_scraper import TestScraper
from scraper.base_scraper import ApiNotConfiguredError
from scraper.logger import logger


class ScraperManager:
    """
    Manages registration, selection, and multi-source execution of scrapers.
    """

    def __init__(self):
        self.scrapers = {
            "test": TestScraper(),
            "amazon": AmazonScraper(),
            "alibaba": AlibabaScraper(),
            "flipkart": FlipkartScraper()
        }

        # Friendly display name mappings
        self.alias_map = {
            "test": "test",
            "test site": "test",
            "test_site": "test",
            "amazon": "amazon",
            "flipkart": "flipkart",
            "alibaba": "alibaba"
        }

    def normalize_name(self, website):
        """Map human or varied keys to internal scraper key."""
        if not isinstance(website, str):
            return None
        cleaned = website.strip().lower()
        return self.alias_map.get(cleaned, cleaned)

    def get_scraper(self, website):
        """
        Return scraper instance for given website name.
        """
        key = self.normalize_name(website)
        return self.scrapers.get(key)

    def is_configured(self, website):
        """
        Check if the target scraper is ready and configured.
        """
        scraper = self.get_scraper(website)
        if scraper is None:
            return False
        return scraper.is_configured()

    def search(self, website, query, max_products=20):
        """
        Search products on a specific website.

        Raises:
            ValueError: If website is unsupported.
            ApiNotConfiguredError: If website API credentials are not set.
        """
        scraper = self.get_scraper(website)
        if scraper is None:
            raise ValueError(f"Unsupported website: '{website}'")

        return scraper.search_products(query, max_products=max_products)

    def search_multiple(self, query, websites=None, max_products=20):
        """
        Search for products across multiple websites.

        Args:
            query (str): Product search query.
            websites (list[str], optional): List of website identifiers.
            max_products (int): Maximum products per website.

        Returns:
            list[dict]: Combined product results.
        """
        results = []

        if not isinstance(query, str) or not query.strip():
            logger.warning("Search query is empty or invalid.")
            return results

        query = query.strip()

        if websites is None:
            # Default to test scraper if none provided
            websites = ["test"]

        logger.info(f"Multi-search initiated: '{query}' on websites {websites} (limit: {max_products}/site)")

        for site in websites:
            scraper = self.get_scraper(site)
            if scraper is None:
                logger.warning(f"Skipping unsupported website: {site}")
                continue

            try:
                products = scraper.search_products(query, max_products=max_products)
                if products:
                    results.extend(products)
                    logger.info(f"Retrieved {len(products)} products from {scraper.source_name}")
                else:
                    logger.info(f"No products found on {scraper.source_name}")
            except ApiNotConfiguredError as e:
                logger.warning(f"{scraper.source_name} skipped: {e}")
            except Exception as e:
                logger.error(f"Error scraping {scraper.source_name}: {e}")

        logger.info(f"Multi-search complete. Total aggregated products: {len(results)}")
        return results