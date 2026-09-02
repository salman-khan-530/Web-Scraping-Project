from scraper.data_processor import clean_data
from scraper.http_client import fetch_page
from scraper.parser import (
    parse_html,
    extract_products,
    extract_product_details
)
import pandas as pd
from scraper.exporter import export_data


BASE_URL = "https://books.toscrape.com/"


# Get listing page
html = fetch_page(BASE_URL)

soup = parse_html(html)

products = extract_products(
    soup,
    BASE_URL
)


# Get details for each product
for product in products:

    product_html = fetch_page(product["url"])

    product_soup = parse_html(product_html)

    details = extract_product_details(
        product_soup
    )

    product.update(details)


print(f"Products found: {len(products)}")

for product in products[:3]:

    print("\nProduct:")

    for key, value in product.items():
        print(f"{key}: {value}")



df = pd.DataFrame(products)

# Clean and preprocess the data
df = clean_data(df)
        
print("\nDataFrame:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())


# Step 67 — Verify Required Fields

required_columns = [
    "name",
    "price",
    "rating",
    "availability",
    "url",
    "category",
    "description"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if not missing_columns:
    print("\nAll 7 required fields are present.")
else:
    print("\nMissing fields:")
    print(missing_columns)


# Step 80 — Export cleaned product data

export_data(
    df,
    "output/products.csv",
    "output/products.xlsx"
)