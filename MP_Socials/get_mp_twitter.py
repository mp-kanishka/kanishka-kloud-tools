import requests
import json
from typing import List, Dict
import time
from datetime import datetime

def get_mp_contact_details(mp_id: int) -> str:
    """
    Get MP's contact details including Twitter handle using the Members API Contact endpoint.
    """
    url = f"https://members-api.parliament.uk/api/Members/{mp_id}/Contact"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Debug: Print first MP's contact data
        if mp_id == 172:  # Diane Abbott's ID
            print("\nDebug - Contact data for Diane Abbott:")
            print(json.dumps(data, indent=2))
        
        # Look for Twitter in contact details
        if 'value' in data:
            for contact in data['value']:
                # Debug: Print contact type for first MP
                if mp_id == 172:
                    print(f"Contact type: {contact.get('type')}")
                    print(f"Contact value: {contact}")
                
                if contact.get('type') == 'X (formerly Twitter)':
                    # Extract handle from the URL in line1
                    twitter_url = contact.get('line1', '')
                    if twitter_url:
                        handle = twitter_url.split('/')[-1]
                        print(f"\nFound Twitter handle for MP {mp_id}: {handle}")
                        return handle
            print(f"\nNo Twitter handle found in contact details for MP {mp_id}")
        return None
    except Exception as e:
        print(f"\nError fetching contact details for MP {mp_id}: {e}")
        return None

def get_all_mps() -> List[Dict]:
    """
    Fetch all current MPs using the Members API.
    """
    base_url = "https://members-api.parliament.uk/api/Members/Search"
    params = {
        "IsCurrentMember": True,
        "House": "Commons",
        "skip": 0,
        "take": 20
    }
    
    all_mps = []
    total_fetched = 0
    
    while True:
        try:
            print(f"\rFetching MPs {total_fetched + 1}-{total_fetched + params['take']}...", end="")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('items'):
                break
            
            # Process each MP
            for mp in data['items']:
                mp_id = mp['value']['id']
                twitter_handle = get_mp_contact_details(mp_id)
                if twitter_handle:
                    print(f"\nFound Twitter handle for {mp['value']['nameDisplayAs']}: {twitter_handle}")
                mp['twitter_handle'] = twitter_handle
                time.sleep(0.1)  # Rate limiting
            
            all_mps.extend(data['items'])
            total_fetched += len(data['items'])
            
            if len(data['items']) < params['take'] or total_fetched >= data.get('totalResults', 0):
                break
                
            params['skip'] += params['take']
            
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching MPs: {e}")
            break
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Saving current progress...")
            break
    
    print(f"\nFetched {len(all_mps)} MPs in total")
    return all_mps

def extract_mp_info(mps_data: List[Dict]) -> List[Dict]:
    """
    Extract just the MP names and Twitter handles.
    """
    mp_info = []
    print("\nMPs without Twitter handles:")
    print("-" * 25)
    
    for mp in mps_data:
        info = {
            "name": mp['value']['nameDisplayAs'],
            "twitter_handle": mp['twitter_handle']
        }
        if not mp['twitter_handle']:
            print(f"- {info['name']}")
        mp_info.append(info)
    
    print("-" * 25)
    return mp_info

def save_to_json(data: List[Dict], filename: str = None):
    """
    Save the MP data to a JSON file with timestamp.
    """
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'mp_twitter_{timestamp}.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nData successfully saved to {filename}")
        
        # Print first few entries from saved file
        print("\nFirst few entries from saved file:")
        with open(filename, 'r') as f:
            saved_data = json.load(f)
            for entry in saved_data[:5]:
                print(json.dumps(entry, indent=2))
    except Exception as e:
        print(f"Error saving data to file: {e}")

def main():
    print("Starting MP Twitter handle collection...")
    mps_data = get_all_mps()
    
    if not mps_data:
        print("No MP data was fetched. Exiting.")
        return
    
    print("\nExtracting Twitter handles...")
    mp_twitter_info = extract_mp_info(mps_data)
    
    # Print some statistics
    total_mps = len(mp_twitter_info)
    mps_with_twitter = sum(1 for mp in mp_twitter_info if mp['twitter_handle'])
    print(f"\nStatistics:")
    print(f"Total MPs found: {total_mps}")
    print(f"MPs with Twitter handles: {mps_with_twitter}")
    print(f"Percentage with Twitter: {(mps_with_twitter/total_mps)*100:.1f}%")
    
    # Save the data
    save_to_json(mp_twitter_info)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...") 