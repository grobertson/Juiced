"""Juiced - Terminal User Interface for CyTube

A modern, colorful TUI chat client for CyTube rooms, inspired by 
classic IRC clients like BitchX and IRCII, with 11 robot-themed color schemes!
"""

__version__ = '0.2.0'
__author__ = 'Juiced Contributors'
__license__ = 'MIT'

from .tui_bot import TUIBot

__all__ = ['TUIBot']
