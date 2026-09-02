import pandas as pd

from scraper.visualizer import show_all_visualizations


# Load cleaned product data
df = pd.read_csv("output/products.csv")


# Display dataset information
print("DATASET INFORMATION")
print("=" * 30)

print(f"Total products: {len(df)}")

print("\nColumns:")
print(df.columns.tolist())


# Display all visualizations
print("\nDisplaying visualizations...")

show_all_visualizations(df)