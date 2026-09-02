import pandas as pd


def total_products(df):
    """Return the total number of products."""
    return len(df)


def average_price(df):
    """Return the average product price."""
    return df["price"].mean()


def minimum_price(df):
    """Return the minimum product price."""
    return df["price"].min()


def maximum_price(df):
    """Return the maximum product price."""
    return df["price"].max()


def most_common_rating(df):
    """Return the most common product rating."""

    mode = df["rating"].mode()

    if not mode.empty:
        return mode.iloc[0]

    return None


def available_products(df):
    """Return the number of available products."""

    available = df["availability"].str.contains(
        "in stock",
        case=False,
        na=False
    )

    return available.sum()


def highest_rated_products(df):
    """Return products with the highest rating."""

    highest_rating = df["rating"].max()

    return df[
        df["rating"] == highest_rating
    ]


def lowest_priced_products(df):
    """Return products with the lowest price."""

    lowest_price = df["price"].min()

    return df[
        df["price"] == lowest_price
    ]


def generate_summary(df):
    """Generate basic statistical summary."""

    summary = {
        "total_products": total_products(df),
        "average_price": average_price(df),
        "minimum_price": minimum_price(df),
        "maximum_price": maximum_price(df),
        "most_common_rating": most_common_rating(df),
        "available_products": available_products(df)
    }

    return summary