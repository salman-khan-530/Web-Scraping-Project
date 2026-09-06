"""
Matplotlib-based visualizer for static charts and offline reporting.
"""

from pathlib import Path
import matplotlib
# Use non-interactive Agg backend if running in headless environment
import matplotlib.pyplot as plt

from scraper.logger import logger


def _prepare_canvas(figsize=(8, 5)):
    plt.figure(figsize=figsize)


def plot_price_distribution(df, save_path=None, show=True):
    """Plot distribution of product prices."""
    if df is None or "price" not in df.columns or df["price"].dropna().empty:
        logger.warning("Price data missing for visualization.")
        return

    _prepare_canvas((8, 5))
    plt.hist(df["price"].dropna(), bins=10, edgecolor="black", color="#3B82F6")
    plt.title("Product Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Number of Products")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        logger.info(f"Price distribution plot saved to {save_path}")

    if show:
        plt.show()
    plt.close()


def plot_rating_distribution(df, save_path=None, show=True):
    """Plot distribution of product ratings."""
    if df is None or "rating" not in df.columns or df["rating"].dropna().empty:
        logger.warning("Rating data missing for visualization.")
        return

    _prepare_canvas((8, 5))
    counts = df["rating"].dropna().value_counts().sort_index()
    counts.plot(kind="bar", color="#10B981", edgecolor="black")
    plt.title("Product Rating Distribution")
    plt.xlabel("Rating (Stars)")
    plt.ylabel("Number of Products")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        logger.info(f"Rating distribution plot saved to {save_path}")

    if show:
        plt.show()
    plt.close()


def plot_price_vs_rating(df, save_path=None, show=True):
    """Scatter plot of price vs. rating."""
    if df is None or "price" not in df.columns or "rating" not in df.columns:
        return

    subset = df.dropna(subset=["price", "rating"])
    if subset.empty:
        return

    _prepare_canvas((8, 5))
    plt.scatter(subset["rating"], subset["price"], color="#8B5CF6", alpha=0.8, edgecolors="black")
    plt.title("Price vs. Rating")
    plt.xlabel("Rating")
    plt.ylabel("Price")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)

    if show:
        plt.show()
    plt.close()


def plot_products_by_category(df, save_path=None, show=True):
    """Bar plot of product categories."""
    if df is None or "category" not in df.columns:
        return

    valid = df[df["category"].notna() & (df["category"] != "Unknown")]
    if valid.empty:
        return

    _prepare_canvas((10, 6))
    counts = valid["category"].value_counts().head(10)
    counts.plot(kind="bar", color="#F59E0B", edgecolor="black")
    plt.title("Top Categories")
    plt.xlabel("Category")
    plt.ylabel("Number of Products")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)

    if show:
        plt.show()
    plt.close()


def show_all_visualizations(df, save_dir=None, show=False):
    """
    Generate and display or save all available static visualizations.
    """
    if df is None or df.empty:
        logger.warning("No data provided for visualizations.")
        return

    out_path = Path(save_dir) if save_dir else None
    plot_price_distribution(df, save_path=out_path / "price_dist.png" if out_path else None, show=show)
    plot_rating_distribution(df, save_path=out_path / "rating_dist.png" if out_path else None, show=show)
    plot_price_vs_rating(df, save_path=out_path / "price_vs_rating.png" if out_path else None, show=show)
    plot_products_by_category(df, save_path=out_path / "category_dist.png" if out_path else None, show=show)