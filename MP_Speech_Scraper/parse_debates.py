import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
import re
from collections import defaultdict
from tqdm import tqdm
import os
from typing import Dict, Set, List
import json

class SpeakerStats:
    def __init__(self):
        self.word_counts = defaultdict(int)
        self.total_speeches = 0
        self.person_id = None

class DebateParser:
    def __init__(self):
        self.base_urls = [
            "https://www.theyworkforyou.com/pwdata/scrapedxml/debates/",
            "https://www.theyworkforyou.com/pwdata/scrapedxml/westminhall/"
        ]
        self.speakers: Dict[str, SpeakerStats] = defaultdict(SpeakerStats)
        
    def get_debate_files(self, start_date: str, end_date: str) -> List[str]:
        """Get list of debate files between start_date and end_date from all sources."""
        print("Fetching debate file lists...")
        debate_files = []
        
        # Convert input dates to datetime objects
        start = parser.parse(start_date).date()
        end = parser.parse(end_date).date()
        
        for base_url in self.base_urls:
            try:
                response = requests.get(base_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all links that match the debate file pattern
                links = soup.find_all('a', href=re.compile(r'(?:debates|westminster)\d{4}-\d{2}-\d{2}[a-z]?.xml'))
                print(f"Found {len(links)} total debate files in {base_url}")
                
                for link in links:
                    filename = link['href']
                    # Extract date from filename using either debates or westminster pattern
                    date_match = re.search(r'(?:debates|westminster)(\d{4}-\d{2}-\d{2})', filename)
                    if date_match:
                        file_date = parser.parse(date_match.group(1)).date()
                        if start <= file_date <= end:
                            debate_files.append((base_url, filename))
            except Exception as e:
                print(f"Error whilst accessing {base_url}: {str(e)}")
        
        return sorted(debate_files)

    def analyse_speech(self, speech_tag):
        """Analyse a single speech tag and update speaker statistics."""
        speaker_name = speech_tag.get('speakername', 'Unknown')
        person_id = speech_tag.get('person_id', 'Unknown')
        
        # Update speaker stats
        if speaker_name != 'Unknown':
            self.speakers[speaker_name].person_id = person_id
            self.speakers[speaker_name].total_speeches += 1
            
            # Get all text content from the speech
            text = ' '.join(speech_tag.stripped_strings)
            
            # Split into words and count
            words = re.findall(r'\b\w+\b', text.lower())
            for word in words:
                if len(word) > 1:  # Omit single-letter words
                    self.speakers[speaker_name].word_counts[word] += 1

    def analyse_debate_file(self, base_url: str, filename: str):
        """Analyse a single debate file."""
        url = f"{base_url}{filename}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'xml')
            
            # Find all speech tags
            speeches = soup.find_all('speech')
            print(f"Found {len(speeches)} speeches in {filename}")
            
            for speech in speeches:
                self.analyse_speech(speech)
                
        except Exception as e:
            print(f"Error whilst processing {filename}: {str(e)}")

    def analyse_date_range(self, start_date: str, end_date: str):
        """Analyse all debate files between start_date and end_date."""
        debate_files = self.get_debate_files(start_date, end_date)
        print(f"Found {len(debate_files)} total debate files to analyse")
        
        if not debate_files:
            print("Warning: No debate files found for the specified date range!")
            return
            
        for base_url, filename in tqdm(debate_files, desc="Analysing debate files"):
            self.analyse_debate_file(base_url, filename)
            
        if not self.speakers:
            print("Warning: No speakers found in any of the analysed files!")

    def save_results(self, output_file: str):
        """Save the results to a JSON file."""
        results = {}
        for speaker, stats in self.speakers.items():
            results[speaker] = {
                'person_id': stats.person_id,
                'total_speeches': stats.total_speeches,
                'word_counts': dict(stats.word_counts)
            }
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    parser = DebateParser()
    
    # Hardcoded date range
    start_date = "2024-07-17"
    end_date = "2025-03-06"
    
    print(f"Analysing both main debates and Westminster Hall debates from {start_date} to {end_date}")
    parser.analyse_date_range(start_date, end_date)
    
    if not parser.speakers:
        print("\nNo speakers found. Please check:")
        print("1. The date range is correct and not in the future")
        print("2. The websites are accessible")
        print("3. The XML files contain speech tags")
        return
    
    output_file = "speaker_statistics.json"
    parser.save_results(output_file)
    print(f"\nResults saved to {output_file}")
    
    # Print some basic statistics
    print("\nSummary:")
    print(f"Total number of speakers: {len(parser.speakers)}")
    
    if parser.speakers:
        most_speeches = max(parser.speakers.items(), key=lambda x: x[1].total_speeches)
        print(f"\nSpeaker with most speeches: {most_speeches[0]}")
        print(f"Number of speeches: {most_speeches[1].total_speeches}")

if __name__ == "__main__":
    main() 