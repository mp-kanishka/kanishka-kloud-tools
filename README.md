# UK Parliament Data Analysis Tools

A collection of Python tools for scraping, processing, and analysing UK Parliamentary data. This repository contains several utilities designed to work together to gather MP information, extract parliamentary debates, standardise MP identifiers, and prepare data for visualisation.

## Repository Contents

This repository contains the following tools:

### 1. MP Profile Scraper

Located in the `MP_Profile_Scraper` directory, this tool fetches current Member of Parliament (MP) data from the UK Parliament API.

**Features:**
- Fetches data for all current MPs
- Includes name, person ID, party affiliation, constituency, and portrait URL
- Saves data to a timestamped JSON file
- Provides two methods for data collection (general MP data and constituency-focused)

### 2. MP Speech Scraper

Located in the `MP_Speech_Scraper` directory, this tool analyses parliamentary debate XML files from TheyWorkForYou.com and tracks word usage statistics for each speaker.

**Features:**
- Downloads and processes debate XML files between specified dates
- Tracks unique words used by each speaker
- Counts frequency of word usage per speaker
- Stores speaker statistics including person ID and total speeches
- Saves results in a JSON format

### 3. MP ID Standardisation

Located in the `MP_ID_Standardise` directory, this tool standardises Member of Parliament (MP) IDs across different parliamentary debate datasets.

**Features:**
- Matches MP names across different datasets using fuzzy matching
- Handles variations in MP names (e.g., "Mr John Smith" vs "John Smith")
- Processes special cases for MPs with multiple name formats
- Creates a mapping between old and new person IDs
- Generates detailed reports of matches and potential issues

### 4. JSON Sanitiser and CSV Maker

Located in the `JSON_Sanitiser` directory, this set of utilities cleans JSON data containing speaker statistics and converts it to CSV format for further analysis.

**Features:**
- Cleans and filters word count data from JSON files
- Removes stop words, single characters, numbers, and common parts of speech
- Extracts data for specified MPs and converts to CSV format
- Prepares data for visualisation tools like word clouds

## Workflow

These tools are designed to work together in the following workflow:

1. Use **MP Profile Scraper** to fetch current MP data with official IDs
2. Use **MP Speech Scraper** to download and analyse parliamentary debates
3. Use **MP ID Standardisation** to ensure consistent MP identification across datasets
4. Use **JSON Sanitiser and CSV Maker** to clean the data and prepare it for visualisation

## Requirements

Each tool has its own specific requirements listed in its respective directory. Generally, you'll need:

- Python 3.6+
- Various Python packages (see `requirements.txt` in each directory)

## Usage

Please refer to the README.md file in each tool's directory for specific usage instructions.

## Licence

This project is available for use under the MIT Licence.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 