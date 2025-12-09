# 📁 Project Structure Guide

```
scraping/
│
├── 🎯 CORE APPLICATION FILES
│   ├── scraper.py              # Web scraping logic
│   ├── data_processor.py       # Data cleaning & export
│   ├── main_gui.py             # Desktop GUI (Tkinter)
│   └── web_gui.py              # Web GUI (Flask) ⭐ USE THIS ON macOS
│
├── 🚀 LAUNCHER SCRIPTS
│   ├── launch.py               # Smart launcher (auto-detect)
│   ├── setup_macos.sh          # Complete setup for macOS
│   └── macos_fix.sh            # Quick fix for existing setup
│
├── 📚 DOCUMENTATION
│   ├── README.md               # Main documentation
│   ├── QUICKSTART_MACOS.md     # Quick reference for macOS
│   ├── MACOS_SETUP.md          # Detailed macOS troubleshooting
│   ├── MACOS_FIX_SUMMARY.md    # Explanation of fixes
│   ├── INTERFACE_COMPARISON.md # Desktop vs Web comparison
│   └── PROJECT_STRUCTURE.md    # This file
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt        # Python dependencies
│   └── .gitignore             # Git ignore rules
│
├── 📊 OUTPUT FILES (generated)
│   ├── pricespy_results_*.csv  # CSV exports
│   └── pricespy_results_*.xlsx # Excel exports
│
└── 🔧 SYSTEM
    ├── venv/                   # Virtual environment
    ├── templates/              # HTML templates for web GUI
    └── __pycache__/           # Python cache
```

---

## 🎯 File Purposes

### Core Application

#### `scraper.py`
**Purpose:** Web scraping engine  
**Key Features:**
- Crawls books.toscrape.com
- Extracts product data
- Rate limiting (0.5s between requests)
- Retry logic with exponential backoff
- Handles pagination

**Main Class:** `ProductScraper`

---

#### `data_processor.py`
**Purpose:** Data processing and export  
**Key Features:**
- Price normalization (£51.77 → 51.77)
- Deduplication by URL
- CSV export
- Excel export with formatting
- Summary statistics

**Main Class:** `DataProcessor`

---

#### `main_gui.py`
**Purpose:** Desktop GUI application  
**Technology:** Tkinter  
**Status:** ⚠️ May not work on macOS

**Features:**
- Native desktop window
- Progress bar
- Real-time logs
- Settings panel
- File save dialog

**When to use:** Linux, Windows, or macOS with working Tkinter

---

#### `web_gui.py` ⭐
**Purpose:** Web-based GUI application  
**Technology:** Flask  
**Status:** ✅ Works on ALL platforms

**Features:**
- Modern web interface
- Real-time updates
- Progress tracking
- Download button
- Mobile-friendly
- No Tkinter dependency

**When to use:** macOS (recommended), remote access, any platform

**API Endpoints:**
- `GET /` - Main interface
- `POST /api/start` - Start scraping
- `GET /api/status` - Get progress
- `GET /api/download/<file>` - Download results

---

### Launcher Scripts

#### `launch.py`
**Purpose:** Smart launcher  
**Logic:**
```python
if tkinter_available():
    run main_gui.py
else:
    run web_gui.py
```

**Use:** When you want automatic detection

---

#### `setup_macos.sh`
**Purpose:** Complete macOS setup  
**What it does:**
1. Checks Python installation
2. Creates virtual environment
3. Installs all dependencies
4. Fixes macOS-specific issues
5. Tests installations
6. Offers to launch app

**Use:** First-time setup on macOS

---

#### `macos_fix.sh`
**Purpose:** Quick fix for existing installations  
**What it does:**
1. Downgrades urllib3 to <2.0
2. Installs Flask
3. Shows next steps

**Use:** When you already have venv but encounter errors

---

### Documentation Files

#### `README.md`
- Project overview
- Installation instructions
- Usage examples
- Features list

#### `QUICKSTART_MACOS.md`
- One-page reference
- Quick commands
- Common errors
- Cheat sheet

#### `MACOS_SETUP.md`
- Detailed troubleshooting
- Multiple solutions
- Step-by-step guides
- Verification commands

#### `MACOS_FIX_SUMMARY.md`
- Explanation of issues
- Why they occur
- What was fixed
- Recommended approach

#### `INTERFACE_COMPARISON.md`
- Desktop vs Web comparison
- Feature matrix
- Pros/cons
- Recommendations

#### `PROJECT_STRUCTURE.md`
- This file
- File explanations
- Architecture overview
- Usage recommendations

---

## 🔄 Application Flow

