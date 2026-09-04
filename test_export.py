import pandas as pd

from scraper.exporter import export_data


# Create sample product data
data = [
    {
        "name": "Example Product",
        "price": 25.99,
        "rating": 4,
        "availability": "In Stock",
        "url": "https://example.com/product",
        "category": "Electronics",
        "description": "Example product description."
    },
    {
        "name": "Another Product",
        "price": 39.99,
        "rating": 5,
        "availability": "In Stock",
        "url": "https://example.com/product2",
        "category": "Science",
        "description": "Another product description."
    }
]


# Create DataFrame
df = pd.DataFrame(data)


# Export data to CSV and Excel
export_data(
    df,
    "output/test_products.csv",
    "output/test_products.xlsx"
)