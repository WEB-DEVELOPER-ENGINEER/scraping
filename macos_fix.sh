#!/bin/bash
# Quick fix script for macOS users with Tkinter issues

echo "=================================================="
echo "PriceSpy Lite - macOS Quick Fix"
echo "=================================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  No virtual environment detected!"
    echo ""
    echo "Please run:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  ./macos_fix.sh"
    exit 1
fi

echo "✓ Virtual environment detected"
echo ""

# Fix urllib3 issue
echo "📦 Fixing urllib3 LibreSSL compatibility issue..."
pip install "urllib3<2.0.0" --quiet
echo "✓ urllib3 downgraded to v1.x"
echo ""

# Install Flask for web interface
echo "📦 Installing Flask for web interface..."
pip install flask --quiet
echo "✓ Flask installed"
echo ""

echo "=================================================="
echo "✅ Fix applied successfully!"
echo "=================================================="
echo ""
echo "Now you can run:"
echo ""
echo "  Option 1 (Web Interface - Recommended for macOS):"
echo "    python web_gui.py"
echo "    Then open: http://localhost:5000"
echo ""
echo "  Option 2 (Auto-detect):"
echo "    python launch.py"
echo ""
echo "  Option 3 (Try Desktop GUI):"
echo "    python main_gui.py"
echo ""
echo "=================================================="
