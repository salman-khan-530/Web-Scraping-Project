"""
Abstract Base Scraper defining the standard interface for all web scrapers.
"""

from abc import ABC, abstractmethod


class ApiNotConfiguredError(Exception):
    """Raised when a scraper requires authorized API credentials that have not been configured."""
    def __init__(self, service_name, env_var):
        self.service_name = service_name
        self.env_var = env_var
        super().__init__(
            f"{service_name} API is not configured. "
            f"Please configure the required authorized API credentials via {env_var} in your environment (.env)."
        )


class ApiError(Exception):
    """Raised when an external API returns an error response (such as 401, 403, 429)."""
    pass


class BaseScraper(ABC):
    """
    Common interface for all website and API scrapers.
    """

    source_name = "Base Scraper"

    @abstractmethod
    def search_products(self, query, max_products=20):
        """
        Search for products on the target website/API.

        Args:
            query (str): Product search query.
            max_products (int): Maximum number of products to return.

        Returns:
            list[dict]: List of standardized product dictionaries.
        """
        pass

    @abstractmethod
    def get_product_details(self, product_url):
        """
        Extract detailed information from a product page/resource.

        Args:
            product_url (str): Product page URL or identifier.

        Returns:
            dict: Dictionary with 'category' and 'description' or other detail fields.
        """
        pass

    def is_configured(self):
        """
        Check whether this scraper has the necessary credentials or prerequisites.

        Returns:
            bool: True if ready to operate, False otherwise.
        """
        return True

    @staticmethod
    def create_product(
        name=None,
        price=None,
        rating=None,
        availability=None,
        url=None,
        category=None,
        description=None,
        source=None
    ):
        """
        Create a standardized product dictionary.

        Returns:
            dict: Standard product format.
        """
        return {
            "name": name,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": url,
            "category": category,
            "description": description,
            "source": source
        }