from scraper.scraper_manager import ScraperManager
from scraper.books_scraper import BooksToScrapeScraper


manager = ScraperManager()

scraper = manager.get_scraper("books")


print("Selected Scraper:")
print(scraper)

print("\nScraper Type:")
print(type(scraper).__name__)


if isinstance(scraper, BooksToScrapeScraper):
    print("\nScraper Manager test passed!")
else:
    print("\nScraper Manager test failed!")


unsupported_scraper = manager.get_scraper("amazon")

print("\nUnsupported Website Test:")
print(unsupported_scraper)


if unsupported_scraper is None:
    print("Unsupported website handled correctly!")
else:
    print("Unsupported website test failed!")