import json
import csv
import sys
from typing import List, Dict

def load_cleaned_statistics(file_path: str = 'cleaned_speaker_statistics.json') -> Dict:
    """Load the cleaned speaker statistics from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file")
        sys.exit(1)

def find_mp_case_insensitive(mp_name: str, statistics: Dict) -> str:
    """Find the exact MP name in statistics using case-insensitive matching."""
    mp_name_lower = mp_name.lower()
    for name in statistics.keys():
        if name.lower() == mp_name_lower:
            return name
    return None

def create_csv_for_mps(mp_names: List[str], output_file: str = 'mp_statistics.csv'):
    """Create a CSV file containing statistics for specified MPs."""
    # Load the cleaned statistics
    statistics = load_cleaned_statistics()
    
    # Prepare the data for CSV
    csv_data = []
    
    for mp_name in mp_names:
        # Find the exact name with correct case
        exact_name = find_mp_case_insensitive(mp_name, statistics)
        
        if not exact_name:
            print(f"Warning: No data found for MP: {mp_name}")
            continue
            
        mp_data = statistics[exact_name]
        
        # Create a row for each word count
        for word, count in mp_data['word_counts'].items():
            csv_data.append({
                'MP_Name': exact_name,  # Use the exact name from the data
                'Person_ID': mp_data['person_id'],
                'Total_Speeches': mp_data['total_speeches'],
                'Word': word,
                'Count': count
            })
    
    # Write to CSV
    if not csv_data:
        print("No data to write to CSV")
        return
        
    fieldnames = ['MP_Name', 'Person_ID', 'Total_Speeches', 'Word', 'Count']
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python CSVMaker.py 'MP Name 1' 'MP Name 2' ...")
        print("Example: python CSVMaker.py 'John Smith' 'Jane Doe'")
        sys.exit(1)
    
    # Get MP names from command line arguments
    mp_names = sys.argv[1:]
    
    # Create the CSV file
    create_csv_for_mps(mp_names)

if __name__ == "__main__":
    main() 