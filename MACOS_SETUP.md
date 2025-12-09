# macOS Setup Instructions

If you encounter issues running PriceSpy Lite on macOS, follow these steps:

## Issue 1: SSL/OpenSSL Warning

If you see:
```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'
```

**Solution**: The `requirements.txt` has been updated to use urllib3 < 2.0.0. Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## Issue 2: Tkinter macOS Version Mismatch

If you see:
```
macOS 26 (2601) or later required, have instead 16 (1601) !
zsh: abort      python main_gui.py
```

This means your Python installation's Tkinter was compiled for a different macOS version.

### Solution A: Use Homebrew Python (Recommended)

1. Install Homebrew if you haven't: https://brew.sh
2. Install Python via Homebrew:
   ```bash
   brew install python-tk@3.11
   ```
3. Create a new virtual environment with Homebrew Python:
   ```bash
   /opt/homebrew/bin/python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main_gui.py
   ```

### Solution B: Use the Web Interface (No Tkinter Required)

We've created an alternative web-based interface that works on any system:
```bash
python web_gui.py
```
Then open your browser to: http://localhost:5000

### Solution C: Use System Python

If you have macOS's system Python:
```bash
/usr/bin/python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main_gui.py
```

## Verification

Check your Python and Tkinter:
```bash
python -c "import tkinter; print(tkinter.TkVersion)"
python -c "import sys; print(sys.version)"
```

If Tkinter import fails, use Solution B (web interface).
