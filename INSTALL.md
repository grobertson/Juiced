# 📦 Juiced Installation Guide

This guide will walk you through installing Juiced step-by-step. No prior experience required!

---

## 📋 Prerequisites

You need Python 3.7 or newer installed on your computer.

### Check if you have Python

**Windows:**
```bash
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

If you see a version number like `Python 3.11.x`, you're good to go! ✅

If you get an error, install Python first:
- **Windows/macOS**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3 python3-venv` (Ubuntu/Debian) or `sudo dnf install python3` (Fedora)

---

## 🚀 Quick Install (Recommended)

### Windows

1. **Download Juiced**
   ```bash
   git clone https://github.com/grobertson/Juiced.git
   cd Juiced
   ```

2. **Run the setup script**
   ```bash
   setup.bat
   ```

3. **Follow the prompts:**
   - Enter your CyTube channel name (e.g., `movienight`)
   - Enter your username (or press Enter for guest access)
   - Enter your password (if you provided a username)

4. **Launch Juiced**
   ```bash
   juiced.bat
   ```

That's it! 🎉

---

### macOS/Linux

1. **Download Juiced**
   ```bash
   git clone https://github.com/grobertson/Juiced.git
   cd Juiced
   ```

2. **Make setup script executable**
   ```bash
   chmod +x setup.sh
   ```

3. **Run the setup script**
   ```bash
   ./setup.sh
   ```

4. **Follow the prompts:**
   - Enter your CyTube channel name (e.g., `movienight`)
   - Enter your username (or press Enter for guest access)
   - Enter your password (if you provided a username)

5. **Launch Juiced**
   ```bash
   ./juiced.py
   ```

That's it! 🎉

---

## 🔧 Manual Install (Advanced)

If you prefer to set things up manually or the automatic setup doesn't work:

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `blessed` - Terminal UI library
- `python-socketio` - CyTube connection
- `PyYAML` - Config file support
- `requests` and `aiohttp` - Network communication

### Step 3: Configure Juiced

1. **Copy the example config:**
   ```bash
   # Windows
   copy configs\config.yaml.example configs\config.yaml

   # macOS/Linux
   cp configs/config.yaml.example configs/config.yaml
   ```

2. **Edit the config file:**
   Open `configs/config.yaml` in your favorite text editor and change:

   ```yaml
   channel: your-channel-name      # ← Your CyTube channel
   user:
     - your-username               # ← Your username
     - your-password               # ← Your password
   ```

   **For guest access**, use:
   ```yaml
   user: null
   ```

3. **Special note about passwords:**
   If your password starts with special characters (`@`, `#`, `!`, etc.), you **must** quote it:
   ```yaml
   user:
     - myusername
     - "@myP@ssw0rd!"              # ← Quoted because it starts with @
   ```

### Step 4: Run Juiced

**Windows:**
```bash
python -m juiced configs\config.yaml
```

**macOS/Linux:**
```bash
python -m juiced configs/config.yaml
```

---

## 🎨 Choosing a Theme

Juiced comes with 11 robot-themed color schemes! Change your theme in the config file:

```yaml
tui:
  theme: hal9000        # ← Change this
```

Available themes:
- `default` - Clean blue/cyan
- `hal9000` - Menacing red
- `r2d2` - Plucky blue
- `c3po` - Golden yellow
- `t800` - Cyberdyne red
- `walle` - Rusty orange
- `robocop` - Detroit blue
- `robby` - Classic robot
- `marvin` - Depressing gray
- `johnny5` - High contrast
- `data` - Android amber

You can also change themes while Juiced is running with `/theme <name>` command!

---

## 🐛 Troubleshooting

### "Python is not recognized as a command"

**Problem:** Python isn't in your system PATH.

**Solution:**
- **Windows:** Reinstall Python and check "Add Python to PATH" during installation
- **macOS/Linux:** Use `python3` instead of `python`

---

### "ERROR: PyYAML is required for YAML config files"

**Problem:** Dependencies aren't installed.

**Solution:**
```bash
pip install -r requirements.txt
```

Or run the setup script again.

---

### "ERROR: No module named 'blessed'"

**Problem:** Virtual environment isn't activated or dependencies not installed.

**Solution:**
1. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`

---

### "Connection failed" or "Socket error"

**Problem:** Can't connect to CyTube server.

**Checklist:**
- ✅ Is your internet connection working?
- ✅ Is the CyTube server up? (Try accessing it in your browser)
- ✅ Is your channel name correct? (Check for typos)
- ✅ Is your username/password correct?

---

### Config file won't load

**Problem:** YAML syntax error.

**Common mistakes:**
- Forgot to quote password starting with special characters
- Wrong indentation (use 2 spaces, not tabs)
- Left example values in place

**Solution:** Compare your config to `configs/config.yaml.example` carefully.

---

## 🆘 Getting Help

Still stuck? Here's how to get help:

1. **Check the docs:**
   - [README.md](README.md) - Full documentation
   - [BETA_TESTING.md](BETA_TESTING.md) - Quick start guide
   - [CHANGELOG.md](CHANGELOG.md) - Version history

2. **Open an issue:**
   - Go to [GitHub Issues](https://github.com/grobertson/Juiced/issues)
   - Describe your problem
   - Include your OS and Python version
   - Include any error messages

3. **Check logs:**
   - Juiced creates log files in the `logs/` directory
   - Include relevant log snippets when asking for help

---

## 🎓 Next Steps

Once installed, check out:
- [BETA_TESTING.md](BETA_TESTING.md) - Learn the keyboard shortcuts and commands
- [README.md](README.md) - Explore all features
- Press `Ctrl+C` or type `/quit` to exit Juiced

**Happy chatting!** 🎉
