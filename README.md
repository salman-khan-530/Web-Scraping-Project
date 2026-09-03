# E-Commerce Product Data Web Scraper

A modular Python-based web scraping project that collects e-commerce product information, processes and validates the data, exports it to CSV and Excel, and performs basic analysis and visualization.

## Project Overview

The **E-Commerce Product Data Web Scraper** is designed to collect structured product information from publicly accessible e-commerce sources.

The project currently includes a working scraper for **Books to Scrape**, which is used as a safe practice website. The architecture also includes scraper modules for **Amazon, Alibaba, and Flipkart**, prepared for integration through authorized APIs or other approved data-access methods.

### Data collected

For each product, the scraper is designed to handle:

- Product name
- Product price
- Product rating
- Availability/status
- Product URL
- Product category
- Product description
- Data source

## Features

- Web scraping with Python Requests
- HTML parsing with BeautifulSoup
- Pagination handling
- Product search
- Multiple website scraper architecture
- `robots.txt` checking
- Request delays
- Timeout and connection error handling
- Missing HTML element handling
- Data cleaning and preprocessing
- Duplicate removal
- Missing-value handling
- Price conversion to numeric values
- Rating standardization
- Data validation
- CSV export
- Excel export
- Statistical analysis
- Data visualization
- Logging
- Command-line interface
- Modular and reusable project structure

## Technologies Used

- Python 3.12
- Requests
- BeautifulSoup4
- Pandas
- OpenPyXL
- Matplotlib
- Jupyter Notebook
- Git & GitHub

## Project Structure

```text
Web Scraping Project/
│
├── scraper/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── http_client.py
│   ├── robots_checker.py
│   ├── parser.py
│   ├── pagination.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   ├── amazon_scraper.py
│   ├── alibaba_scraper.py
│   ├── flipkart_scraper.py
│   ├── scraper_manager.py
│   ├── data_processor.py
│   ├── exporter.py
│   ├── analyzer.py
│   └── visualizer.py
│
├── data/
│
├── output/
│   ├── products.csv
│   └── products.xlsx
│
├── notebooks/
│   └── 01_requests_basics.ipynb
│
├── logs/
│   └── scraper.log
│
├── main.py
├── analyze_data.py
├── visualize_data.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/salman-khan-530/Web-Scraping-Project.git
```

### 2. Navigate to the project

```bash
cd Web-Scraping-Project
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

The scraper is controlled through the command line.

### Search Books to Scrape

```powershell
python main.py --websites books --query light --max-products 2
```

The command:

- Searches for the specified product/query
- Collects matching products
- Processes the data
- Saves CSV and Excel files
- Performs analysis
- Generates visualizations

### Search Multiple Websites

```powershell
python main.py --websites books amazon alibaba flipkart --query light --max-products 2
```

The scraper manager sends the same search query to each selected website scraper.

Currently, **Books to Scrape** has a working implementation. Amazon, Alibaba, and Flipkart modules safely return empty results until an authorized data-access method is configured.

### Command Options

| Argument | Description |
|---|---|
| `--query` | Product search query |
| `--websites` | One or more websites to search |
| `--max-products` | Maximum products to collect per website |

Example:

```powershell
python main.py --websites books --query "light" --max-products 5
```

## Data Processing

After scraping, the collected data passes through a preprocessing pipeline.

### Cleaning

- Product names are stripped and normalized.
- Prices are converted to numeric values.
- Ratings are standardized to values from 1 to 5.
- Availability values are normalized.
- Text encoding issues are handled.
- Missing values receive appropriate fallback values.

### Duplicate Removal

Duplicate records are removed using complete-record comparison and product URLs where available.

### Validation

Records are validated to ensure:

- Product name exists.
- Product URL exists.
- Price is valid and non-negative.
- Rating is between 1 and 5.

Invalid records are removed before export.

## Data Export

Processed data is saved in two formats:

### CSV

```text
output/products.csv
```

### Excel

```text
output/products.xlsx
```

The exported dataset contains:

```text
name
price
rating
availability
url
category
description
source
```

## Data Analysis

The project performs the following analysis:

- Total number of products
- Average product price
- Minimum price
- Maximum price
- Most common rating
- Number of available products
- Highest-rated products
- Lowest-priced products

Example analysis output:

```text
total_products: 2
average_price: 40.82
minimum_price: 29.87
maximum_price: 51.77
most_common_rating: 3.0
available_products: 2
```

## Data Visualization

The project generates visualizations for:

### 1. Price Distribution

Shows how product prices are distributed.

### 2. Rating Distribution

Shows the number of products for each rating.

### 3. Price vs Rating

Shows the relationship between product price and rating.

### 4. Products by Category

Shows the number of products in each category.

## Error Handling

The project includes error handling for:

- Invalid URLs
- Empty search queries
- Empty product URLs
- Connection failures
- Request timeouts
- HTTP errors
- Missing HTML elements
- Invalid prices
- Invalid ratings
- Missing data
- Unsupported websites
- Failed product-page requests
- Export errors
- Visualization errors

The scraper logs important events and errors in:

```text
logs/scraper.log
```

## Ethical Scraping

This project is designed with responsible scraping practices in mind.

The scraper:

- Checks `robots.txt` before accessing pages.
- Uses a request delay between requests.
- Handles HTTP errors and failed requests.
- Avoids aggressive request rates.
- Should only be used against websites and data sources where access is permitted.

For commercial platforms such as Amazon, Alibaba, and Flipkart, the project should use their official APIs or another authorized data-access method where required by their terms and policies.

## Current Website Support

| Website | Status |
|---|---|
| Books to Scrape | Working |
| Amazon | Authorized integration placeholder |
| Alibaba | Authorized integration placeholder |
| Flipkart | Authorized integration placeholder |

**Books to Scrape** is currently used as the working practice data source.

## Testing

The project contains separate test scripts for important components, including:

- HTTP requests
- Parser
- CSV export
- Excel export
- Analyzer
- Visualization
- Scraper manager
- Multi-website search
- Robots.txt checking
- Books scraper
- Logging

The main application has also been tested using both single-website and multi-website commands.

## Example Workflow

```text
User enters search query
        ↓
Scraper Manager
        ↓
Select website scraper(s)
        ↓
Fetch webpage
        ↓
Check robots.txt
        ↓
Parse HTML
        ↓
Extract product information
        ↓
Handle pagination
        ↓
Fetch product details
        ↓
Clean and preprocess data
        ↓
Remove duplicates
        ↓
Validate records
        ↓
Export CSV + Excel
        ↓
Analyze data
        ↓
Generate visualizations
```

## Future Improvements

Possible future improvements include:

- Authorized Amazon API integration
- Authorized Alibaba API integration
- Authorized Flipkart API integration
- Advanced search filtering
- Category-based searches
- Concurrent scraping where permitted
- Retry mechanisms with exponential backoff
- Database storage
- Web-based user interface
- Automated scheduled scraping
- More advanced analytics
- Interactive dashboards

## Author

**Salman Khan**

BSCS (Artificial Intelligence) Student  
Machine Learning Intern

## License

This project is intended for educational and portfolio purposes. Always review the target website's terms, robots.txt, API documentation, and applicable policies before collecting data.