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

### Standard Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### macOS Users (Quick Fix)

If you encounter SSL or Tkinter errors on macOS, run:
```bash
source venv/bin/activate
./macos_fix.sh
```

Then use the web interface instead:
```bash
python web_gui.py
```

See [MACOS_SETUP.md](MACOS_SETUP.md) for detailed troubleshooting.

## Usage

### Option 1: Desktop GUI (Tkinter)
Run the desktop application:
```bash
python main_gui.py
```

### Option 2: Web Interface (Works on all platforms)
If you have Tkinter issues on macOS, use the web interface:
```bash
python web_gui.py
```
Then open your browser to: http://localhost:5000

Both interfaces allow you to:
1. Enter the number of pages to scrape (1-50)
2. Choose output format (CSV or Excel)
3. Start the scraping process
4. View progress and results

## Legal Notice

This tool is configured to scrape books.toscrape.com, which is a legal scraping playground site designed for testing purposes. Always ensure you have permission before scraping any website.
