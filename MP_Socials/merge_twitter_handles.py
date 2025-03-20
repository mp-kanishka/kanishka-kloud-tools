import json
from datetime import datetime

def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    # Load both JSON files
    mps_data = load_json_file('mps_data_20250307_093055.json')
    twitter_data = load_json_file('mp_twitter_20250311_201554.json')

    # Create a dictionary mapping names to Twitter handles
    twitter_handles = {mp['name']: mp['twitter_handle'] for mp in twitter_data}

    # Update MPs data with Twitter handles
    for mp in mps_data:
        mp['twitter_handle'] = twitter_handles.get(mp['name'])

    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'mps_data_with_twitter_{timestamp}.json'

    # Save the updated data
    save_json_file(mps_data, output_filename)
    print(f'Updated data saved to {output_filename}')

if __name__ == '__main__':
    main() 