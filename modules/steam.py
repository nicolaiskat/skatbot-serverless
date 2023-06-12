# sharingcode.py
import os
import logging
import base64
import requests
import time

API_KEY = base64.b64decode(os.environ['STEAM_API_KEY']).decode('utf-8')

def find_matches(player):
    new_known_codes = []
    result = 'invalid-code'
    while (result != 'n/a'):
        time.sleep(1)
        url = f"https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={API_KEY}&steamid={player['steam64Id']}&steamidkey={player['authCode']}&knowncode={player['knownCode']}"
        response = requests.get(url)
        logging.info(response)
        if (response.status_code == 403):
            return new_known_codes
        if (response.status_code == 412):
            return new_known_codes
        if (response.status_code == 202):
            return new_known_codes
        result = response.json()['result']['nextcode']
        if result == 'n/a':
            return new_known_codes
        new_known_codes.append(result)
        player['knownCode'] = result
    return new_known_codes
