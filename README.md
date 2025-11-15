#  Juiced

**A retro-futuristic terminal chat client for CyTube**  Inspired by classic IRC clients like BitchX, built for the modern web

[![Beta Release](https://img.shields.io/badge/version-0.2.0--beta-orange.svg)](https://github.com/grobertson/Juiced/releases)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

##  Why Juiced?

Tired of clunky web interfaces? **Juiced** brings the speed and elegance of terminal-based chat to CyTube. Born from daily use in the Rosey-Robot project, it proved so indispensable that it earned its own release.

**Live in the terminal. Chat like it's 1999. Ship like it's 2025.**

---

##  Features That Pop

 **11 Robot-Themed Color Schemes**  HAL 9000, R2-D2, C-3PO, T-800, WALL-E, and more  
 **Lightning-Fast Tab Completion**  Usernames, emotes, commands  
 **Infinite Scroll**  1000+ message history at your fingertips  
 **Live User List**  Rank colors, AFK detection, real-time updates  
 **Media Display**  See what's playing without leaving your terminal  
 **Session Stats**  Uptime, viewer counts, connection health  
 **Smart Message Wrapping**  Long messages that actually look good  
 **Private Messages**  Direct communication, terminal-style  
 **Mention Highlighting**  Never miss when someone's talking to you  
 **Cross-Platform**  Windows, Linux, macOS ready

---

##  Quick Start

```bash
# Clone it
git clone https://github.com/grobertson/Juiced.git
cd Juiced

# Install it
pip install -r requirements.txt

# Configure it
cp configs/config.yaml.example configs/config.yaml
nano configs/config.yaml

# Run it
python -m juiced configs/config.yaml
```

**That's it.** You're in.

---

##  Choose Your Fighter

Switch themes on the fly with `/theme <name>`:

| Theme | Vibe |
|-------|------|
| `hal9000` | Menacing red intelligence |
| `r2d2` | Plucky blue optimism |
| `c3po` | Golden protocol perfection |
| `t800` | Cyberdyne red steel |
| `walle` | Rusty heartfelt charm |
| `robocop` | Detroit's finest blue |
| `marvin` | Depressing gray genius |
| `johnny5` | High-contrast alive |

---

##  Built For Beta Testers

This is **v0.2.0**  early, raw, and ready for feedback. DEBUG logging is enabled by default to help us squash bugs together.

**Found a bug?** Open an issue.  
**Have an idea?** Start a discussion.  
**Love it?** Star the repo and tell your friends.

---

##  The Stack

- **blessed**  Terminal rendering magic
- **python-socketio**  Real-time CyTube connection
- **PyYAML**  Human-friendly config
- Pure Python, async/await throughout
- Zero bloat, maximum performance

---

##  License

MIT License  Use it, fork it, make it yours.

---

##  Acknowledgments

Extracted with  from [Rosey-Robot](https://github.com/grobertson/Rosey-Robot)  
Inspired by the golden age of IRC clients  
Built for the CyTube community

---

**Ready to get Juiced?**  [BETA_TESTING.md](BETA_TESTING.md)
