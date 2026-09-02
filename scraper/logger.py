import logging
import os


# Create logs directory if it does not exist
os.makedirs("logs", exist_ok=True)


# Create logger
logger = logging.getLogger("web_scraper")

logger.setLevel(logging.INFO)


# Prevent duplicate handlers
if not logger.handlers:

    # Log file handler
    file_handler = logging.FileHandler(
        "logs/scraper.log",
        encoding="utf-8"
    )

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    # Add handler
    logger.addHandler(file_handler)