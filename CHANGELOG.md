# Changelog

All notable changes to Juiced will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.6] - 2025-11-14

### Fixed
- Message wrapping now works correctly for all messages (no more truncation)
- Tab completion works with usernames containing underscores
- Emote tab completion now uses actual channel emotes from CyTube
- Fixed startup crash with get_config() argument error
- AFK users now display with dim + italic formatting for better visibility
- User list now sorts by rank hierarchy (Owner > Admin > Mod > User)
- Mods always display at top of user list even when AFK

### Added
- Interactive setup scripts (setup.bat / setup.sh) for easy installation
- Automated config file setup with prompts for credentials
- Virtual environment detection and warnings in launchers
- Comprehensive INSTALL.md guide for new users
- emoteList event handler for receiving channel-specific emotes

### Changed
- User list sorting now prioritizes by rank, then alphabetically
- Setup scripts now prompt for channel, username, and password
- Improved launcher scripts with helpful warnings

## [0.2.0] - 2025-11-14

### Added
- Initial beta release of Juiced! 
- Full-featured TUI chat client for CyTube
- 11 robot-themed color schemes (HAL 9000, R2-D2, C-3PO, T-800, WALL-E, RoboCop, Robby, Marvin, Johnny 5, Data, Default)
- Smart tab completion for usernames and emotes
- Scrollable chat history (1000+ messages)
- Live user list with rank-based coloring
- Media information display (now playing, duration, remaining)
- Session statistics (uptime, viewer counts)
- Auto-logging (chat history and errors)
- Responsive terminal layout
- Full keyboard navigation
- Command system (/help, /theme, /pm, /users, etc.)
- YAML and JSON configuration support
- Cross-platform support (Windows, Linux, macOS)
- Message wrapping for long text
- Mention highlighting
- Private message support
- Join/quit message toggles
- 12h/24h clock format options
- AFK user hiding option

### Technical
- Standalone package structure
- Pure Python implementation
- Async/await throughout
- Minimal dependencies
- MIT licensed

### Notes
- This is an early beta release
- Extracted from Rosey-Robot project
- Proving so useful everyone wanted to try it!
- Expect improvements and refinements in future versions

## [Unreleased]

### Planned for v0.3.0
- Code cleanup and refactoring
- Performance optimizations
- Enhanced error handling
- Better documentation
- Bug fixes from beta testing feedback

### Future Features
- Multi-channel support (Alt+1-9 switching)
- Audio notifications
- Custom theme editor
- Plugin system
- Performance monitoring
- Mouse support
- Playlist management improvements
- Enhanced moderation tools

---

For more information, see [README.md](README.md)