### Desktop GUI Flow (main_gui.py)
```
User launches main_gui.py
    ↓
Tkinter window opens
    ↓
User sets parameters
    ↓
Clicks "Start Scraping"
    ↓
Background thread starts
    ↓
scraper.py crawls pages
    ↓
data_processor.py processes data
    ↓
Results saved to file
    ↓
Dialog shows completion
```

### Web GUI Flow (web_gui.py)
```
User launches web_gui.py
    ↓
Flask server starts
    ↓
User opens browser to localhost:5000
    ↓
HTML interface loads
    ↓
User sets parameters
    ↓
Clicks "Start Scraping"
    ↓
JavaScript sends POST to /api/start
    ↓
Background thread starts
    ↓
JavaScript polls /api/status
    ↓
UI updates in real-time
    ↓
Results ready
    ↓
Download button appears
```

---

## 🛠️ Data Flow

```
books.toscrape.com
    ↓
[scraper.py]
    → Extracts: title, price, rating, availability, URL
    ↓
[Raw Product List]
    ↓
[data_processor.py]
    → Deduplicates
    → Normalizes prices
    → Creates DataFrame
    ↓
[Processed Data]
    ↓
[Export Module]
    → CSV or Excel
    ↓
[Output File]
pricespy_results_TIMESTAMP.csv/xlsx
```

---

## 🏗️ Architecture

### Separation of Concerns

1. **Scraping Logic** (`scraper.py`)
   - Independent of UI
   - Can be used programmatically
   - Handles HTTP, parsing, retries

2. **Data Processing** (`data_processor.py`)
   - Independent of scraping
   - Can process any product list
   - Handles export formats

3. **User Interface** (`main_gui.py` OR `web_gui.py`)
   - Uses scraper and processor
   - Provides user interaction
   - Shows progress

### Benefits
- ✅ Each module testable independently
- ✅ Easy to swap UI (Tkinter ↔ Flask)
- ✅ Can use scraper in other projects
- ✅ Clear responsibilities

---

## 🎯 Usage Recommendations

### For macOS Users:
```bash
./setup_macos.sh          # First time
python web_gui.py         # Every time after
```

### For Linux/Windows Users:
```bash
pip install -r requirements.txt
python main_gui.py        # Or web_gui.py
```

### For Developers:
```python
# Use modules programmatically
from scraper import ProductScraper
from data_processor import DataProcessor

scraper = ProductScraper()
products = scraper.scrape_multiple_pages(5)

processor = DataProcessor()
df = processor.process_products(products)
processor.save_to_csv(df, "output.csv")
```

---

## 📦 Dependencies

### Required for All:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast parsing
- `pandas` - Data manipulation
- `openpyxl` - Excel export
- `urllib3<2.0` - macOS compatibility

### Required for Web GUI:
- `flask` - Web framework

### Built-in:
- `tkinter` - Desktop GUI (if available)
- `threading` - Background tasks
- `datetime` - Timestamps
- `re` - Regex
- `os` - File operations

---

## 🔍 Finding What You Need

**Want to modify scraping logic?**
→ Edit `scraper.py`

**Want to change data processing?**
→ Edit `data_processor.py`

**Want to customize desktop UI?**
→ Edit `main_gui.py`

**Want to customize web UI?**
→ Edit `web_gui.py` (HTML is embedded)

**Need help with macOS?**
→ Read `QUICKSTART_MACOS.md`

**Want to understand the fix?**
→ Read `MACOS_FIX_SUMMARY.md`

**Comparing interfaces?**
→ Read `INTERFACE_COMPARISON.md`

---

## 🎓 Learning Path

1. **Start Here:** `README.md`
2. **macOS Setup:** `QUICKSTART_MACOS.md`
3. **Run the app:** `python web_gui.py`
4. **Understand code:** Read `scraper.py`, `data_processor.py`
5. **Customize:** Modify parameters, add features
6. **Deploy:** Use `web_gui.py` for production

---

## 🚀 Quick Commands Reference

```bash
# Setup (first time)
./setup_macos.sh

# Run web interface
python web_gui.py

# Run desktop interface
python main_gui.py

# Auto-detect
python launch.py

# Install deps
pip install -r requirements.txt

# Fix macOS issues
./macos_fix.sh

# Check installation
pip list | grep -E "flask|requests|pandas"
```

---

## 📊 File Size Overview

| File | Lines | Purpose |
|------|-------|---------|
| `scraper.py` | ~200 | Scraping engine |
| `data_processor.py` | ~170 | Data processing |
| `main_gui.py` | ~400 | Desktop GUI |
| `web_gui.py` | ~550 | Web GUI + HTML |
| `launch.py` | ~70 | Smart launcher |

**Total Code:** ~1,400 lines  
**Documentation:** ~1,000+ lines

---

This project is well-documented, modular, and ready for use! 🎉
