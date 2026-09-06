"""
Scraper package for E-Commerce Product Data Web Scraper.
"""

from scraper.base_scraper import BaseScraper
from scraper.test_scraper import TestScraper
from scraper.amazon_scraper import AmazonScraper
from scraper.flipkart_scraper import FlipkartScraper
from scraper.alibaba_scraper import AlibabaScraper
from scraper.scraper_manager import ScraperManager
from scraper.data_processor import clean_data, validate_data, remove_duplicates
from scraper.exporter import export_to_csv, export_to_excel, export_data
from scraper.http_client import fetch_page
from scraper.robots_checker import can_fetch
from scraper.logger import logger

__all__ = [
    "BaseScraper",
    "TestScraper",
    "AmazonScraper",
    "FlipkartScraper",
    "AlibabaScraper",
    "ScraperManager",
    "clean_data",
    "validate_data",
    "remove_duplicates",
    "export_to_csv",
    "export_to_excel",
    "export_data",
    "fetch_page",
    "can_fetch",
    "logger",
]
