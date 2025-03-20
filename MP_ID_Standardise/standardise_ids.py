import json
from typing import Dict, List
import difflib

def load_json_file(filename: str) -> Dict:
    with open(filename, 'r') as f:
        return json.load(f)

def save_json_file(data: Dict, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_name_similarity(name1: str, name2: str) -> float:
    # Special case mappings
    special_cases = {
        "Tanmanjeet Singh Dhesi": "Tan Dhesi",
        "Mr Tanmanjeet Singh Dhesi": "Tan Dhesi",
        "Steff Aquarone": "Steffan Aquarone",
        "Jess Asato": "Jessica Asato",
        "Chris Bloore": "Christopher Bloore",
        "Jess Brown-Fuller": "Jessica Brown-Fuller",
        "Al Carns": "Alistair Carns",
        "Jen Craft": "Jennifer Craft",
        "Ed Davey": "Edward Davey",
        "Mary Kelly Foy": "Mary Foy",
        "Jon Pearce": "Jonathan Pearce"
    }
    
    # Apply special case mapping if exists
    if name1 in special_cases:
        name1 = special_cases[name1]
    if name2 in special_cases:
        name2 = special_cases[name2]
    
    # Remove all titles and clean names
    titles = ['Ms', 'Mrs', 'Mr', 'Dr', 'Sir', 'Dame', 'Lady']
    clean_name1 = name1
    clean_name2 = name2
    
    for title in titles:
        clean_name1 = clean_name1.replace(f"{title} ", "").strip()
        clean_name2 = clean_name2.replace(f"{title} ", "").strip()
    
    # Convert to lowercase for comparison
    clean_name1 = clean_name1.lower()
    clean_name2 = clean_name2.lower()
    
    # If exact match after cleaning, return 1.0
    if clean_name1 == clean_name2:
        return 1.0
        
    # Split names into parts
    name1_parts = clean_name1.split()
    name2_parts = clean_name2.split()
    
    # If first and last names match exactly, return high similarity
    if len(name1_parts) > 0 and len(name2_parts) > 0:
        if name1_parts[0] == name2_parts[0] and name1_parts[-1] == name2_parts[-1]:
            return 0.95
    
    # For fuzzy matching, only consider names that share the same first name
    if len(name1_parts) > 0 and len(name2_parts) > 0:
        if name1_parts[0] != name2_parts[0]:
            return 0.0  # Don't match names with different first names
    
    # Calculate similarity for remaining cases
    return difflib.SequenceMatcher(None, clean_name1, clean_name2).ratio()

def match_mps(mps_data: List[Dict], speaker_stats: Dict, similarity_threshold: float = 0.75) -> Dict:
    # Create a mapping of old person_ids to new ones
    id_mapping = {}
    unmatched_mps = []
    needs_review = []  # Store matches below 0.85 for review
    
    # Create cleaned name mappings to avoid repeated cleaning
    cleaned_mp_names = {}
    cleaned_speaker_names = {}
    mp_id_by_clean_name = {}  # Store MP IDs by cleaned name for exact matching
    speaker_id_by_clean_name = {}  # Store speaker IDs by cleaned name for exact matching
    
    # Clean all names once and store mappings
    titles = ['Ms', 'Mrs', 'Mr', 'Dr', 'Sir', 'Dame', 'Lady']
    
    def clean_name(name: str) -> str:
        clean = name
        for title in titles:
            clean = clean.replace(f"{title} ", "").strip()
        return clean.lower()
    
    # Special case mappings
    special_cases = {
        "Tanmanjeet Singh Dhesi": "Tan Dhesi",
        "Mr Tanmanjeet Singh Dhesi": "Tan Dhesi",
        "Steff Aquarone": "Steffan Aquarone",
        "Jess Asato": "Jessica Asato",
        "Chris Bloore": "Christopher Bloore",
        "Jess Brown-Fuller": "Jessica Brown-Fuller",
        "Al Carns": "Alistair Carns",
        "Jen Craft": "Jennifer Craft",
        "Ed Davey": "Edward Davey",
        "Mary Kelly Foy": "Mary Foy",
        "Jon Pearce": "Jonathan Pearce"
    }
    
    # Clean and store MP names
    print("\nProcessing MP names...")
    for mp in mps_data:
        original_name = mp['name']
        # Apply special case mapping if exists
        if original_name in special_cases:
            original_name = special_cases[original_name]
            
        clean_name_val = clean_name(original_name)
        cleaned_mp_names[mp['name']] = clean_name_val
        mp_id_by_clean_name[clean_name_val] = mp['person_id']
    
    # Clean and store speaker names
    print("\nProcessing speaker names...")
    for speaker_name, speaker_data in speaker_stats.items():
        # Apply special case mapping if exists
        if speaker_name in special_cases:
            speaker_name = special_cases[speaker_name]
            
        clean_name_val = clean_name(speaker_name)
        cleaned_speaker_names[speaker_name] = clean_name_val
        speaker_id_by_clean_name[clean_name_val] = speaker_data.get('person_id')
    
    # Track which names have been matched
    matched_mp_names = set()
    matched_speaker_names = set()
    
    # First pass: Find exact matches using cleaned names
    print("\nFinding exact matches...")
    for mp in mps_data:
        mp_name = mp['name']
        if mp_name in special_cases:
            mp_name = special_cases[mp_name]
        clean_mp_name = cleaned_mp_names[mp['name']]
        
        # Look for exact matches in speaker names
        for speaker_name, speaker_data in speaker_stats.items():
            if speaker_name in special_cases:
                speaker_name = special_cases[speaker_name]
            clean_speaker_name = cleaned_speaker_names[speaker_name]
            
            if clean_mp_name == clean_speaker_name:
                id_mapping[mp['person_id']] = speaker_data.get('person_id')
                matched_mp_names.add(mp_name)
                matched_speaker_names.add(speaker_name)
                print(f"Exact match found: {mp_name} -> {speaker_name}")
                break
    
    # Second pass: Only try fuzzy matching for names that didn't have exact matches
    print("\nAttempting fuzzy matches for remaining names...")
    for mp in mps_data:
        mp_name = mp['name']
        if mp_name in special_cases:
            mp_name = special_cases[mp_name]
            
        # Skip if we already found an exact match
        if mp_name in matched_mp_names:
            continue
            
        matched = False
        best_match = None
        best_similarity = similarity_threshold
        
        for speaker_name, speaker_data in speaker_stats.items():
            if speaker_name in special_cases:
                speaker_name = special_cases[speaker_name]
                
            # Skip if this speaker name was exactly matched to someone else
            if speaker_name in matched_speaker_names:
                continue
                
            # Calculate similarity
            clean_mp_name = cleaned_mp_names[mp['name']]
            clean_speaker_name = cleaned_speaker_names[speaker_name]
            
            # Split names into parts for comparison
            mp_parts = clean_mp_name.split()
            speaker_parts = clean_speaker_name.split()
            
            # Only proceed if first names match
            if len(mp_parts) > 0 and len(speaker_parts) > 0 and mp_parts[0] == speaker_parts[0]:
                similarity = difflib.SequenceMatcher(None, clean_mp_name, clean_speaker_name).ratio()
                
                # Update best match if this is better
                if similarity >= best_similarity:
                    best_similarity = similarity
                    best_match = (speaker_name, speaker_data.get('person_id'), similarity)
        
        # If we found a fuzzy match, use it
        if best_match:
            speaker_name, new_id, similarity = best_match
            id_mapping[mp['person_id']] = new_id
            matched = True
            if similarity < 0.85:
                needs_review.append({
                    'mp_name': mp_name,
                    'matched_name': speaker_name,
                    'similarity': similarity,
                    'old_id': mp['person_id'],
                    'new_id': new_id
                })
        
        if not matched:
            unmatched_mps.append(mp_name)
    
    # Print matches that need review
    if needs_review:
        print("\nWarning: The following matches are below 0.85 similarity and should be reviewed:")
        for match in needs_review:
            print(f"- {match['mp_name']} -> {match['matched_name']}")
            print(f"  Similarity: {match['similarity']:.3f}")
            print(f"  ID Change: {match['old_id']} -> {match['new_id']}")
            print()
    
    # Print unmatched MPs for review
    if unmatched_mps:
        print("\nWarning: The following MPs could not be matched:")
        for name in unmatched_mps:
            print(f"- {name}")
            # Also print their current ID for reference
            for mp in mps_data:
                if mp['name'] == name:
                    print(f"  Current ID: {mp['person_id']}")
    
    return id_mapping

def main():
    # Load the data files
    print("Loading data files...")
    mps_data = load_json_file('mps_data_20250307_093055.json')
    speaker_stats = load_json_file('combined_speaker_statistics.json')
    
    # Match MPs and create ID mapping
    print("Matching MPs between files...")
    id_mapping = match_mps(mps_data, speaker_stats)
    
    # Create a backup of the original file
    print("Creating backup of original MPs data...")
    save_json_file(mps_data, 'mps_data_20250307_093055.backup.json')
    
    # Update person_ids in mps_data
    print("Updating person IDs...")
    updated_count = 0
    for mp in mps_data:
        old_id = mp['person_id']
        if old_id in id_mapping:
            mp['person_id'] = id_mapping[old_id]
            updated_count += 1
            print(f"Updated {mp['name']}: {old_id} -> {mp['person_id']}")
    
    # Save the updated data
    print("Saving updated data...")
    save_json_file(mps_data, 'mps_data_20250307_093055.json')
    
    # Print summary
    print(f"\nSummary:")
    print(f"Total MPs processed: {len(mps_data)}")
    print(f"IDs updated: {updated_count}")
    print(f"IDs unchanged: {len(mps_data) - updated_count}")
    
    if updated_count < len(mps_data):
        print("\nNote: Some MPs could not be matched. Check the warnings above for details.")
        print("You may want to adjust the similarity threshold or manually review these cases.")

if __name__ == "__main__":
    main() 