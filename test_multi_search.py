from scraper.scraper_manager import ScraperManager


manager = ScraperManager()


print("Testing Multi-Website Search")
print("=" * 50)


# Search across all supported websites
results = manager.search_multiple(
    query="light",
    websites=[
        "books",
        "amazon",
        "alibaba",
        "flipkart"
    ],
    max_products=2
)


print(
    f"\nTotal results: {len(results)}"
)


for product in results:

    print(
        f"\nProduct: {product.get('name')}"
    )

    print(
        f"Source: {product.get('source')}"
    )


print("\n" + "=" * 50)

print(
    "Multi-website search test completed!"
)