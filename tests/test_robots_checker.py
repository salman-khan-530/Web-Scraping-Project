"""
Unit tests for the robots.txt checker module.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests

from scraper.robots_checker import can_fetch, get_robot_parser, clear_robots_cache


class TestRobotsChecker(unittest.TestCase):

    def setUp(self):
        clear_robots_cache()

    def tearDown(self):
        clear_robots_cache()

    @patch("requests.get")
    def test_robots_allowed(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "User-agent: *\nAllow: /public/\nDisallow: /admin/"
        mock_get.return_value = mock_resp

        self.assertTrue(can_fetch("https://example.com/public/item1"))
        self.assertFalse(can_fetch("https://example.com/admin/dashboard"))

    @patch("requests.get")
    def test_robots_404_allows_all(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        self.assertTrue(can_fetch("https://example.com/any-page"))

    @patch("requests.get")
    def test_robots_network_error_fail_closed(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("DNS failure")

        # Conservative fail-closed policy
        self.assertFalse(can_fetch("https://unreachable-domain-12345.com/page"))

    def test_invalid_urls(self):
        self.assertFalse(can_fetch(""))
        self.assertFalse(can_fetch("not-a-valid-url"))
        self.assertFalse(can_fetch(None))
        self.assertFalse(can_fetch("http://"))

    @patch("requests.get")
    def test_domain_caching(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "User-agent: *\nDisallow: /secret/"
        mock_get.return_value = mock_resp

        can_fetch("https://example.org/page1")
        can_fetch("https://example.org/page2")
        can_fetch("https://example.org/page3")

        # robots.txt should only be fetched once for example.org
        self.assertEqual(mock_get.call_count, 1)


if __name__ == "__main__":
    unittest.main()
