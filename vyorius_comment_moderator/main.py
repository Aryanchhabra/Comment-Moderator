#!/usr/bin/env python3
"""
Vyorius Comment Moderation Tool

A Python application that reads user comments from a local file,
uses Gemini AI to detect offensive or inappropriate content,
and generates a report of flagged comments.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)

# Import the CLI using relative import
from vyorius_comment_moderator.cli import cli

if __name__ == '__main__':
    # Run the CLI
    cli() 