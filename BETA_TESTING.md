# Juiced - Quick Start Guide for Beta Testers

Welcome to **Juiced v0.2.0 Beta**! 🎉

This is the first standalone release of Juiced, a terminal user interface for CyTube chat rooms.

## Prerequisites

- Python 3.7 or higher
- Terminal with 256-color support (most modern terminals)
- A CyTube account (or you can use guest access)

## Installation for Beta Testers

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Juiced.git
cd Juiced

# 2. Create virtual environment (recommended)
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Configuration

```bash
# 1. Copy the example config
cp configs/config.yaml.example configs/config.yaml

# 2. Edit with your details (use any text editor)
notepad configs/config.yaml  # Windows
nano configs/config.yaml     # Linux/Mac
```

**Minimal config needed:**
```yaml
domain: https://cytu.be
channel: YOUR_CHANNEL_NAME
user:
  - YOUR_USERNAME
  - YOUR_PASSWORD

tui:
  theme: hal9000  # Try different robots!
```

## Running Juiced

### Option 1: Direct command
```bash
python -m juiced configs/config.yaml
```

### Option 2: Launcher script
```bash
# Windows:
juiced.bat

# Linux/Mac (make executable first):
chmod +x juiced.py
./juiced.py
```

## First Time Using Juiced?

### Basic Controls
- Type and press `Enter` to send messages
- `Ctrl+C` to quit
- `/help` for all commands

### Try the Themes!
Type `/theme` to list all 11 robot themes, then:
```
/theme hal9000   - Red menacing AI (2001)
/theme r2d2      - Blue/white astromech (Star Wars)
/theme c3po      - Golden protocol droid
/theme t800      - Red HUD cyborg (Terminator)
/theme walle     - Rusty & cute (WALL-E)
/theme robocop   - Blue steel justice
```

### Tab Completion
- Type 2+ letters of a username, press `Tab`
- Type `#sm` then `Tab` for emotes like `#smile`
- Press `Tab` again to cycle through matches

### Scroll History
- `Page Up` / `Page Down` to scroll
- Or use `Ctrl+↑` / `Ctrl+↓`

## Known Issues (Beta)

- Terminal must be at least 80x24 (resize if needed)
- Some terminals may show rendering glitches on resize
- Long usernames may get truncated in narrow terminals
- Windows: SIGWINCH not supported (manual resize detection)

## Feedback Welcome!

Please report:
- ✅ What works well
- 🐛 Bugs you encounter
- 💡 Feature requests
- 🎨 Theme suggestions

## Common Issues

### "ModuleNotFoundError: No module named 'blessed'"
```bash
pip install blessed
```

### "Error loading config"
- Check config.yaml syntax (YAML is picky about indentation!)
- Make sure domain starts with `https://`
- Verify channel name is correct

### Colors look wrong
```bash
# Check your terminal supports 256 colors
echo $TERM  # Should be xterm-256color or similar
```

### Can't connect
- Test your credentials on the CyTube web interface first
- Check your internet connection
- Try a different channel

## Tips for Beta Testing

1. **Try all themes** - Each robot has a unique vibe!
2. **Test tab completion** - It's smart and context-aware
3. **Scroll around** - History holds 1000 messages
4. **Try commands** - Type `/help` for the full list
5. **Check the logs** - `logs/` folder has chat history and errors

## What to Test

- ✅ Connecting to different channels
- ✅ Sending messages (short and long)
- ✅ Private messages (`/pm username message`)
- ✅ Tab completion (usernames and emotes)
- ✅ Scrolling chat history
- ✅ Changing themes (`/theme <name>`)
- ✅ User list (ranks, AFK status)
- ✅ Media info (now playing, duration)
- ✅ Window resizing
- ✅ Running for extended periods

## Project Structure

```
Juiced/
├── juiced/              # Main application
│   ├── tui_bot.py       # Core TUI
│   ├── lib/             # CyTube library
│   └── themes/          # Robot themes
├── configs/             # Your configs
├── logs/                # Auto-generated logs
└── requirements.txt     # Dependencies
```

## Next Steps After Testing

1. **Report Issues** - Open GitHub issues for bugs
2. **Suggest Features** - What would make Juiced better?
3. **Share Feedback** - Join the discussion
4. **Spread the Word** - Tell other CyTubers!

---

**Have fun and get Juiced!** 🤖💬

For more details, see [README.md](README.md)
