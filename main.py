import argparse

import pandas as pd

from scraper.scraper_manager import ScraperManager

from scraper.config import (
    CSV_OUTPUT,
    EXCEL_OUTPUT
)

from scraper.data_processor import clean_data

from scraper.exporter import (
    export_to_csv,
    export_to_excel
)

from scraper.analyzer import (
    generate_summary,
    highest_rated_products,
    lowest_priced_products
)

from scraper.visualizer import (
    plot_price_distribution,
    plot_rating_distribution,
    plot_price_vs_rating,
    plot_products_by_category
)

from scraper.logger import logger


def main():

    # ==========================================
    # Create command-line parser
    # ==========================================

    parser = argparse.ArgumentParser(
        description=(
            "E-Commerce Product Data "
            "Web Scraper"
        )
    )


    # ==========================================
    # Product search query
    # ==========================================

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Product search query."
    )


    # ==========================================
    # Websites
    # ==========================================

    parser.add_argument(
        "--websites",
        nargs="+",
        default=["books"],
        choices=[
            "books",
            "amazon",
            "alibaba",
            "flipkart"
        ],
        help=(
            "Websites to search. "
            "You can select one or multiple websites."
        )
    )


    # ==========================================
    # Maximum products per website
    # ==========================================

    parser.add_argument(
        "--max-products",
        type=int,
        default=20,
        help=(
            "Maximum number of products to collect "
            "from each website."
        )
    )


    # ==========================================
    # Parse arguments
    # ==========================================

    args = parser.parse_args()


    # ==========================================
    # Validate max products
    # ==========================================

    if args.max_products <= 0:

        print(
            "\nError: --max-products must be "
            "greater than zero."
        )

        return


    # ==========================================
    # Validate query
    # ==========================================

    if not args.query.strip():

        print(
            "\nError: --query cannot be empty."
        )

        return


    # ==========================================
    # Display application information
    # ==========================================

    print("\n" + "=" * 60)

    print(
        "       E-COMMERCE PRODUCT DATA WEB SCRAPER"
    )

    print("=" * 60)


    print(
        f"\nSearch query: {args.query}"
    )

    print(
        f"Websites: "
        f"{', '.join(args.websites)}"
    )

    print(
        f"Maximum products per website: "
        f"{args.max_products}"
    )


    # ==========================================
    # Create scraper manager
    # ==========================================

    manager = ScraperManager()


    # ==========================================
    # Search selected websites
    # ==========================================

    logger.info(
        "Starting multi-website search..."
    )

    products = manager.search_multiple(
        query=args.query,
        websites=args.websites,
        max_products=args.max_products
    )


    print(
        f"\nProducts collected: "
        f"{len(products)}"
    )


    # ==========================================
    # Stop if no products found
    # ==========================================

    if not products:

        print(
            "\nNo products were collected."
        )

        return


    # ==========================================
    # Create DataFrame
    # ==========================================

    df = pd.DataFrame(
        products
    )


    print(
        f"\nDataFrame created: "
        f"{df.shape[0]} rows × "
        f"{df.shape[1]} columns"
    )


    # ==========================================
    # Required columns
    # ==========================================

    required_columns = [
        "name",
        "price",
        "rating",
        "availability",
        "url",
        "category",
        "description",
        "source"
    ]


    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]


    if missing_columns:

        logger.error(
            f"Missing required columns: "
            f"{missing_columns}"
        )

        print(
            "\nRequired columns are missing:"
        )

        print(
            missing_columns
        )

        return


    print(
        "\nAll required columns are present."
    )


    # ==========================================
    # Clean and process data
    # ==========================================

    print(
        "\nCleaning and processing data..."
    )


    df = clean_data(
        df
    )


    print(
        f"Data cleaning completed. "
        f"Final records: {len(df)}"
    )


    # ==========================================
    # Stop if no valid records remain
    # ==========================================

    if df.empty:

        print(
            "\nNo valid records remain "
            "after data cleaning."
        )

        return


    # ==========================================
    # Export data
    # ==========================================

    print(
        "\nExporting data..."
    )


    try:

        export_to_csv(
            df,
            CSV_OUTPUT
        )

        export_to_excel(
            df,
            EXCEL_OUTPUT
        )

    except Exception as e:

        logger.error(
            f"Data export failed: {e}"
        )

        print(
            f"\nExport failed: {e}"
        )

        return


    # ==========================================
    # Analysis
    # ==========================================

    print(
        "\nRunning analysis..."
    )


    summary = generate_summary(
        df
    )


    highest_rated = highest_rated_products(
        df
    )


    lowest_priced = lowest_priced_products(
        df
    )


    # ==========================================
    # Display analysis summary
    # ==========================================

    print(
        "\nAnalysis Summary"
    )

    print(
        "-" * 40
    )


    for key, value in summary.items():

        print(
            f"{key}: {value}"
        )


    # ==========================================
    # Highest rated products
    # ==========================================

    print(
        "\nHighest Rated Products"
    )

    print(
        "-" * 40
    )


    if not highest_rated.empty:

        print(
            highest_rated[
                [
                    "name",
                    "rating",
                    "price"
                ]
            ].to_string(
                index=False
            )
        )

    else:

        print(
            "No highest-rated products found."
        )


    # ==========================================
    # Lowest priced products
    # ==========================================

    print(
        "\nLowest Priced Products"
    )

    print(
        "-" * 40
    )


    if not lowest_priced.empty:

        print(
            lowest_priced[
                [
                    "name",
                    "rating",
                    "price"
                ]
            ].to_string(
                index=False
            )
        )

    else:

        print(
            "No lowest-priced products found."
        )


    # ==========================================
    # Visualizations
    # ==========================================

    print(
        "\nGenerating visualizations..."
    )


    try:

        plot_price_distribution(
            df
        )

        plot_rating_distribution(
            df
        )

        plot_price_vs_rating(
            df
        )

        plot_products_by_category(
            df
        )

    except Exception as e:

        logger.error(
            f"Visualization failed: {e}"
        )

        print(
            f"\nVisualization error: {e}"
        )


    # ==========================================
    # Completion message
    # ==========================================

    print(
        "\n" + "=" * 60
    )

    print(
        "       SCRAPING COMPLETED SUCCESSFULLY"
    )

    print(
        "=" * 60
    )

    print(
        f"Total products processed: "
        f"{len(df)}"
    )

    print(
        f"CSV output: {CSV_OUTPUT}"
    )

    print(
        f"Excel output: {EXCEL_OUTPUT}"
    )


if __name__ == "__main__":
    main()