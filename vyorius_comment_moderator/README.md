# Vyorius Comment Moderation Tool

A Python application that reads user comments from local files (CSV or JSON), uses Google's Gemini AI to detect offensive or inappropriate content, and generates comprehensive reports of flagged comments.

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

## Installation

### Prerequisites

- Python 3.8 or higher
- A Gemini API key from the Google AI Studio

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd vyorius_comment_moderator
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

## Usage

### Basic Usage

Analyze comments from a file:

```bash
python main.py moderate data/comments.csv
```

This will:
1. Load comments from the CSV file
2. Analyze each comment for offensive content
3. Generate a console report
4. Save the analyzed data to a new file in the same format

### Preview Comments

To preview comments without performing moderation:

```bash
python main.py preview data/comments.csv
```

### Additional Options

The tool supports various options:

```bash
python main.py moderate data/comments.csv \
  --output-file=output/analyzed_comments.csv \
  --use-profanity-filter \
  --generate-html \
  --generate-plot
```

- `--output-file` / `-o`: Specify the output file path
- `--api-key` / `-k`: Provide a Gemini API key (overrides .env file)
- `--use-profanity-filter` / `--no-profanity-filter`: Enable/disable profanity pre-filtering
- `--generate-html` / `--no-html`: Generate an HTML report
- `--generate-plot` / `--no-plot`: Generate an offense type distribution plot

## Input Data Format

The tool expects input files in CSV or JSON format with the following required fields:

- `comment_id`: Unique identifier for the comment
- `username`: User who posted the comment
- `comment_text`: The actual comment text to analyze

Example CSV:
```csv
comment_id,username,comment_text
1,user123,This is a comment
2,drone_fan,Amazing product!
```

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

The tool can generate bar charts or pie charts visualizing the distribution of offense types among flagged comments.

## Architecture

The application is organized into the following modules:

- `comment_loader.py`: Handles loading and parsing comment data
- `content_moderator.py`: Performs content moderation using Gemini API
- `report_generator.py`: Generates reports and visualizations
- `cli.py`: Command-line interface
- `main.py`: Main application entry point

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google's Gemini API for AI content moderation
- Vyorius Drones for the opportunity to develop this tool 