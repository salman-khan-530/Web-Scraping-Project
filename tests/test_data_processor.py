"""
Unit tests for data processor (cleaning, conversion, deduplication, and validation).
"""

import unittest
import pandas as pd

from scraper.data_processor import (
    clean_price,
    clean_rating,
    clean_availability,
    clean_product_name,
    clean_text_encoding,
    handle_missing_values,
    remove_duplicates,
    validate_data,
    clean_data
)


class TestDataProcessor(unittest.TestCase):

    def test_clean_price(self):
        self.assertEqual(clean_price("£51.77"), 51.77)
        self.assertEqual(clean_price("Â£51.77"), 51.77)
        self.assertEqual(clean_price("$29.99"), 29.99)
        self.assertEqual(clean_price("€19.50"), 19.50)
        self.assertEqual(clean_price("₹1,499.00"), 1499.00)
        self.assertEqual(clean_price(45.5), 45.5)
        self.assertIsNone(clean_price("Not Available"))
        self.assertIsNone(clean_price(None))
        self.assertIsNone(clean_price(-10.0))

    def test_clean_rating(self):
        self.assertEqual(clean_rating("One"), 1.0)
        self.assertEqual(clean_rating("three"), 3.0)
        self.assertEqual(clean_rating("Five"), 5.0)
        self.assertEqual(clean_rating(["star-rating", "Four"]), 4.0)
        self.assertEqual(clean_rating(4), 4.0)
        self.assertEqual(clean_rating("4.5 out of 5"), 4.5)
        self.assertIsNone(clean_rating("Unrated"))
        self.assertIsNone(clean_rating(0))
        self.assertIsNone(clean_rating(6))
        self.assertIsNone(clean_rating(None))

    def test_clean_availability(self):
        self.assertEqual(clean_availability("In stock"), "In Stock")
        self.assertEqual(clean_availability("in stock (19 available)"), "In Stock")
        self.assertEqual(clean_availability("IN STOCK"), "In Stock")
        self.assertEqual(clean_availability("Out of stock"), "Out of Stock")
        self.assertEqual(clean_availability(""), "Unknown")
        self.assertEqual(clean_availability(None), "Unknown")

    def test_clean_product_name(self):
        self.assertEqual(clean_product_name("  A   Light in   the Attic  "), "A Light in the Attic")
        self.assertEqual(clean_product_name(""), "Unknown")
        self.assertEqual(clean_product_name(None), "Unknown")

    def test_handle_missing_values(self):
        df = pd.DataFrame([{
            "name": None,
            "price": None,
            "rating": None,
            "availability": None,
            "url": None,
            "category": None,
            "description": None
        }])

        df_handled = handle_missing_values(df)
        self.assertEqual(df_handled.iloc[0]["name"], "Unknown")
        self.assertEqual(df_handled.iloc[0]["url"], "N/A")
        self.assertEqual(df_handled.iloc[0]["category"], "Unknown")
        self.assertEqual(df_handled.iloc[0]["availability"], "Unknown")

    def test_remove_duplicates(self):
        df = pd.DataFrame([
            {"name": "Item 1", "price": 10.0, "url": "https://example.com/item1"},
            {"name": "Item 1 Duplicate", "price": 10.0, "url": "https://example.com/item1"},
            {"name": "Item 2", "price": 20.0, "url": "https://example.com/item2"},
        ])

        deduped = remove_duplicates(df)
        self.assertEqual(len(deduped), 2)

    def test_validate_data_preserves_optional_missing_fields(self):
        # Items with missing description, category, or rating should NOT be dropped!
        df = pd.DataFrame([
            {
                "name": "Valid Product Without Rating",
                "price": 25.0,
                "rating": None,
                "url": "https://example.com/prod1",
                "description": None
            },
            {
                "name": "Valid Product Without Price",
                "price": None,
                "rating": 4.0,
                "url": "https://example.com/prod2",
                "description": "Some description"
            },
            {
                "name": "Invalid Product Without URL",
                "price": 15.0,
                "rating": 3.0,
                "url": "",
                "description": "Has no URL"
            },
            {
                "name": "",
                "price": 15.0,
                "rating": 3.0,
                "url": "https://example.com/noname",
                "description": "Empty name"
            }
        ])

        validated = validate_data(df)
        # Should retain prod1 and prod2, dropping only the ones with missing name or missing URL
        self.assertEqual(len(validated), 2)
        names = validated["name"].tolist()
        self.assertIn("Valid Product Without Rating", names)
        self.assertIn("Valid Product Without Price", names)

    def test_full_clean_data_pipeline(self):
        raw = pd.DataFrame([
            {
                "name": "  A Light in the Attic  ",
                "price": "£51.77",
                "rating": "Three",
                "availability": "In stock",
                "url": "https://books.toscrape.com/catalogue/a-light.html",
                "category": "Poetry",
                "description": "Classic poems...more",
                "source": "Test Site"
            }
        ])

        cleaned = clean_data(raw)
        self.assertEqual(len(cleaned), 1)
        row = cleaned.iloc[0]
        self.assertEqual(row["name"], "A Light in the Attic")
        self.assertEqual(row["price"], 51.77)
        self.assertEqual(row["rating"], 3.0)
        self.assertEqual(row["availability"], "In Stock")


if __name__ == "__main__":
    unittest.main()
