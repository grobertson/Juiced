# Juiced - CyTube Terminal User Interface

![Python](https://img.shields.io/badge/python-3.7+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Status](https://img.shields.io/badge/status-beta-yellow)

**Juiced** is a powerful, colorful terminal user interface (TUI) for CyTube chat rooms. Inspired by classic IRC clients like BitchX and IRCII, Juiced brings a modern, feature-rich chat experience to your terminal with 11 robot-themed color schemes!

![Juiced TUI Screenshot](docs/screenshot.png)

## ✨ Features

- 🎨 **11 Robot Themes** - HAL 9000, R2-D2, C-3PO, T-800, WALL-E, RoboCop, and more!
- 💬 **Full Chat Support** - Messages, PMs, mentions, emotes
- ⌨️ **Smart Tab Completion** - Auto-complete usernames and #emotes
- 📜 **Scrollable History** - Navigate through 1000+ messages
- 👥 **Live User List** - Rank-based colors, AFK tracking, status indicators  
- 🎵 **Media Info** - Now playing, duration, time remaining
- 📊 **Live Stats** - Session time, viewer counts, uptime
- 📝 **Auto Logging** - Chat history and error logs
- 🖥️ **Responsive Layout** - Adapts to terminal size
- ⚡ **Fast & Lightweight** - Pure Python, minimal dependencies

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Juiced.git
cd Juiced

# Install dependencies
pip install -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the example config
cp configs/config.yaml.example configs/config.yaml

# Edit with your CyTube server and credentials
nano configs/config.yaml
```

**Minimal config.yaml:**
```yaml
domain: https://cytu.be
channel: YourChannelName
user:
  - YourUsername
  - YourPassword

tui:
  theme: hal9000  # Choose your favorite robot!
```

### Run

```bash
# Start Juiced!
python -m juiced configs/config.yaml

# Or make it executable (Linux/Mac)
chmod +x juiced.py
./juiced.py configs/config.yaml

# Windows: Use the launcher
juiced.bat
```

## 🤖 Robot Themes

Choose from 11 iconic robot color schemes:

| Theme | Robot | Source | Vibe |
|-------|-------|--------|------|
| `default` | - | - | Classic cyan/white |
| `hal9000` | HAL 9000 | 2001: A Space Odyssey | 🔴 Red menacing AI |
| `r2d2` | R2-D2 | Star Wars | 🔵 Blue/white beeps |
| `c3po` | C-3PO | Star Wars | ✨ Golden protocol |
| `t800` | T-800 | Terminator | 🔴 Red HUD cyborg |
| `walle` | WALL-E | WALL-E | 🟡 Rusty & cute |
| `robby` | Robby | Forbidden Planet | 🔷 Cyan retro sci-fi |
| `marvin` | Marvin | Hitchhiker's Guide | 💚 Depressed genius |
| `johnny5` | Johnny 5 | Short Circuit | 🌟 Bright & alive |
| `robocop` | RoboCop | RoboCop | 🔷 Blue steel justice |
| `data` | Data | Star Trek: TNG | 💛 Yellow ops uniform |

Change themes anytime with `/theme <name>`!

## ⌨️ Keyboard Controls

### Navigation
- `Enter` - Send message
- `↑` / `↓` - Navigate command history
- `Page Up` / `Page Down` - Scroll chat
- `Ctrl+↑` / `Ctrl+↓` - Alternative scroll
- `Tab` - Auto-complete (usernames/emotes)
- `Ctrl+C` - Quit

### Commands

```
/help                    - Show all commands
/theme [name]            - List or change theme
/pm <user> <msg>         - Send private message
/users                   - List all users
/playlist [n]            - Show playlist
/quit                    - Exit Juiced
```

See full command list with `/help` in Juiced.

## 🎯 Tab Completion

**Usernames**: Type 2+ letters, press Tab
- Example: `he<Tab>` → `hello_user`
- Press Tab again to cycle matches

**Emotes**: Type `#` + letters, press Tab  
- Example: `#sm<Tab>` → `#smile`
- Cycles through all matching emotes

## 📁 Project Structure

```
Juiced/
├── juiced/                  # Main package
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── tui_bot.py           # Core TUI implementation
│   ├── lib/                 # CyTube library
│   │   ├── bot.py           # Base bot
│   │   ├── channel.py
│   │   ├── socket_io.py
│   │   └── ...
│   └── themes/              # 11 robot themes
│       ├── hal9000.json
│       ├── r2d2.json
│       └── ...
├── configs/
│   └── config.yaml.example  # Configuration template
├── logs/                    # Auto-generated logs
├── requirements.txt         # Dependencies
├── setup.py                 # Package installer
├── juiced.bat               # Windows launcher
├── juiced.py                # Unix launcher
├── LICENSE                  # MIT License
└── README.md                # This file
```

## 🔧 Configuration

Full configuration options:

```yaml
# Connection
domain: https://cytu.be         # CyTube server
channel: YourChannel            # Channel to join  
user: [username, password]      # Credentials (or null for guest)

# Socket.IO
response_timeout: 1             # Response timeout (seconds)
restart_delay: 5                # Reconnect delay
log_level: WARNING              # DEBUG|INFO|WARNING|ERROR

# TUI Options
tui:
  theme: hal9000                # Theme name
  show_join_quit: true          # Show join/leave messages
  clock_format: 12h             # 12h or 24h  
  hide_afk_users: false         # Hide AFK from list
```

## 🛠️ Requirements

- Python 3.7+
- blessed (terminal library)
- python-socketio
- websocket-client
- PyYAML (for YAML configs)

All dependencies install via `requirements.txt`.

## 🐛 Troubleshooting

### Colors not showing?
```bash
# Check terminal color support
echo $TERM  # Should be xterm-256color

# Test colors
python -c "from blessed import Terminal; t=Terminal(); print(t.green('OK'))"
```

### Terminal too small?
Minimum: 80 columns × 24 rows

### Unicode issues?
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Connection fails?
- Verify domain includes `https://`
- Check channel name is correct
- Test credentials on web interface first

## 📝 Logs

Auto-saved in `logs/`:
- `chat_YYYYMMDD_HHMMSS.log` - Complete chat history
- `tui_errors.log` - Errors and warnings

## 🤝 Contributing

Contributions welcome! This is a beta release.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly  
5. Submit a pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **blessed** - Terminal manipulation library
- **BitchX** & **IRCII** - Interface inspiration
- **CyTube** - The awesome synchronized media platform
- All the robots that inspired our themes! 🤖

## 🔗 Links

- [CyTube](https://github.com/calzoneman/sync)
- [blessed docs](https://blessed.readthedocs.io/)
- [Report Issues](https://github.com/yourusername/Juiced/issues)

---

**Get Juiced and chat in style!** 🎉🤖💬

*"I'm sorry Dave, I'm afraid I can't do that... but I can help you chat!"* - HAL 9000 theme
