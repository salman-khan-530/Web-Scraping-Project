"""
Data analysis module for computing summary statistics and insights on scraped product datasets.
"""

import pandas as pd


def total_products(df):
    """Return total number of products."""
    return len(df) if df is not None else 0


def average_price(df):
    """Return average product price, or 0.0 if not available."""
    if df is None or "price" not in df.columns or df["price"].dropna().empty:
        return 0.0
    return round(float(df["price"].mean()), 2)


def minimum_price(df):
    """Return minimum product price, or 0.0 if not available."""
    if df is None or "price" not in df.columns or df["price"].dropna().empty:
        return 0.0
    return round(float(df["price"].min()), 2)


def maximum_price(df):
    """Return maximum product price, or 0.0 if not available."""
    if df is None or "price" not in df.columns or df["price"].dropna().empty:
        return 0.0
    return round(float(df["price"].max()), 2)


def average_rating(df):
    """Return average rating, or 0.0 if not available."""
    if df is None or "rating" not in df.columns or df["rating"].dropna().empty:
        return 0.0
    return round(float(df["rating"].mean()), 2)


def most_common_rating(df):
    """Return the most frequent rating."""
    if df is None or "rating" not in df.columns or df["rating"].dropna().empty:
        return None
    mode_val = df["rating"].mode()
    return float(mode_val.iloc[0]) if not mode_val.empty else None


def available_products(df):
    """Return count of in-stock products."""
    if df is None or "availability" not in df.columns:
        return 0
    return int(df["availability"].astype(str).str.lower().str.contains("in stock").sum())


def unavailable_products(df):
    """Return count of out-of-stock or unavailable products."""
    if df is None:
        return 0
    return total_products(df) - available_products(df)


def most_common_category(df):
    """Return the most frequent product category."""
    if df is None or "category" not in df.columns:
        return "Unknown"
    valid_categories = df["category"].dropna()
    valid_categories = valid_categories[valid_categories != "Unknown"]
    if valid_categories.empty:
        return "Unknown"
    return str(valid_categories.mode().iloc[0])


def highest_rated_products(df, top_n=5):
    """Return top-rated products."""
    if df is None or "rating" not in df.columns or df["rating"].dropna().empty:
        return pd.DataFrame()
    max_rating = df["rating"].max()
    return df[df["rating"] == max_rating].head(top_n)


def lowest_priced_products(df, top_n=5):
    """Return lowest-priced products."""
    if df is None or "price" not in df.columns or df["price"].dropna().empty:
        return pd.DataFrame()
    min_price = df["price"].min()
    return df[df["price"] == min_price].head(top_n)


def most_expensive_products(df, top_n=5):
    """Return highest-priced products."""
    if df is None or "price" not in df.columns or df["price"].dropna().empty:
        return pd.DataFrame()
    max_price = df["price"].max()
    return df[df["price"] == max_price].head(top_n)


def generate_summary(df):
    """
    Generate comprehensive statistical summary.
    """
    return {
        "total_products": total_products(df),
        "average_price": average_price(df),
        "minimum_price": minimum_price(df),
        "maximum_price": maximum_price(df),
        "average_rating": average_rating(df),
        "most_common_rating": most_common_rating(df),
        "available_products": available_products(df),
        "unavailable_products": unavailable_products(df),
        "most_common_category": most_common_category(df),
    }