# sharingcode.py
import os
import logging
import base64
import requests
import time
from dotenv import load_dotenv
load_dotenv()

API_KEY = base64.b64decode(os.environ['STEAM_API_KEY']).decode('utf-8')

def find_matches(player):
    global new_known_codes
    new_known_codes = []
    def reset():
        global new_known_codes
        new_known_codes = []
        
    def new_match_found(player):
        global new_known_codes
        url = f"https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={API_KEY}&steamid={player['steam64Id']}&steamidkey={player['authCode']}&knowncode={player['knownCode']}"
        response = requests.get(url)
        result = response.json()['result']['nextcode']
        if (result != 'n/a'):
            player['knownCode'] = result
            new_known_codes.append(result)
            time.sleep(1)
            result = new_match_found(player)
        return new_known_codes 
    
    reset()
    return new_match_found(player)