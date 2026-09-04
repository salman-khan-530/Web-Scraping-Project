import streamlit as st
import pandas as pd

from io import BytesIO

from scraper.scraper_manager import ScraperManager


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="E-Commerce Product Scraper",
    page_icon="🛒",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("🛒 E-Commerce Product Scraper")

st.write(
    "Scrape, clean, analyze, and export "
    "e-commerce product data."
)


# ==================================================
# INITIALIZE SCRAPER MANAGER
# ==================================================

scraper_manager = ScraperManager()


# ==================================================
# SESSION STATE
# ==================================================

if "products" not in st.session_state:
    st.session_state.products = None


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("⚙️ Scraping Settings")

website = st.sidebar.selectbox(
    "Select Website",
    [
        "Amazon",
        "Flipkart",
        "Alibaba"
    ]
)

query = st.sidebar.text_input(
    "Search Query",
    placeholder="Enter product name..."
)

max_products = st.sidebar.number_input(
    "Maximum Products",
    min_value=1,
    max_value=100,
    value=10,
    step=1
)


# ==================================================
# START SCRAPING
# ==================================================

if st.sidebar.button("🚀 Start Scraping"):

    # ----------------------------------------------
    # Validate Search Query
    # ----------------------------------------------

    if not query.strip():

        st.warning(
            "⚠️ Please enter a search query."
        )

    else:

        # ------------------------------------------
        # Website Mapping
        # ------------------------------------------

        website_map = {
            "Amazon": "amazon",
            "Flipkart": "flipkart",
            "Alibaba": "alibaba"
        }

        selected_website = website_map[website]

        # ------------------------------------------
        # Scraping
        # ------------------------------------------

        with st.spinner(
            f"🔎 Scraping {website}..."
        ):

            try:

                scraper = scraper_manager.get_scraper(
                    selected_website
                )

                # ----------------------------------
                # Check Scraper
                # ----------------------------------

                if scraper is None:

                    st.error(
                        "❌ Selected website is not supported."
                    )

                else:

                    # ------------------------------
                    # Search Products
                    # ------------------------------

                    products = scraper.search_products(
                        query.strip(),
                        max_products
                    )

                    # Save products in session state
                    st.session_state.products = products

            except Exception as e:

                st.error(
                    f"❌ An error occurred: {e}"
                )


# ==================================================
# DISPLAY RESULTS
# ==================================================

if st.session_state.products:

    products = st.session_state.products

    st.success(
        f"✅ Found {len(products)} products!"
    )

    # ----------------------------------------------
    # Convert to DataFrame
    # ----------------------------------------------

    df = pd.DataFrame(products)


    # ==================================================
    # SUMMARY METRICS
    # ==================================================

    st.subheader(
        "📊 Scraping Summary"
    )

    # ----------------------------------------------
    # Total Products
    # ----------------------------------------------

    total_products = len(df)


    # ----------------------------------------------
    # Clean Price
    # ----------------------------------------------

    if "price" in df.columns:

        price_numeric = (
            df["price"]
            .astype(str)
            .str.replace(
                "Â£",
                "",
                regex=False
            )
            .str.replace(
                "Ã‚Â£",
                "",
                regex=False
            )
            .str.replace(
                "£",
                "",
                regex=False
            )
            .str.strip()
        )

        price_numeric = pd.to_numeric(
            price_numeric,
            errors="coerce"
        )

        average_price = price_numeric.mean()

    else:

        average_price = None


    # ----------------------------------------------
    # Average Rating
    # ----------------------------------------------

    if "rating" in df.columns:

        average_rating = pd.to_numeric(
            df["rating"],
            errors="coerce"
        ).mean()

    else:

        average_rating = None


    # ----------------------------------------------
    # Available Products
    # ----------------------------------------------

    if "availability" in df.columns:

        available_products = (
            df["availability"]
            .astype(str)
            .str.lower()
            .str.contains(
                "in stock"
            )
            .sum()
        )

    else:

        available_products = 0


    # ----------------------------------------------
    # Metric Columns
    # ----------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📦 Total Products",
            total_products
        )


    with col2:

        if pd.notna(average_price):

            st.metric(
                "💰 Average Price",
                f"£{average_price:.2f}"
            )

        else:

            st.metric(
                "💰 Average Price",
                "N/A"
            )


    with col3:

        if pd.notna(average_rating):

            st.metric(
                "⭐ Average Rating",
                f"{average_rating:.1f}"
            )

        else:

            st.metric(
                "⭐ Average Rating",
                "N/A"
            )


    with col4:

        st.metric(
            "✅ In Stock",
            available_products
        )


    # ==================================================
    # PRODUCT RESULTS
    # ==================================================

    st.subheader(
        "📦 Scraped Products"
    )


    # ----------------------------------------------
    # Create Display Copy
    # ----------------------------------------------

    display_df = df.copy()


    # ----------------------------------------------
    # Clean Price Encoding For Display
    # ----------------------------------------------

    if "price" in display_df.columns:

        display_df["price"] = (
            display_df["price"]
            .astype(str)
            .str.replace(
                "Ã‚Â£",
                "£",
                regex=False
            )
            .str.replace(
                "Â£",
                "£",
                regex=False
            )
        )


    # ----------------------------------------------
    # Shorten Description
    # ----------------------------------------------

    if "description" in display_df.columns:

        display_df["description"] = (
            display_df["description"]
            .astype(str)
            .apply(
                lambda text:
                (
                    text[:150] + "..."
                    if len(text) > 150
                    else text
                )
            )
        )


    # ----------------------------------------------
    # Display Product Table
    # ----------------------------------------------

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "url": st.column_config.LinkColumn(
                "Product URL"
            )
        }
    )


    # ==================================================
    # DOWNLOAD BUTTONS
    # ==================================================

    st.subheader(
        "⬇️ Download Data"
    )


    # ----------------------------------------------
    # CSV Download
    # ----------------------------------------------

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")


    # ----------------------------------------------
    # Excel Download
    # ----------------------------------------------

    excel_buffer = BytesIO()


    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Products"
        )


    excel_data = excel_buffer.getvalue()


    # ----------------------------------------------
    # Download Columns
    # ----------------------------------------------

    download_col1, download_col2 = st.columns(2)


    with download_col1:

        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="products.csv",
            mime="text/csv"
        )


    with download_col2:

        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name="products.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )


# ==================================================
# NO RESULTS / INITIAL INFORMATION
# ==================================================

else:

    st.info(
        "👈 Configure the scraping options "
        "from the sidebar and click "
        "**Start Scraping**."
    )