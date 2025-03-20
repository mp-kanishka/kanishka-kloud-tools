# UK Parliament MP Data Fetcher

This tool fetches current Member of Parliament (MP) data from the UK Parliament API and saves it to a JSON file.

## Features

- Fetches data for all current MPs
- Includes name, person ID, party affiliation, constituency, and portrait URL
- Saves data to a timestamped JSON file
- Utilises the official UK Parliament API

## Requirements

- Python 3.6 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

The repository contains two scripts for fetching MP data:

### 1. MP Data Fetcher (mp_data_fetcher.py)

This script fetches detailed MP information with pagination to handle large datasets:

```bash
python mp_data_fetcher.py
```

The script will:
1. Fetch current MP data from the UK Parliament API
2. Process the data to extract relevant information
3. Save the data to a JSON file named `mps_data_YYYYMMDD_HHMMSS.json`

### 2. Constituency Fetcher (constituency_fetch.py)

This script provides an alternative method to fetch MP data, focusing on constituency information:

```bash
python constituency_fetch.py
```

The script will:
1. Fetch all current MPs in a single request
2. Extract constituency information for each MP
3. Save the data to a JSON file named `mps_data_YYYYMMDD_HHMMSS.json`

## Output Format

The JSON file will contain an array of MP objects, each with the following structure:
```json
{
    "name": "MP Name",
    "person_id": "uk.org.publicwhip/person/12345",
    "party_affiliation": "Party Name",
    "constituency": "Constituency Name",
    "portrait_URL": "https://members-api.parliament.uk/api/members/12345/Portrait?cropType=ThreeFour"
}
``` 