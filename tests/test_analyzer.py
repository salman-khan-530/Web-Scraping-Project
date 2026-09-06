"""
Unit tests for data analyzer module.
"""

import unittest
import pandas as pd

from scraper.analyzer import (
    total_products,
    average_price,
    minimum_price,
    maximum_price,
    average_rating,
    most_common_rating,
    available_products,
    unavailable_products,
    most_common_category,
    highest_rated_products,
    lowest_priced_products,
    most_expensive_products,
    generate_summary
)


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame([
            {"name": "Book A", "price": 10.0, "rating": 5.0, "availability": "In Stock", "category": "Fiction"},
            {"name": "Book B", "price": 20.0, "rating": 3.0, "availability": "In Stock", "category": "Fiction"},
            {"name": "Book C", "price": 30.0, "rating": 5.0, "availability": "Out of Stock", "category": "Poetry"},
        ])

    def test_statistics(self):
        self.assertEqual(total_products(self.df), 3)
        self.assertEqual(average_price(self.df), 20.0)
        self.assertEqual(minimum_price(self.df), 10.0)
        self.assertEqual(maximum_price(self.df), 30.0)
        self.assertAlmostEqual(average_rating(self.df), 4.33, places=2)
        self.assertEqual(most_common_rating(self.df), 5.0)
        self.assertEqual(available_products(self.df), 2)
        self.assertEqual(unavailable_products(self.df), 1)
        self.assertEqual(most_common_category(self.df), "Fiction")

    def test_top_and_lowest(self):
        highest = highest_rated_products(self.df, top_n=2)
        self.assertEqual(len(highest), 2)
        self.assertTrue((highest["rating"] == 5.0).all())

        lowest = lowest_priced_products(self.df, top_n=1)
        self.assertEqual(lowest.iloc[0]["name"], "Book A")

        expensive = most_expensive_products(self.df, top_n=1)
        self.assertEqual(expensive.iloc[0]["name"], "Book C")

    def test_summary_dictionary(self):
        summary = generate_summary(self.df)
        self.assertIn("total_products", summary)
        self.assertEqual(summary["total_products"], 3)
        self.assertEqual(summary["average_price"], 20.0)

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame()
        self.assertEqual(total_products(empty_df), 0)
        self.assertEqual(average_price(empty_df), 0.0)
        self.assertEqual(average_rating(empty_df), 0.0)
        self.assertEqual(available_products(empty_df), 0)
        self.assertEqual(most_common_category(empty_df), "Unknown")


if __name__ == "__main__":
    unittest.main()
