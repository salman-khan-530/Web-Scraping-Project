"""
Centralized logging system for the E-Commerce Product Data Web Scraper.
"""

import logging
from pathlib import Path
from scraper.config import LOG_FILE, LOGS_DIR

# Ensure logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Create and configure logger
logger = logging.getLogger("web_scraper")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if module is reloaded
if not logger.handlers:
    # Log file handler with UTF-8 encoding
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
        mode="a"
    )

    # Log formatting
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console stream handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)