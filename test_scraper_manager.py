from scraper.scraper_manager import ScraperManager
from scraper.amazon_scraper import AmazonScraper
from scraper.alibaba_scraper import AlibabaScraper
from scraper.flipkart_scraper import FlipkartScraper


manager = ScraperManager()


print("Testing Scraper Manager")
print("=" * 50)


websites = {
    "amazon": AmazonScraper,
    "alibaba": AlibabaScraper,
    "flipkart": FlipkartScraper
}


all_passed = True


for website, expected_class in websites.items():

    scraper = manager.get_scraper(website)

    print(f"\nWebsite: {website}")
    print(f"Scraper Type: {type(scraper).__name__}")

    if isinstance(scraper, expected_class):

        print("Status: PASSED")

    else:

        print("Status: FAILED")
        all_passed = False


print("\n" + "=" * 50)


if all_passed:

    print("All scraper manager tests passed!")

else:

    print("Some scraper manager tests failed!")


# ==================================================
# TEST UNSUPPORTED WEBSITE
# ==================================================

unsupported_scraper = manager.get_scraper("unknown")


print("\nUnsupported Website Test:")
print(unsupported_scraper)


if unsupported_scraper is None:

    print("Unsupported website handled correctly!")

else:

    print("Unsupported website test failed!")
    all_passed = False