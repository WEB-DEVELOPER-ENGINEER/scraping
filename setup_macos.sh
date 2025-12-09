#!/bin/bash
# Complete setup script for macOS users
# This will install everything needed and launch the web interface

echo "=========================================="
echo "🍎 PriceSpy Lite - macOS Complete Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found!${NC}"
    echo "Please install Python 3 first:"
    echo "  brew install python3"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"
echo ""

# Check/Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install requirements with macOS fixes
echo "📦 Installing dependencies..."
pip install requests beautifulsoup4 lxml --quiet
echo "  ✓ Web scraping libraries"

pip install "pandas>=2.1.0" --quiet
echo "  ✓ Data processing"

pip install openpyxl --quiet
echo "  ✓ Excel support"

pip install "urllib3<2.0.0" --quiet
echo "  ✓ urllib3 (LibreSSL compatible)"

pip install flask --quiet
echo "  ✓ Flask web framework"

echo ""
echo -e "${GREEN}✅ All dependencies installed!${NC}"
echo ""

# Test installations
echo "🧪 Testing installations..."
python3 -c "import requests; print('  ✓ requests')" 2>/dev/null
python3 -c "import bs4; print('  ✓ beautifulsoup4')" 2>/dev/null
python3 -c "import pandas; print('  ✓ pandas')" 2>/dev/null
python3 -c "import openpyxl; print('  ✓ openpyxl')" 2>/dev/null
python3 -c "import flask; print('  ✓ flask')" 2>/dev/null
echo ""

# Check Tkinter
echo "🔍 Checking Tkinter availability..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${GREEN}✓ Tkinter is available (desktop GUI will work)${NC}"
    TKINTER_OK=1
else
    echo -e "${YELLOW}⚠ Tkinter not available (will use web interface)${NC}"
    TKINTER_OK=0
fi
echo ""

# Summary
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "You can now run PriceSpy Lite using:"
echo ""

if [ $TKINTER_OK -eq 1 ]; then
    echo "Option 1 (Desktop GUI):"
    echo "  ${GREEN}python main_gui.py${NC}"
    echo ""
fi

echo "Option 2 (Web Interface - Recommended):"
echo "  ${GREEN}python web_gui.py${NC}"
echo "  Then open: ${YELLOW}http://localhost:5000${NC}"
echo ""

echo "Option 3 (Auto-detect best option):"
echo "  ${GREEN}python launch.py${NC}"
echo ""
echo "=========================================="
echo ""

# Ask if user wants to launch now
read -p "Would you like to launch the web interface now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Launching web interface..."
    echo "Open your browser to: http://localhost:5000"
    echo ""
    python web_gui.py
fi
