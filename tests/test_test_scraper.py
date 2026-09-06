"""
Unit tests for the TestScraper (Books-to-Scrape test demonstration source).
"""

import unittest
from unittest.mock import patch

from scraper.test_scraper import TestScraper

SAMPLE_PAGE_HTML = """
<!DOCTYPE html>
<html>
<body>
    <ol class="row">
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
                <div class="image_container">
                    <a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache.jpg" alt="A Light in the Attic"></a>
                </div>
                <p class="star-rating Three"></p>
                <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
                <div class="product_price">
                    <p class="price_color">£51.77</p>
                    <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                </div>
            </article>
        </li>
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
                <p class="star-rating Five"></p>
                <h3><a href="catalogue/tipping-the-velvet_999/index.html" title="Tipping the Velvet">Tipping the Velvet</a></h3>
                <div class="product_price">
                    <p class="price_color">£53.74</p>
                    <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                </div>
            </article>
        </li>
    </ol>
</body>
</html>
"""

SAMPLE_DETAIL_HTML = """
<!DOCTYPE html>
<html>
<body>
    <ul class="breadcrumb">
        <li><a href="../../index.html">Home</a></li>
        <li><a href="../category/books_1/index.html">Books</a></li>
        <li><a href="../category/books/poetry_23/index.html">Poetry</a></li>
        <li class="active">A Light in the Attic</li>
    </ul>
    <div id="product_description" class="sub-header">
        <h2>Product Description</h2>
    </div>
    <p>It's hard to imagine a world without A Light in the Attic...more</p>
</body>
</html>
"""


class TestTestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = TestScraper()

    def test_invalid_query_returns_empty(self):
        self.assertEqual(self.scraper.search_products(""), [])
        self.assertEqual(self.scraper.search_products("   "), [])
        self.assertEqual(self.scraper.search_products(None), [])

    def test_invalid_max_products_returns_empty(self):
        self.assertEqual(self.scraper.search_products("light", max_products=0), [])
        self.assertEqual(self.scraper.search_products("light", max_products=-5), [])

    @patch("scraper.test_scraper.fetch_page")
    def test_search_and_extraction(self, mock_fetch):
        def side_effect(url):
            if "a-light-in-the-attic" in url:
                return SAMPLE_DETAIL_HTML
            return SAMPLE_PAGE_HTML

        mock_fetch.side_effect = side_effect

        results = self.scraper.search_products("light", max_products=5)

        self.assertEqual(len(results), 1)
        item = results[0]
        self.assertEqual(item["name"], "A Light in the Attic")
        self.assertEqual(item["price"], "£51.77")
        self.assertEqual(item["rating"], 3)
        self.assertIn("In stock", item["availability"])
        self.assertEqual(item["category"], "Poetry")
        self.assertEqual(item["source"], "Test Site")
        self.assertIn("It's hard to imagine", item["description"])
        self.assertNotIn("...more", item["description"])

    @patch("scraper.test_scraper.fetch_page")
    def test_missing_fields_handling(self, mock_fetch):
        broken_html = """
        <article class="product_pod">
            <h3><a title="Broken Item" href="item.html">Broken Item</a></h3>
        </article>
        """
        mock_fetch.return_value = broken_html

        results = self.scraper.search_products("broken", max_products=1)
        self.assertEqual(len(results), 1)
        item = results[0]
        self.assertEqual(item["name"], "Broken Item")
        self.assertIsNone(item["price"])
        self.assertIsNone(item["rating"])
        self.assertIsNone(item["availability"])


if __name__ == "__main__":
    unittest.main()
