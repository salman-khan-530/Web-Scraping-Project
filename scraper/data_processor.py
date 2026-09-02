import pandas as pd


def convert_rating(rating):
    """
    Convert rating text into a numeric value.

    Args:
        rating: Rating value.

    Returns:
        int or None: Numeric rating from 1 to 5.
    """

    # If rating is already numeric, keep it
    if isinstance(rating, (int, float)):
        return rating

    # If rating is a list of rating classes
    if isinstance(rating, list) and len(rating) > 1:

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        return rating_map.get(rating[1])

    return None


def clean_text_encoding(text):
    """
    Fix common UTF-8 encoding issues in scraped text.

    Args:
        text (str): Text containing encoding problems.

    Returns:
        str: Cleaned text.
    """

    if not isinstance(text, str):
        return text

    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def clean_product_name(name):
    """
    Clean and standardize a product name.

    Args:
        name (str): Product name.

    Returns:
        str: Cleaned product name.
    """

    if not isinstance(name, str):
        return "Unknown"

    name = name.strip()

    name = " ".join(name.split())

    return name


def clean_price(price):
    """
    Clean and convert product price into a numeric value.

    Args:
        price (str): Product price.

    Returns:
        float or None: Numeric price.
    """

    if price is None:
        return None

    price = str(price)

    # Remove currency symbols and encoding characters
    price = price.replace("£", "")
    price = price.replace("Â", "")
    price = price.strip()

    try:
        return float(price)
    except ValueError:
        return None


def clean_rating(rating):
    """
    Convert and standardize product rating.

    Args:
        rating: Product rating.

    Returns:
        float or None: Rating between 1 and 5.
    """

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    # Handle text ratings
    if isinstance(rating, str):
        rating = rating.strip()

        if rating in rating_map:
            return rating_map[rating]

    # Handle numeric ratings
    try:
        rating = float(rating)

        if 1 <= rating <= 5:
            return rating

    except (ValueError, TypeError):
        pass

    return None


def clean_availability(availability):
    """
    Clean and standardize product availability.

    Args:
        availability (str): Product availability status.

    Returns:
        str: Standardized availability status.
    """

    if not isinstance(availability, str):
        return "Unknown"

    availability = availability.strip()

    availability = " ".join(availability.split())

    if not availability:
        return "Unknown"

    if "in stock" in availability.lower():
        return "In Stock"

    return availability.title()


def handle_missing_values(df):
    """Handle missing values in product data."""

    df["name"] = df["name"].fillna("Unknown")

    df["availability"] = df["availability"].fillna(
        "Unknown"
    )

    df["url"] = df["url"].fillna("N/A")

    df["category"] = df["category"].fillna(
        "Unknown"
    )

    df["description"] = df["description"].fillna(
        "Unknown"
    )

    return df


def remove_duplicates(df):
    """Remove duplicate product records."""

    before = len(df)

    # Remove completely identical records
    df = df.drop_duplicates()

    # Remove duplicate URLs only when a valid URL exists
    valid_url = (
        df["url"].notna()
        & (df["url"].str.strip() != "")
        & (df["url"] != "N/A")
    )

    df_with_url = df[valid_url].drop_duplicates(
        subset="url",
        keep="first"
    )

    df_without_url = df[~valid_url]

    df = pd.concat(
        [df_with_url, df_without_url],
        ignore_index=True
    )

    after = len(df)

    print(
        f"Duplicates removed: "
        f"{before - after}"
    )

    return df


def validate_data(df):
    """Validate product records and remove invalid data."""

    before = len(df)

    # Remove records without a valid product name
    df = df[
        df["name"].notna()
        & (df["name"].str.strip() != "")
    ]

    # Remove records without a valid URL
    df = df[
        df["url"].notna()
        & (df["url"].str.strip() != "")
        & (df["url"] != "N/A")
    ]

    # Keep only valid prices
    df = df[
        df["price"].notna()
        & (df["price"] >= 0)
    ]

    # Keep only valid ratings
    df = df[
        df["rating"].notna()
        & (df["rating"].between(1, 5))
    ]

    after = len(df)

    print(
        f"Invalid records removed: "
        f"{before - after}"
    )

    return df


def create_dataframe(products):
    """
    Convert scraped products into a Pandas DataFrame.

    Args:
        products (list): List of product dictionaries.

    Returns:
        pandas.DataFrame: Product DataFrame.
    """

    df = pd.DataFrame(products)

    return df


def clean_data(df):
    """
    Clean and standardize scraped product data.

    Args:
        df (pandas.DataFrame): Raw product DataFrame.

    Returns:
        pandas.DataFrame: Cleaned and validated DataFrame.
    """

    # Handle missing values
    df = handle_missing_values(df)

    # Clean product names
    df["name"] = df["name"].apply(clean_product_name)

    # Fix text encoding
    df["name"] = df["name"].apply(clean_text_encoding)
    df["availability"] = df["availability"].apply(clean_text_encoding)
    df["category"] = df["category"].apply(clean_text_encoding)
    df["description"] = df["description"].apply(clean_text_encoding)

    # Clean availability
    df["availability"] = df["availability"].apply(
        clean_availability
    )

    # Clean price
    df["price"] = df["price"].apply(clean_price)

    # Standardize rating
    df["rating"] = df["rating"].apply(clean_rating)

    # Remove duplicate products
    df = remove_duplicates(df)

    # Validate product data
    df = validate_data(df)

    return df