#!/usr/bin/env python3
"""Entry point for Juiced - CyTube TUI Chat Client."""

import sys
import asyncio
from pathlib import Path

from juiced import TUIBot
from juiced.lib import get_config


def main():
    """Main entry point for Juiced."""
    # Check for config file argument
    if len(sys.argv) < 2:
        print("Juiced - CyTube Terminal User Interface")
        print("")
        print("Usage: juiced <config.yaml|config.json>")
        print("")
        print("Quick Start:")
        print("  1. Copy configs/config.yaml.example to configs/config.yaml")
        print("  2. Edit config.yaml with your CyTube server and credentials")
        print("  3. Run: juiced configs/config.yaml")
        print("")
        print("For more info, see README.md")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    # Load configuration (get_config reads from sys.argv directly)
    try:
        config, kwargs = get_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        print("")
        print("Make sure your config file exists and is valid YAML or JSON.")
        print("See configs/config.yaml.example for a template.")
        sys.exit(1)
    
    # Extract TUI-specific config
    tui_config = config.pop('tui', {})
    
    # Create and run bot
    bot = TUIBot(config_file, tui_config=tui_config, **kwargs)
    
    try:
        asyncio.run(bot.run_tui())
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
