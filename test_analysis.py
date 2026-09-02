import pandas as pd

from scraper.analyzer import total_products


# Load cleaned product data
df = pd.read_csv("output/products.csv")


# Calculate total number of products
total = total_products(df)


print("Total Number of Products:")
print(total)