import requests
import json
from datetime import datetime
import time

def fetch_constituency(constituency_id):
    """Fetch constituency information using the constituency ID."""
    url = f"https://members-api.parliament.uk/api/Location/Constituency/{constituency_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('value', {}).get('name', '')
    except Exception as e:
        print(f"Error fetching constituency {constituency_id}: {e}")
        return ''

def fetch_mps_constituencies():
    # Base URL for the UK Parliament API
    base_url = "https://members-api.parliament.uk/api/Members/Search"
    
    # Parameters for the API request
    params = {
        "House": 1,  # 1 represents House of Commons
        "skip": 0,
        "take": 650,  # Maximum number of MPs to fetch
        "IncludeFormerMembers": False  # Only get current MPs
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract MPs data
        mps_data = []
        for mp in data.get('items', []):
            value = mp.get('value', {})
            latest_membership = value.get('latestHouseMembership', {})
            constituency = latest_membership.get('constituency', {})
            
            mp_info = {
                "name": value.get('nameDisplayAs', ''),
                "person_id": value.get('id', ''),
                "party_affiliation": value.get('latestParty', {}).get('name', ''),
                "constituency": constituency.get('name', ''),
                "portrait_URL": f"https://members-api.parliament.uk/api/members/{value.get('id', '')}/Portrait?cropType=ThreeFour"
            }
            mps_data.append(mp_info)
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.1)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mps_data_{timestamp}.json"
        
        # Save to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(mps_data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully fetched data for {len(mps_data)} MPs")
        print(f"Data saved to {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_mps_constituencies() 