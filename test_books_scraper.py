from scraper.books_scraper import BooksToScrapeScraper


scraper = BooksToScrapeScraper()


products = scraper.search_products(
    query="books",
    max_products=2
)


print("\nStandardized Products:")
print("======================")

for product in products:

    print("\n", product)