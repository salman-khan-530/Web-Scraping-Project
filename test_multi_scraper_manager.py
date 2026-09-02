from scraper.scraper_manager import ScraperManager

from scraper.books_scraper import BooksToScrapeScraper

from scraper.amazon_scraper import AmazonScraper

from scraper.alibaba_scraper import AlibabaScraper

from scraper.flipkart_scraper import FlipkartScraper


manager = ScraperManager()


websites = {
    "books": BooksToScrapeScraper,
    "amazon": AmazonScraper,
    "alibaba": AlibabaScraper,
    "flipkart": FlipkartScraper
}


print("Testing Multi-Website Scraper Manager")
print("=" * 50)


all_passed = True


for website, expected_class in websites.items():

    scraper = manager.get_scraper(
        website
    )

    print(
        f"\nWebsite: {website}"
    )

    print(
        f"Scraper: "
        f"{type(scraper).__name__}"
    )

    if isinstance(
        scraper,
        expected_class
    ):

        print("Status: PASSED")

    else:

        print("Status: FAILED")

        all_passed = False


print("\n" + "=" * 50)


if all_passed:

    print(
        "All scraper manager tests passed!"
    )

else:

    print(
        "Some scraper manager tests failed!"
    )