from scraper.books_scraper import BooksToScrapeScraper
from scraper.amazon_scraper import AmazonScraper
from scraper.alibaba_scraper import AlibabaScraper
from scraper.flipkart_scraper import FlipkartScraper

from scraper.logger import logger


class ScraperManager:
    """
    Manage and select different website scrapers.
    """

    def __init__(self):

        self.scrapers = {
            "books": BooksToScrapeScraper(),
            "amazon": AmazonScraper(),
            "alibaba": AlibabaScraper(),
            "flipkart": FlipkartScraper()
        }

    def get_scraper(self, website):
        """
        Return the scraper for the selected website.

        Args:
            website (str): Website identifier.

        Returns:
            BaseScraper: Selected scraper instance.
            None: If the website is not supported.
        """

        if not isinstance(website, str):
            return None

        website = website.lower().strip()

        return self.scrapers.get(
            website
        )

    def search_multiple(
        self,
        query,
        websites=None,
        max_products=20
    ):
        """
        Search for a product across multiple websites.

        Args:
            query (str): Product search query.
            websites (list): Website identifiers.
            max_products (int): Maximum products per website.

        Returns:
            list: Combined product results.
        """

        results = []

        # Validate query
        if not isinstance(query, str):

            logger.warning(
                "Search query must be a string."
            )

            return results

        query = query.strip()

        if not query:

            logger.warning(
                "Search query is empty."
            )

            return results

        # Use all supported websites if none are provided
        if websites is None:

            websites = list(
                self.scrapers.keys()
            )

        if not websites:

            logger.warning(
                "No websites were selected."
            )

            return results

        logger.info(
            f"Multi-website search started: "
            f"'{query}'"
        )

        logger.info(
            f"Websites selected: {websites}"
        )

        # Search each selected website
        for website in websites:

            scraper = self.get_scraper(
                website
            )

            if scraper is None:

                logger.warning(
                    f"Unsupported website: "
                    f"{website}"
                )

                continue

            logger.info(
                f"Searching {website}..."
            )

            try:

                products = scraper.search_products(
                    query,
                    max_products
                )

                if products:

                    results.extend(
                        products
                    )

                    logger.info(
                        f"{website}: "
                        f"{len(products)} products found."
                    )

                else:

                    logger.info(
                        f"{website}: "
                        f"No products found."
                    )

            except Exception as e:

                logger.error(
                    f"Error while searching "
                    f"{website}: {e}"
                )

                continue

        logger.info(
            f"Multi-website search completed. "
            f"Total products: {len(results)}"
        )

        return results