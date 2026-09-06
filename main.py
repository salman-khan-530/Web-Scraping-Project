"""
Command-line interface for the E-Commerce Product Data Web Scraper.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

# Reconfigure stdout/stderr for UTF-8 on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scraper.scraper_manager import ScraperManager
from scraper.config import CSV_OUTPUT, EXCEL_OUTPUT
from scraper.data_processor import clean_data
from scraper.exporter import export_to_csv, export_to_excel
from scraper.analyzer import (
    generate_summary,
    highest_rated_products,
    lowest_priced_products,
    most_expensive_products
)
from scraper.visualizer import show_all_visualizations
from scraper.logger import logger


def main():
    parser = argparse.ArgumentParser(
        description="E-Commerce Product Data Web Scraper CLI"
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Product search keyword (e.g. 'light', 'python', 'book')."
    )

    parser.add_argument(
        "--websites",
        nargs="+",
        default=["test"],
        choices=["test", "amazon", "alibaba", "flipkart"],
        help="Websites to search. Options: test, amazon, alibaba, flipkart. Default: test."
    )

    parser.add_argument(
        "--max-products",
        type=int,
        default=20,
        help="Maximum number of products to collect per website (default: 20)."
    )

    parser.add_argument(
        "--save-plots",
        action="store_true",
        help="Save static visualization charts into output/plots/ directory."
    )

    args = parser.parse_args()

    # Input validations
    if args.max_products <= 0:
        print("\n[Error] --max-products must be greater than zero.")
        sys.exit(1)

    query = args.query.strip()
    if not query:
        print("\n[Error] --query cannot be empty.")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("        E-COMMERCE PRODUCT DATA WEB SCRAPER")
    print("=" * 65)
    print(f"  Search Query : {query}")
    print(f"  Websites     : {', '.join(args.websites)}")
    print(f"  Max Products : {args.max_products}")
    print("=" * 65)

    manager = ScraperManager()

    # Check for unconfigured APIs among selected websites
    for site in args.websites:
        if site != "test" and not manager.is_configured(site):
            scraper = manager.get_scraper(site)
            name = scraper.source_name if scraper else site.capitalize()
            print(f"\n[Notice] {name} API is not configured.")
            print(f"         Set {scraper.env_var} in your environment or .env file to enable official access.")

    logger.info(f"Starting CLI scrape run: query='{query}', websites={args.websites}")

    # Collect raw products
    raw_products = manager.search_multiple(
        query=query,
        websites=args.websites,
        max_products=args.max_products
    )

    print(f"\nCollected {len(raw_products)} raw product record(s).")

    if not raw_products:
        print("\nNo matching products found. Try a different query or ensure your API credentials are set.")
        return

    # Create DataFrame and clean data
    raw_df = pd.DataFrame(raw_products)
    print("\nCleaning, standardizing, and validating product data...")
    cleaned_df = clean_data(raw_df)

    if cleaned_df.empty:
        print("\nNo valid records remained after cleaning and validation.")
        return

    print(f"Data cleaning complete. Clean records: {len(cleaned_df)}")

    # Export
    print("\nExporting cleaned dataset...")
    try:
        export_to_csv(cleaned_df, CSV_OUTPUT)
        export_to_excel(cleaned_df, EXCEL_OUTPUT)
        print(f" -> CSV output   : {CSV_OUTPUT}")
        print(f" -> Excel output : {EXCEL_OUTPUT}")
    except Exception as e:
        logger.error(f"Export failure: {e}")
        print(f"[Error] Export failed: {e}")
        return

    # Analysis Summary
    print("\n" + "-" * 40)
    print("          ANALYSIS SUMMARY")
    print("-" * 40)
    summary = generate_summary(cleaned_df)
    for key, val in summary.items():
        label = key.replace("_", " ").title()
        if isinstance(val, float):
            print(f"  {label:<24}: {val:.2f}")
        else:
            print(f"  {label:<24}: {val}")

    # Top & Lowest products (using safe ASCII formatting)
    highest = highest_rated_products(cleaned_df, top_n=3)
    if not highest.empty:
        print("\n  Top-Rated Products:")
        for _, row in highest.iterrows():
            r_str = f"{row['rating']} stars" if pd.notna(row['rating']) else "N/A"
            p_str = f"GBP {row['price']:.2f}" if pd.notna(row['price']) else "N/A"
            print(f"   * {row['name']} ({r_str}) - {p_str}")

    lowest = lowest_priced_products(cleaned_df, top_n=3)
    if not lowest.empty:
        print("\n  Lowest-Priced Products:")
        for _, row in lowest.iterrows():
            r_str = f"{row['rating']} stars" if pd.notna(row['rating']) else "N/A"
            p_str = f"GBP {row['price']:.2f}" if pd.notna(row['price']) else "N/A"
            print(f"   * {row['name']} - {p_str} ({r_str})")

    # Optional plot saving
    if args.save_plots:
        plots_dir = "output/plots"
        print(f"\nGenerating and saving plot figures to {plots_dir}...")
        show_all_visualizations(cleaned_df, save_dir=plots_dir, show=False)
        print(" -> Charts saved successfully.")

    print("\n" + "=" * 65)
    print("          EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()