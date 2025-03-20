# MP Social Media Collector

A Python-based tool for collecting and managing social media handles for Members of Parliament in the United Kingdom.

## Overview

This tool interfaces with the UK Parliament Members API to fetch and collate social media information for current MPs. It specifically focuses on gathering X (formerly Twitter) handles through both the official Parliament API and supplementary web searches.

## Features

- Fetches current MP data from the official Parliament API
- Extracts X/Twitter handles from MP contact information
- Generates detailed statistics about MP social media presence
- Exports data in JSON format with timestamps

## Requirements

```
requests
json
typing
datetime
re
```

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the main script to collect MP Twitter handles:
```bash
python get_mp_twitter.py
```


### Output

The scripts generate JSON files with timestamps containing:
- MP names
- Twitter handles (where available)
- Collection statistics

Example output format:
```json
{
    "name": "MP Name",
    "twitter_handle": "@handle"
}
```

## Statistics

The tool provides:
- Total number of MPs
- Number of MPs with social media handles
- Percentage of MPs with social media presence

## Rate Limiting

The tool implements appropriate rate limiting to respect API constraints:
- 0.1 second delay between API calls
- 2 second delay between web searches

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.