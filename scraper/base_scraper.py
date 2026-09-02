from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """
    Common interface for all website scrapers.
    """

    @abstractmethod
    def search_products(self, query, max_products=20):
        """
        Search for products on the website.

        Args:
            query (str): Product search query.
            max_products (int): Maximum number of products.

        Returns:
            list: List of product dictionaries.
        """
        pass

    @abstractmethod
    def get_product_details(self, product_url):
        """
        Extract detailed information from a product page.

        Args:
            product_url (str): Product page URL.

        Returns:
            dict: Product details.
        """
        pass

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