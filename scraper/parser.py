from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.logger import logger


def parse_html(html):
    """
    Convert HTML text into a BeautifulSoup object.

    Returns:
        BeautifulSoup: Parsed HTML.
        None: If HTML is empty or invalid.
    """

    if not html:

        logger.warning(
            "No HTML content received for parsing."
        )

        return None

    try:

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        logger.info(
            "HTML parsed successfully."
        )

        return soup

    except Exception as e:

        logger.error(
            f"HTML parsing error: {e}"
        )

        return None


def extract_products(soup, base_url):
    """
    Extract product information from a listing page.

    Returns:
        list: List of product dictionaries.
    """

    products = []

    if soup is None:

        logger.warning(
            "Cannot extract products because soup is None."
        )

        return products

    product_items = soup.select(
        "article.product_pod"
    )

    logger.info(
        f"Product elements found: {len(product_items)}"
    )

    if not product_items:

        logger.warning(
            "No product elements found on the page."
        )

    for item in product_items:

        # --------------------------------------------------
        # PRODUCT NAME
        # --------------------------------------------------

        name_tag = item.select_one(
            "h3 a"
        )

        if name_tag:

            name = name_tag.get(
                "title",
                ""
            ).strip()

            if not name:

                name = name_tag.get_text(
                    strip=True
                )

            if not name:

                logger.warning(
                    "Product name is empty."
                )

        else:

            name = None

            logger.warning(
                "Product name not found."
            )

        # --------------------------------------------------
        # PRODUCT PRICE
        # --------------------------------------------------

        price_tag = item.select_one(
            ".price_color"
        )

        if price_tag:

            price = price_tag.get_text(
                strip=True
            )

            if not price:

                logger.warning(
                    f"Product price is empty: {name}"
                )

        else:

            price = None

            logger.warning(
                f"Product price not found: {name}"
            )

        # --------------------------------------------------
        # PRODUCT RATING
        # --------------------------------------------------

        rating_tag = item.select_one(
            "p.star-rating"
        )

        rating = None

        if rating_tag:

            rating_classes = rating_tag.get(
                "class",
                []
            )

            rating_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }

            for rating_name, rating_value in rating_map.items():

                if rating_name in rating_classes:

                    rating = rating_value

                    break

        if rating is None:

            logger.warning(
                f"Product rating not found: {name}"
            )

        # --------------------------------------------------
        # AVAILABILITY
        # --------------------------------------------------

        availability_tag = item.select_one(
            ".instock.availability"
        )

        if availability_tag:

            availability = availability_tag.get_text(
                " ",
                strip=True
            )

            if not availability:

                logger.warning(
                    f"Availability is empty: {name}"
                )

        else:

            availability = None

            logger.warning(
                f"Availability not found: {name}"
            )

        # --------------------------------------------------
        # PRODUCT URL
        # --------------------------------------------------

        url = None

        if name_tag:

            product_href = name_tag.get(
                "href"
            )

            if product_href:

                # Convert relative URL to absolute URL
                url = urljoin(
                    base_url,
                    product_href
                )

                # Books to Scrape sometimes provides
                # product URLs without the /catalogue/
                # directory. Correct that structure.
                if (
                    url.startswith(
                        "https://books.toscrape.com/"
                    )
                    and "/catalogue/" not in url
                ):

                    product_path = url.replace(
                        "https://books.toscrape.com/",
                        ""
                    )

                    url = urljoin(
                        "https://books.toscrape.com/catalogue/",
                        product_path
                    )

                logger.info(
                    f"Product URL resolved: {url}"
                )

        if url is None:

            logger.warning(
                f"Product URL not found: {name}"
            )

        # --------------------------------------------------
        # CREATE PRODUCT
        # --------------------------------------------------

        product = {
            "name": name,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": url
        }

        products.append(
            product
        )

    logger.info(
        f"Successfully extracted "
        f"{len(products)} products."
    )

    return products


def extract_product_details(soup):
    """
    Extract category and description
    from a product detail page.

    Returns:
        dict: Product category and description.
    """

    category = None
    description = None

    if soup is None:

        logger.warning(
            "Cannot extract product details because soup is None."
        )

        return {
            "category": category,
            "description": description
        }

    # --------------------------------------------------
    # CATEGORY
    # --------------------------------------------------

    breadcrumb_links = soup.select(
        ".breadcrumb li a"
    )

    if len(breadcrumb_links) >= 3:

        category = breadcrumb_links[2].get_text(
            strip=True
        )

        if not category:

            logger.warning(
                "Product category is empty."
            )

    else:

        logger.warning(
            "Product category not found."
        )

    # --------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------

    description_heading = soup.find(
        "div",
        id="product_description"
    )

    if description_heading:

        description_tag = (
            description_heading.find_next_sibling(
                "p"
            )
        )

        if description_tag:

            description = description_tag.get_text(
                " ",
                strip=True
            )

            if not description:

                logger.warning(
                    "Product description is empty."
                )

        else:

            logger.warning(
                "Product description paragraph not found."
            )

    else:

        logger.warning(
            "Product description section not found."
        )

    # --------------------------------------------------
    # CLEAN DESCRIPTION
    # --------------------------------------------------

    if description:

        # Normalize whitespace
        description = " ".join(
            description.split()
        )

        # Remove the website's "...more" marker
        description = description.replace(
            "...more",
            ""
        ).strip()

        # --------------------------------------------------
        # REMOVE DUPLICATED PREFIX
        # --------------------------------------------------
        #
        # Some Books to Scrape pages contain:
        #
        #   Short preview + Full description
        #
        # Example:
        #
        #   "Text A ... Text B Text A ... Text B"
        #
        # We detect the repeated beginning by looking
        # for a phrase that appears again later.
        #

        words = description.split()

        if len(words) > 30:

            max_prefix_length = min(
                40,
                len(words) // 2
            )

            duplicate_found = False

            for prefix_length in range(
                max_prefix_length,
                5,
                -1
            ):

                prefix = words[
                    :prefix_length
                ]

                prefix_text = " ".join(
                    prefix
                )

                remaining_text = " ".join(
                    words[prefix_length:]
                )

                # Look for the same prefix later
                position = remaining_text.find(
                    prefix_text
                )

                if position != -1:

                    # Keep the version beginning
                    # at the repeated full description.
                    repeated_start = (
                        prefix_length
                        + len(
                            remaining_text[
                                :position
                            ].split()
                        )
                    )

                    if repeated_start < len(words):

                        description = " ".join(
                            words[
                                repeated_start:
                            ]
                        )

                        duplicate_found = True

                        logger.info(
                            "Duplicated description "
                            "prefix removed."
                        )

                        break

            if not duplicate_found:

                logger.info(
                    "No duplicated description "
                    "prefix detected."
                )

        description = description.strip()

    # --------------------------------------------------
    # RETURN DETAILS
    # --------------------------------------------------

    logger.info(
        "Product details extracted successfully."
    )

    return {
        "category": category,
        "description": description
    }