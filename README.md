# News Scraper

A web scraping tool designed to extract news articles from ABC News website.

## Features

- Configurable web scraping parameters
- Headless browser support
- Automatic pagination handling
- CSV export functionality
- Robust error handling and logging

## Installation

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Install Chrome and ChromeDriver

## Usage

Run the scraper:
```bash
python src/scraper.py
```

## Configuration

Edit `config/config.yaml` to customize:
- Browser settings
- Output directory
- Scraping parameters
- CSS Selectors

## Output

Scraped data is saved to CSV files in the configured output directory.