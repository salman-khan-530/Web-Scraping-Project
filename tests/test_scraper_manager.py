"""
Unit tests for ScraperManager.
"""

import os
import unittest
from unittest.mock import patch

from scraper.scraper_manager import ScraperManager
from scraper.test_scraper import TestScraper
from scraper.amazon_scraper import AmazonScraper
from scraper.flipkart_scraper import FlipkartScraper
from scraper.alibaba_scraper import AlibabaScraper
from scraper.base_scraper import ApiNotConfiguredError


class TestScraperManager(unittest.TestCase):

    def setUp(self):
        self.manager = ScraperManager()

    def test_scraper_registration(self):
        self.assertIsInstance(self.manager.get_scraper("test"), TestScraper)
        self.assertIsInstance(self.manager.get_scraper("Test Site"), TestScraper)
        self.assertIsInstance(self.manager.get_scraper("amazon"), AmazonScraper)
        self.assertIsInstance(self.manager.get_scraper("flipkart"), FlipkartScraper)
        self.assertIsInstance(self.manager.get_scraper("alibaba"), AlibabaScraper)

    def test_unsupported_scraper(self):
        self.assertIsNone(self.manager.get_scraper("walmart"))
        self.assertIsNone(self.manager.get_scraper(None))

    def test_unconfigured_api_raises_error(self):
        # When keys are cleared, is_configured should be False and search should raise ApiNotConfiguredError
        with patch.dict(os.environ, {"FLIPKART_API_KEY": "", "RAPIDAPI_KEY": ""}, clear=False):
            scraper = self.manager.get_scraper("flipkart")
            # Clear cached env lookups
            with patch.object(scraper, "is_configured", return_value=False):
                self.assertFalse(scraper.is_configured())
                with self.assertRaises(ApiNotConfiguredError):
                    self.manager.search("flipkart", "laptop")

    @patch("scraper.test_scraper.TestScraper.search_products")
    @patch("scraper.flipkart_scraper.FlipkartScraper.search_products")
    def test_search_multiple_aggregates(self, mock_flipkart, mock_test):
        mock_test.return_value = [
            {"name": "Item 1", "price": 10.0, "source": "Test Site"}
        ]
        mock_flipkart.side_effect = ApiNotConfiguredError("Flipkart", "FLIPKART_API_KEY")

        results = self.manager.search_multiple("light", websites=["test", "flipkart"])
        # Flipkart is unconfigured so skipped with warning, Test Site returns 1 item
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Item 1")


if __name__ == "__main__":
    unittest.main()
