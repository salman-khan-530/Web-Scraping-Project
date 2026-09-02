import pandas as pd


# Load exported Excel file
df = pd.read_excel("output/products.xlsx")


# Display basic information
print("Excel file loaded successfully!")

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