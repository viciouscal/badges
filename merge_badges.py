
import json
import requests
from typing import Dict, Set
import sys

PROTECTED_IDS = {
    "1097168432300036177",
    "1041671062586400829", 
    "765440721137303563"
}

YOUR_REPO_FILE = "badges.json"
ORIGINAL_URL = "https://badges.vencord.dev/badges.json"

def load_local_file(filepath: str) -> Dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def download_original(url: str) -> Dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def smart_merge(your_data: Dict, original_data: Dict, protected_ids: Set[str]) -> Dict:
    merged = {}
    
    for user_id in protected_ids:
        if user_id in your_data:
            merged[user_id] = your_data[user_id]
    
    for user_id, badges in original_data.items():
        if user_id not in protected_ids:
            merged[user_id] = badges
    
    for user_id, badges in your_data.items():
        if user_id not in protected_ids and user_id not in original_data:
            merged[user_id] = badges
    
    return merged

def save_file(data: Dict, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

def main():
    your_data = load_local_file(YOUR_REPO_FILE)
    original_data = download_original(ORIGINAL_URL)
    merged_data = smart_merge(your_data, original_data, PROTECTED_IDS)
    save_file(merged_data, YOUR_REPO_FILE)
    print("Done")

if __name__ == "__main__":
    main()
