import pandas as pd

from scraper.analyzer import (
    generate_summary
)


# Load cleaned product data
df = pd.read_csv("output/products.csv")


# Generate analysis summary
summary = generate_summary(df)


# Display summary
print("Product Analysis Summary")
print("=" * 30)

for key, value in summary.items():
    print(f"{key}: {value}")