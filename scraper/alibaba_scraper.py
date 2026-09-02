from scraper.base_scraper import BaseScraper

from scraper.logger import logger


class AlibabaScraper(BaseScraper):
    """
    Scraper implementation for Alibaba.

    Alibaba product data should be collected through
    an authorized access method.
    """

    def __init__(self):

        self.base_url = (
            "https://www.alibaba.com/"
        )

        self.search_url = (
            "https://www.alibaba.com/trade/search"
        )

        self.source_name = "Alibaba"

        logger.info(
            f"{self.source_name} scraper initialized."
        )

    def search_products(
        self,
        query,
        max_products=20
    ):
        """
        Search for Alibaba products.

        The actual Alibaba data source will be connected
        in a later implementation step.
        """

        if not isinstance(query, str):

            logger.warning(
                "Alibaba query must be a string."
            )

            return []

        query = query.strip()

        if not query:

            logger.warning(
                "Alibaba search query is empty."
            )

            return []

        if max_products <= 0:

            logger.warning(
                "Maximum products must be greater "
                "than zero."
            )

            return []

        logger.info(
            f"Alibaba search requested: '{query}'"
        )

        logger.info(
            f"Maximum products requested: "
            f"{max_products}"
        )

        logger.warning(
            "Alibaba data source is not configured."
        )

        logger.warning(
            "Use an authorized Alibaba API or "
            "approved data-access method."
        )

        return []

    def get_product_details(
        self,
        product_url
    ):
        """
        Get detailed Alibaba product information.

        This method will use the same authorized
        data source as search_products().
        """

        if not product_url:

            logger.warning(
                "Alibaba product URL is missing."
            )

            return {
                "category": None,
                "description": None
            }

        logger.info(
            f"Alibaba product details requested: "
            f"{product_url}"
        )

        logger.warning(
            "Alibaba product details source is "
            "not configured yet."
        )

        return {
            "category": None,
            "description": None
        }