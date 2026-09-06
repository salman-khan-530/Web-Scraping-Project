"""
Unit tests for the HTTP client module.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests

from scraper.http_client import HttpClient, fetch_page


class TestHttpClient(unittest.TestCase):

    def setUp(self):
        self.client = HttpClient(delay=0, timeout=2, check_robots=False)

    def tearDown(self):
        self.client.close()

    @patch("requests.Session.get")
    def test_fetch_valid_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Test Page</h1></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.client.fetch("https://example.com/page")
        self.assertIsNotNone(result)
        self.assertIn("Test Page", result)

    def test_fetch_invalid_url_types(self):
        self.assertIsNone(self.client.fetch(None))
        self.assertIsNone(self.client.fetch(""))
        self.assertIsNone(self.client.fetch("   "))
        self.assertIsNone(self.client.fetch(12345))

    @patch("requests.Session.get")
    def test_fetch_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        result = self.client.fetch("https://example.com/timeout")
        self.assertIsNone(result)

    @patch("requests.Session.get")
    def test_fetch_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Host unreachable")

        result = self.client.fetch("https://example.com/down")
        self.assertIsNone(result)

    @patch("requests.Session.get")
    def test_fetch_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = self.client.fetch("https://example.com/missing")
        self.assertIsNone(result)

    @patch("scraper.http_client.can_fetch")
    def test_fetch_robots_disallowed(self, mock_can_fetch):
        mock_can_fetch.return_value = False
        client_with_robots = HttpClient(delay=0, check_robots=True)
        result = client_with_robots.fetch("https://example.com/private")
        self.assertIsNone(result)
        mock_can_fetch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
