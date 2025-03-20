import requests
import json
from datetime import datetime
import time

def get_mp_constituency(mp_data):
    """Get constituency information from MP data"""
    try:
        # Try to get constituency from membershipFrom
        if 'latestHouseMembership' in mp_data:
            return mp_data['latestHouseMembership'].get('membershipFrom')
        return None
            
    except Exception as e:
        print(f"Error whilst getting constituency from MP data: {e}")
        return None

def fetch_mps():
    # Base URL for the UK Parliament API
    base_url = "https://members-api.parliament.uk/api"
    
    # Initialise empty list to store MP data
    mps_data = []
    
    # Parameters for the API request
    page_size = 20  # Number of MPs per page
    skip = 0
    total_processed = 0
    
    while True:
        # Fetch current MPs with pagination
        endpoint = f"{base_url}/Members/Search"
        params = {
            "House": 1,  # 1 represents House of Commons
            "IsCurrentMember": True,
            "Skip": skip,
            "Take": page_size
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Get total count of MPs
            total_count = data.get("totalResults", 0)
            
            # Process each MP in the current page
            for mp in data.get("items", []):
                try:
                    mp_value = mp['value']
                    mp_id = mp_value['id']
                    
                    # Get constituency information from MP data
                    constituency = get_mp_constituency(mp_value)
                    
                    mp_info = {
                        "name": f"{mp_value['nameDisplayAs']}",
                        "person_id": f"uk.org.publicwhip/person/{mp_id}",
                        "party_affiliation": mp_value['latestParty']['name'],
                        "constituency": constituency or "Unknown",
                        "portrait_URL": f"https://members-api.parliament.uk/api/members/{mp_id}/Portrait?cropType=ThreeFour"
                    }
                    mps_data.append(mp_info)
                    total_processed += 1
                    print(f"Processed MP {total_processed}/{total_count}: {mp_info['name']} - {mp_info['constituency']}")
                    
                except Exception as e:
                    print(f"Error whilst processing MP: {e}")
                    continue
            
            # Check if we've processed all MPs
            if total_processed >= total_count:
                break
                
            # Move to next page
            skip += page_size
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Error whilst fetching MP data: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            # Print the full response for debugging
            if 'response' in locals():
                print("API Response:", json.dumps(data, indent=2))
            break
    
    # Save to JSON file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mps_data_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mps_data, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully fetched data for {len(mps_data)} MPs")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    fetch_mps() 