# Parliamentary Debate Word Counter

This script analyses parliamentary debate XML files from TheyWorkForYou.com and tracks word usage statistics for each speaker.

## Features

- Downloads and processes debate XML files between specified dates
- Tracks unique words used by each speaker
- Counts frequency of word usage per speaker
- Stores speaker statistics including person ID and total speeches
- Saves results in a JSON format

## Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Open `parse_debates.py` and modify the date range in the `main()` function:
```python
start_date = "2024-01-01"  # Format: YYYY-MM-DD
end_date = "2024-12-31"    # Format: YYYY-MM-DD
```

2. Run the script:
```bash
python parse_debates.py
```

## Output

The script generates a `speaker_statistics.json` file containing:
- Speaker names
- Person IDs
- Total number of speeches
- Word frequency counts

The JSON structure looks like:
```json
{
  "Speaker Name": {
    "person_id": "123",
    "total_speeches": 10,
    "word_counts": {
      "word1": 5,
      "word2": 3,
      ...
    }
  }
}
```

## Notes

- The script processes both main debates and Westminster Hall debates
- The script omits single-letter words
- All words are converted to lowercase for consistency
- Unknown speakers are excluded from the analysis 