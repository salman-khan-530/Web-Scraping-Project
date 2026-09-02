import pandas as pd

from scraper.analyzer import (
    generate_summary,
    highest_rated_products,
    lowest_priced_products
)


# Load cleaned product data
df = pd.read_csv("output/products.csv")


# Generate summary
summary = generate_summary(df)


# Display summary
print("PRODUCT ANALYSIS SUMMARY")
print("=" * 30)

for key, value in summary.items():
    print(f"{key}: {value}")


# Find highest rated products
highest_rated = highest_rated_products(df)

print("\nHIGHEST RATED PRODUCTS")
print("=" * 30)

print(
    highest_rated[
        ["name", "rating", "price"]
    ].to_string(index=False)
)


# Find lowest priced products
lowest_priced = lowest_priced_products(df)

print("\nLOWEST PRICED PRODUCTS")
print("=" * 30)

print(
    lowest_priced[
        ["name", "rating", "price"]
    ].to_string(index=False)
)