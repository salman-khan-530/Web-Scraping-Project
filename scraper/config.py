# Website configuration

BASE_URL = "https://books.toscrape.com/"


# Scraper configuration

DEFAULT_MAX_PRODUCTS = 20

DEFAULT_TIMEOUT = 10

REQUEST_DELAY = 1


# HTTP request headers

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

# Amazon configuration

AMAZON_BASE_URL = "https://www.amazon.com/"

AMAZON_SEARCH_URL = (
    "https://www.amazon.com/s"
)

AMAZON_SOURCE_NAME = "Amazon"


# Output configuration

CSV_OUTPUT = "output/products.csv"

EXCEL_OUTPUT = "output/products.xlsx"