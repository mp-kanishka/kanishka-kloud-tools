# JSON Sanitiser and CSV Maker

A set of Python utilities for cleaning JSON data containing speaker statistics and converting it to CSV format for further analysis.

## Overview

This repository contains two main scripts:

1. **sanitise_json.py**: Cleans and filters word count data from a JSON file containing speaker statistics.
2. **CSVMaker.py**: Converts the cleaned JSON data into CSV format for specific speakers.

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`:
  - nltk==3.8.1
  - spacy>=3.7.2

To install the required dependencies:

```bash
pip install -r requirements.txt
```

You'll also need to download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

### 1. Sanitise JSON Data

The `sanitise_json.py` script processes a JSON file containing speaker statistics and filters out unwanted words based on linguistic analysis.

```bash
python sanitise_json.py
```

**Input**: The script expects a file named `combined_speaker_statistics.json` in the current directory.

**Output**: The script produces a file named `cleaned_speaker_statistics.json` with filtered word counts.

**How it works**:
- Loads the original JSON data
- For each speaker, filters their word counts using spaCy's linguistic analysis
- Removes stop words, single characters, numbers, and common parts of speech
- Saves the cleaned data to a new JSON file

### 2. Create CSV for Specific MPs

The `CSVMaker.py` script extracts data for specified MPs from the cleaned JSON and converts it to CSV format.

```bash
python CSVMaker.py 'MP Name 1' 'MP Name 2' 'MP Name 3'
```

**Input**: 
- The script uses the `cleaned_speaker_statistics.json` file created by `sanitise_json.py`
- MP names are provided as command-line arguments

**Output**: The script produces a file named `mp_statistics.csv` containing the extracted data.

**How it works**:
- Loads the cleaned JSON data
- Finds the specified MPs (case-insensitive matching)
- For each MP, extracts their word count data
- Converts the data to CSV format with columns for MP name, person ID, total speeches, word, and count

## Example

1. First, clean the JSON data:
   ```bash
   python sanitise_json.py
   ```

2. Then, create a CSV for specific MPs:
   ```bash
   python CSVMaker.py 'Boris Johnson' 'Rishi Sunak'
   ```

## Notes

- The MP name matching is case-insensitive, so 'boris johnson' will match 'Boris Johnson' in the data.
- If an MP name is not found in the data, a warning message will be displayed.
- The CSV output includes one row per word per MP, making it suitable for further analysis or visualisation.

## Licence

This project is available for use under the MIT Licence. 