import matplotlib.pyplot as plt


def plot_price_distribution(df):
    """
    Plot the distribution of product prices.
    """

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["price"],
        bins=10,
        edgecolor="black"
    )

    plt.title(
        "Product Price Distribution"
    )

    plt.xlabel(
        "Price"
    )

    plt.ylabel(
        "Number of Products"
    )

    plt.tight_layout()

    plt.show()


def plot_rating_distribution(df):
    """
    Plot the distribution of product ratings.
    """

    plt.figure(figsize=(8, 5))

    df["rating"].value_counts().sort_index().plot(
        kind="bar"
    )

    plt.title(
        "Product Rating Distribution"
    )

    plt.xlabel(
        "Rating"
    )

    plt.ylabel(
        "Number of Products"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.show()


def plot_price_vs_rating(df):
    """
    Plot product price against product rating.
    """

    plt.figure(figsize=(8, 5))

    plt.scatter(
        df["rating"],
        df["price"]
    )

    plt.title(
        "Price vs Rating"
    )

    plt.xlabel(
        "Rating"
    )

    plt.ylabel(
        "Price"
    )

    plt.tight_layout()

    plt.show()


def plot_products_by_category(df):
    """
    Plot the number of products in each category.
    """

    category_counts = (
        df["category"]
        .value_counts()
    )

    plt.figure(figsize=(10, 6))

    category_counts.plot(
        kind="bar"
    )

    plt.title(
        "Products by Category"
    )

    plt.xlabel(
        "Category"
    )

    plt.ylabel(
        "Number of Products"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()