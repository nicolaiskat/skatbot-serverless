# leetify.py
import os
import logging
import base64
import requests
import json

PASSWORD = base64.b64decode(os.environ['LEETIFY_PASSWORD']).decode('utf-8')

jwt = ''

root_url = 'https://api.leetify.com/api'

def login_leetify():
    global jwt
    url = root_url + '/login'
    credentials = { 'email': 'jegerrockstar@gmail.com', 'password': PASSWORD }
    result = requests.post(url, json = credentials)
    jwt = result.json()['token']
    
def get_general_data():
    url = root_url + '/general-data'
    headers = { 'Authorization': 'Bearer ' + jwt }
    result = requests.get(url, timeout = 30, headers = headers)
    if (result.status_code == 401) or (result.status_code == 403):
        login_leetify()
        return get_general_data()
    if 200 <= result.status_code and result.status_code <= 299:
        return result.text
  
def get_player_profile(steamId64):
    url = root_url + f'/mini-profiles/{steamId64}'
    headers = { 'Authorization': 'Bearer ' + jwt }
    result = requests.get(url, timeout = 30, headers = headers)
    if (result.status_code == 401) or (result.status_code == 403):
        login_leetify()
        return get_player_profile()
    if 200 <= result.status_code and result.status_code <= 299:
        return result.text
      
def get_matches(steamId64, codes):
    login_leetify()
    match_list = []
    recent_matches = json.loads(get_player_profile(steamId64))['recentMatches']
    for match in recent_matches:    
        latest_match_id = match['id']
        url = root_url + f'/games/{latest_match_id}'
        headers = { 'Authorization': 'Bearer ' + jwt }
        result = requests.get(url, timeout = 30, headers = headers)
        if (result.status_code == 401) or (result.status_code == 403):
            login_leetify()
            return get_matches(steamId64, codes)
        if 200 <= result.status_code and result.status_code <= 299:
            result = json.loads(result.text)
            if result["steamShareCode"] in codes:
                match_list.append(result)
    return match_list

      
def get_matches_by_ids(matchIds):
    login_leetify()
    match_list = []
    for matchId in matchIds:    
        url = root_url + f'/games/{matchId}'
        headers = { 'Authorization': 'Bearer ' + jwt }
        result = requests.get(url, timeout = 30, headers = headers)
        status = result.status_code
        if (status == 401) or (status == 403):
            login_leetify()
            return get_matches_by_ids(matchIds)
        if 200 <= status and status <= 299:
            result = json.loads(result.text)
            match_list.append(result)
    return match_list