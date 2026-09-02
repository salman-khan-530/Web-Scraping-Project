import pandas as pd


# Load exported CSV
df = pd.read_csv("output/products.csv")


# Display basic information
print("CSV loaded successfully!")

print("\nTotal products:")
print(len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 products:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())