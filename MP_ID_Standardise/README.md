# Parliamentary MP ID Standardisation

This Python script standardises Member of Parliament (MP) IDs across different parliamentary debate datasets, ensuring consistent identification of MPs across various parliamentary records.

## Features

- Matches MP names across different datasets using fuzzy matching
- Handles variations in MP names (e.g., "Mr John Smith" vs "John Smith")
- Processes special cases for MPs with multiple name formats
- Creates a mapping between old and new person IDs
- Generates detailed reports of matches and potential issues

## Requirements

- Python 3.6 or higher
- Required packages:
  ```bash
  pip install difflib
  ```

## Usage

The script can be run with the following command:

```bash
python standardize_ids.py
```

### Input Files

The script expects two JSON files:
1. `mps_data_[timestamp].json`: Current MP data with person IDs
2. `combined_speaker_statistics.json`: Speaker statistics with alternative person IDs

### Output

The script generates:
1. A backup of the original MP data file
2. An updated version of the MP data file with standardised IDs
3. Console output showing:
   - Exact matches found
   - Fuzzy matches with similarity scores
   - Warnings for matches below 0.85 similarity
   - List of unmatched MPs

## Name Matching Process

The script performs name matching in several stages:

1. **Special Case Handling**
   - Processes known variations of MP names
   - Examples:
     - "Tanmanjeet Singh Dhesi" → "Tan Dhesi"
     - "Steff Aquarone" → "Steffan Aquarone"
     - "Jess Asato" → "Jessica Asato"

2. **Title Removal**
   - Removes common titles before comparison:
     - Ms, Mrs, Mr, Dr, Sir, Dame, Lady

3. **Matching Methods**
   - Exact matching using cleaned names
   - Fuzzy matching for similar names
   - First name verification to prevent false matches

## Output Format

The updated MP data maintains the original structure:
```json
{
  "name": "MP Name",
  "person_id": "uk.org.publicwhip/person/123",
  "party_affiliation": "Party Name",
  "constituency": "Constituency Name",
  "portrait_URL": "https://members-api.parliament.uk/api/members/123/Portrait?cropType=ThreeFour"
}
```

## Notes

- Maintains British English spelling throughout
- Preserves original portrait URLs
- Creates backups before modifying data
- Provides detailed logging of the standardisation process
- Flags potential issues for manual review

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Licence

This project is licensed under the MIT Licence - see the `LICENCE.md` file for details. 