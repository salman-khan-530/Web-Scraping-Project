# E-Commerce Product Data Web Scraper

A modular Python-based web scraping project that collects e-commerce product information, processes and validates the data, exports it to CSV and Excel, and performs basic analysis and visualization.

## Project Overview

The **E-Commerce Product Data Web Scraper** is designed to collect structured product information from e-commerce sources using appropriate and authorized data-access methods.

The project architecture currently includes scraper modules for **Amazon, Alibaba, and Flipkart**. These modules are structured to support integration through official APIs or other authorized data-access methods.

### Data Collected

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

- Web scraping architecture with Python Requests
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
- Streamlit web interface
- Modular and reusable project structure

## Technologies Used

- Python 3.12
- Requests
- BeautifulSoup4
- Pandas
- OpenPyXL
- Matplotlib
- Streamlit
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
│
├── app.py
├── main.py
├── analyze_data.py
├── visualize_data.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/salman-khan-530/Web-Scraping-Project.git
```

### 2. Navigate to the Project

```bash
cd Web-Scraping-Project
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

The project provides both a command-line interface and a Streamlit web interface.

### Command-Line Interface

Run the main application with:

```powershell
python main.py --help
```

The available options include:

| Argument | Description |
|---|---|
| `--query` | Product search query |
| `--websites` | One or more supported websites |
| `--max-products` | Maximum products to collect per website |

Example:

```powershell
python main.py --websites amazon --query "laptop" --max-products 5
```

Multiple websites can also be selected:

```powershell
python main.py --websites amazon alibaba flipkart --query "laptop" --max-products 5
```

The scraper manager sends the search query to each selected website scraper.

> **Note:** Amazon, Alibaba, and Flipkart integrations require an official API or another authorized data-access method before live product data can be collected.

## Streamlit Web Interface

The project includes a Streamlit-based graphical interface.

Start the application with:

```powershell
streamlit run app.py
```

The interface provides:

- Website selection
- Product search
- Maximum product selection
- Scraping controls
- Product results table
- Summary statistics
- CSV download
- Excel download

The Streamlit interface is designed as a user-friendly layer on top of the scraper architecture.

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

Processed data is saved in two formats.

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

The scraper logs important events and errors locally in:

```text
logs/scraper.log
```

Log files are excluded from Git using `.gitignore`.

## Ethical Scraping

This project is designed with responsible data collection practices in mind.

The project:

- Checks `robots.txt` where applicable.
- Uses request delays where applicable.
- Handles HTTP errors and failed requests.
- Avoids aggressive request rates.
- Should only be used against websites and data sources where access is permitted.

For commercial platforms such as Amazon, Alibaba, and Flipkart, the project should use their official APIs or another authorized data-access method where required by their terms and policies.

The project does not attempt to bypass CAPTCHAs, authentication systems, anti-bot protections, or other access controls.

## Current Website Support

| Website | Status |
|---|---|
| Amazon | Authorized integration placeholder |
| Alibaba | Authorized integration placeholder |
| Flipkart | Authorized integration placeholder |

The scraper architecture is prepared for authorized integrations with these platforms.

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
- Logging

The scraper manager has been tested to verify that:

- Amazon scraper is correctly selected.
- Alibaba scraper is correctly selected.
- Flipkart scraper is correctly selected.
- Unsupported websites are handled correctly.

## Example Workflow

```text
User enters search query
        ↓
Scraper Manager
        ↓
Select website scraper(s)
        ↓
Authorized data-access method
        ↓
Fetch product data
        ↓
Parse product information
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
- Concurrent data collection where permitted
- Retry mechanisms with exponential backoff
- Database storage
- Advanced interactive dashboards
- Automated scheduled data collection
- More advanced analytics

## Author

**Salman Khan**

BSCS (Artificial Intelligence) Student  
Machine Learning Intern

## License

This project is intended for educational and portfolio purposes.

Always review the target website's terms, `robots.txt`, API documentation, and applicable policies before collecting data.