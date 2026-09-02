from scraper.base_scraper import BaseScraper

from scraper.config import (
    AMAZON_BASE_URL,
    AMAZON_SEARCH_URL,
    AMAZON_SOURCE_NAME
)

from scraper.logger import logger


class AmazonScraper(BaseScraper):
    """
    Scraper implementation for Amazon.

    Amazon product data should be collected through
    an authorized access method.
    """

    def __init__(self):

        self.base_url = AMAZON_BASE_URL
        self.search_url = AMAZON_SEARCH_URL
        self.source_name = AMAZON_SOURCE_NAME

        logger.info(
            f"{self.source_name} scraper initialized."
        )

    def search_products(
        self,
        query,
        max_products=20
    ):
        """
        Search for Amazon products.

        The actual Amazon data source will be connected
        in a later implementation step.
        """

        if not isinstance(query, str):

            logger.warning(
                "Amazon query must be a string."
            )

            return []

        query = query.strip()

        if not query:

            logger.warning(
                "Amazon search query is empty."
            )

            return []

        if max_products <= 0:

            logger.warning(
                "Maximum products must be greater than zero."
            )

            return []

        logger.info(
            f"Amazon search requested: '{query}'"
        )

        logger.info(
            f"Maximum products requested: "
            f"{max_products}"
        )

        logger.warning(
            "Amazon data source is not configured."
        )

        logger.warning(
            "Use an authorized Amazon API or "
            "approved data-access method."
        )

        return []

    def get_product_details(
        self,
        product_url
    ):
        """
        Get detailed Amazon product information.

        This method will be connected to the same
        authorized data source used by search_products().
        """

        if not product_url:

            logger.warning(
                "Amazon product URL is missing."
            )

            return {
                "category": None,
                "description": None
            }

        logger.info(
            f"Amazon product details requested: "
            f"{product_url}"
        )

        logger.warning(
            "Amazon product details source is "
            "not configured yet."
        )

        return {
            "category": None,
            "description": None
        }