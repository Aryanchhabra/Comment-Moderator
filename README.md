# Vyorius Comment Moderation Tool

A Python application that reads user comments from local files (CSV or JSON), uses Google's Gemini API to detect offensive or inappropriate content, and generates comprehensive reports of flagged comments.

> **Note:** This tool uses the Gemini API for content moderation by default, as required by the project guidelines. For testing without API calls, use the `--mock-mode` flag.

> **Important:** If you encounter API quota limitations with the message "You exceeded your current quota", please use the `--mock-mode` flag to run the application with simulated AI responses.

## Overview

This tool is designed for Vyorius Drones to help moderate user comments across their platforms. It provides automated detection of various types of offensive content including:

- Hate speech
- Harassment
- Profanity
- Threats
- Misinformation
- General toxicity

## Features

- **Flexible Data Loading**: Support for both CSV and JSON comment data formats
- **Advanced AI Detection**: Leverages Google's Gemini API for accurate content moderation
- **Profanity Pre-filtering**: Optimizes API usage by pre-filtering obvious profanity
- **Comprehensive Reports**: Generates detailed reports in multiple formats:
  - Console output with color-coded severity indicators
  - Exportable CSV/JSON with moderation results
  - Interactive HTML reports with visualizations
  - Offense type distribution charts
- **User-friendly CLI**: Simple command-line interface for all operations
- **Graceful Fallback**: Automatically falls back to keyword-based detection if API is unavailable

## Installation

### Prerequisites

- Python 3.8 or higher
- A Gemini API key from the Google AI Studio

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Aryanchhabra/Comment-Moderator.git
cd Comment-Moderator
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Create a `.env` file in the root directory based on the provided `.env.example`
   - Add your Gemini API key to the `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

## Quick Start

The fastest way to see the tool in action (with mock AI responses):

```bash
# Clone the repository
git clone https://github.com/Aryanchhabra/Comment-Moderator.git
cd Comment-Moderator

# Install dependencies
pip install -r requirements.txt

# Run with sample data in mock mode
python run_moderator.py moderate vyorius_comment_moderator/data/comments.csv --mock-mode --generate-html --generate-plot
```

## Usage

### Basic Usage

Analyze comments from a file:

```bash
python run_moderator.py moderate vyorius_comment_moderator/data/comments.csv
```

This will:
1. Load comments from the CSV file
2. Analyze each comment using the Gemini AI model to detect offensive content
3. Generate a console report
4. Save the analyzed data to a new file in the same format

### Testing Without API

For testing or demonstration without making API calls:

```bash
python run_moderator.py moderate vyorius_comment_moderator/data/comments.csv --mock-mode
```

This will use keyword matching instead of the AI API.

### Preview Comments

To preview comments without performing moderation:

```bash
python run_moderator.py preview vyorius_comment_moderator/data/comments.csv
```

### Additional Options

The tool supports various options:

```bash
python run_moderator.py moderate vyorius_comment_moderator/data/comments.csv \
  --output-file=vyorius_comment_moderator/output/analyzed_comments.csv \
  --generate-html \
  --generate-plot
```

- `--output-file` / `-o`: Specify the output file path
- `--api-key` / `-k`: Provide a Gemini API key (overrides .env file)
- `--use-profanity-filter` / `--no-profanity-filter`: Enable/disable profanity pre-filtering
- `--generate-html` / `--no-html`: Generate an HTML report
- `--generate-plot` / `--no-plot`: Generate an offense type distribution plot
- `--mock-mode` / `--api-mode`: Run with keyword matching or actual API calls

## Input Data Format

The tool expects input files in CSV or JSON format with the following required fields:

- `comment_id`: Unique identifier for the comment
- `username`: User who posted the comment
- `comment_text`: The actual comment text to analyze

Example CSV:
```csv
comment_id,username,comment_text
1,user123,"This is a comment"
2,drone_fan,"Amazing product!"
```

**Important**: For CSV files, make sure to quote the comment text to handle commas within comments.

Example JSON:
```json
[
  {
    "comment_id": 1,
    "username": "user123",
    "comment_text": "This is a comment"
  },
  {
    "comment_id": 2, 
    "username": "drone_fan",
    "comment_text": "Amazing product!"
  }
]
```

## Output Format

The tool adds the following fields to each comment:

- `is_offensive`: Boolean indicating if the comment was flagged as offensive
- `offense_type`: The type of offense detected (e.g., hate_speech, profanity)
- `explanation`: A brief explanation of why the comment was flagged
- `pre_filtered`: Boolean indicating if the comment was caught by the profanity filter
- `mock_mode`: Boolean indicating if the result was generated using mock mode

## Sample Output

### Console Report

```
============================================================
           📊 COMMENT MODERATION SUMMARY REPORT 📊
============================================================

📝 TOTAL COMMENTS: 20
🚨 OFFENSIVE COMMENTS: 8 (40.0%)
⚡ PRE-FILTERED BY PROFANITY DETECTOR: 2

📋 OFFENSE TYPE BREAKDOWN:
  • profanity: 3 comments
  • harassment: 2 comments
  • hate_speech: 1 comments
  • threat: 1 comments
  • toxicity: 1 comments

⚠️ TOP OFFENSIVE COMMENTS:
  1. [ID: 5] by angry_neighbor
     "These f***ing drones keep violating my privacy! I will shoot them down next time!"
     Type: threat | Contains explicit language and threat of violence

  2. [ID: 18] by racist_user
     "These foreigners don't know how to make proper technology. Go back to your country!"
     Type: hate_speech | Comment contains xenophobic sentiment targeting nationality
============================================================
```

### HTML Report

The HTML report provides a visually appealing, interactive presentation of the moderation results, including:

- Summary statistics
- Offense type breakdown
- Top offensive comments with color-coded severity

### Visualization

The tool generates bar charts visualizing the distribution of offense types among flagged comments in PNG format.

## Troubleshooting

### API Quota Issues

If you encounter the error `429 You exceeded your current quota`, you have options:

1. Use the `--mock-mode` flag to run without API calls
2. Get a new API key with higher quota from Google AI Studio
3. Add billing information to your Google Cloud account

### CSV Parsing Errors

If you get an error like `Error tokenizing data. Expected 3 fields in line X, saw 4`, make sure:
- All comment text fields are properly quoted in the CSV
- No unescaped quotes within the comments

## Architecture

The application is organized into the following modules:

- `comment_loader.py`: Handles loading and parsing comment data
- `content_moderator.py`: Performs content moderation using Gemini API
- `report_generator.py`: Generates reports and visualizations
- `cli.py`: Command-line interface
- `main.py`: Main application entry point

## Project Structure

```
vyorius_comment_moderator/
├── data/                  # Sample data and output files
│   └── comments.csv       # Sample comments for testing
├── output/                # Generated output files (created on first run)
├── .env.example           # Template for API key configuration
├── __init__.py            # Package initialization
├── cli.py                 # Command-line interface
├── comment_loader.py      # Data loading utilities
├── content_moderator.py   # Comment moderation logic
├── main.py                # Application entry point
├── report_generator.py    # Report generation utilities
│
├── .env                   # Your API key (create this file, not included in repo)
├── requirements.txt       # Project dependencies
├── run_moderator.py       # Convenience script to run the tool
└── README.md              # This documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google's Gemini API for AI content moderation
- Vyorius Drones for the opportunity to develop this tool

## Author

Created by [Aryan Chhabra](https://github.com/Aryanchhabra) as part of the Vyorius AI Moderation & Automation Intern assessment. 