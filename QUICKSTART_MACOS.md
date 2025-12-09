# 🚀 QUICK START - macOS Users

## ⚡ Fastest Way (One Command)

```bash
cd /path/to/scraping-master
./setup_macos.sh
```

This will:
- ✅ Check Python
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Fix macOS issues
- ✅ Launch the app

---

## 📋 Manual Setup (3 Steps)

### Step 1: Setup Environment
```bash
cd /path/to/scraping-master
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Fix Dependencies
```bash
./macos_fix.sh
```

### Step 3: Run the App
```bash
python web_gui.py
```

Then open: **http://localhost:5000**

---

## 🎯 Command Cheat Sheet

| Action | Command |
|--------|---------|
| **Complete Setup** | `./setup_macos.sh` |
| **Quick Fix** | `./macos_fix.sh` |
| **Web Interface** | `python web_gui.py` |
| **Desktop GUI** | `python main_gui.py` |
| **Smart Launcher** | `python launch.py` |
| **Activate venv** | `source venv/bin/activate` |
| **Check Python** | `python --version` |
| **Test Flask** | `python -c "import flask"` |

---

## 🐛 Your Error → Solution

### Error: `NotOpenSSLWarning: urllib3 v2...`
**Fix:**
```bash
pip install "urllib3<2.0.0" --force-reinstall
```

### Error: `macOS 26 (2601) or later required...`
**Fix:** Use web interface instead
```bash
python web_gui.py
```

### Error: `Module 'flask' not found`
**Fix:**
```bash
pip install flask
```

---

## 🌐 Web Interface Features

- ✨ Beautiful modern UI
- 📊 Real-time progress tracking
- 📈 Live statistics
- 📥 Direct download
- 📱 Mobile-friendly
- 🌍 Works everywhere

---

## ✅ Verification Steps

After setup, verify everything works:

```bash
# 1. Check virtual environment
echo $VIRTUAL_ENV

# 2. Check Python packages
pip list | grep -E "flask|requests|pandas|beautifulsoup4"

# 3. Test imports
python -c "import flask, requests, bs4, pandas; print('✅ All OK')"

# 4. Launch app
python web_gui.py
```

---

## 💡 Pro Tips

1. **Always activate venv first:**
   ```bash
   source venv/bin/activate
   ```

2. **Web interface runs on port 5000:**
   - Local: http://localhost:5000
   - Network: http://YOUR_IP:5000

3. **Stop web server:**
   Press `Ctrl + C` in terminal

4. **View output files:**
   ```bash
   ls -la pricespy_results_*.{csv,xlsx}
   ```

5. **Fresh start:**
   ```bash
   rm -rf venv
   ./setup_macos.sh
   ```

---

## 📞 Need Help?

1. Read [MACOS_SETUP.md](MACOS_SETUP.md) - Detailed guide
2. Read [MACOS_FIX_SUMMARY.md](MACOS_FIX_SUMMARY.md) - Issue explanation
3. Read [INTERFACE_COMPARISON.md](INTERFACE_COMPARISON.md) - Compare options

---

## 🎉 Success Checklist

- [ ] Downloaded/extracted the project
- [ ] Ran `./setup_macos.sh` or followed manual steps
- [ ] No errors during installation
- [ ] Activated virtual environment
- [ ] Launched `python web_gui.py`
- [ ] Opened http://localhost:5000 in browser
- [ ] Saw PriceSpy Lite interface
- [ ] Successfully scraped some pages
- [ ] Downloaded CSV/Excel results

**All checked?** You're ready to go! 🚀

---

## 📞 One-Liner Summary

**Just run this and you're done:**
```bash
cd scraping-master && ./setup_macos.sh
```

That's it! 🎊
