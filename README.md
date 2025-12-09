# PriceSpy Lite

A simple web scraping tool with a GUI interface that crawls product listings from books.toscrape.com and extracts product data.

## Features

- 🔍 Crawl one or multiple pages of product listings
- 📊 Extract product data: title, price, availability, rating, and URL
- 🔄 Automatic deduplication of results
- 💰 Normalized price column for easy analysis
- 💾 Export to CSV or Excel format
- ⏱️ Built-in rate limiting and retry mechanism
- 🖥️ User-friendly GUI interface

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main_gui.py
```

The GUI will allow you to:
1. Enter the number of pages to scrape (1-50)
2. Choose output format (CSV or Excel)
3. Start the scraping process
4. View progress and results

## Legal Notice

This tool is configured to scrape books.toscrape.com, which is a legal scraping playground site designed for testing purposes. Always ensure you have permission before scraping any website.
