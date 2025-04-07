#!/usr/bin/env python3
"""
Runner script for Vyorius Comment Moderation Tool

This tool uses the Gemini API for comment moderation by default.
For demo/testing without API calls, use the --mock-mode flag.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the CLI
from vyorius_comment_moderator.cli import cli

if __name__ == '__main__':
    print("\n📊 Vyorius Comment Moderation Tool 📊")
    print("Using Gemini API for comment moderation.")
    print("For testing without API calls, use the --mock-mode flag.\n")
    # Run the CLI
    cli() 