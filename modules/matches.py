import logging
from .database import get_database

dbname = get_database()
collection = dbname["matches"]

# Matches structure: 
example = {
    "_id": "1f5eba1e-e62b-4f15-bab1-b2294274e344",  # String
    "matchId": "1f5eba1e-e62b-4f15-bab1-b2294274e344",  # String
    "gamemode": "matchmaking",                          # String
    "mapName": "de_overpass",                           # String
    "code": "CSGO-dM64E-AxM96-9eGsZ-NewxY-XZrKG",       # String
    "gameFinishedAt": "2023-05-04T20:38:35.000Z",       # Timestamp
}

def insertNewMatch(match):
    try:
        match['_id'] = match['matchId']
        collection.insert_one(match)
    except Exception as e:
        print("Failed to execute the above query", e)
           
def deleteMatch(match):
    try:
        collection.delete_one({ '_id': match['matchId']})
    except Exception as e:
        print("Failed to execute the above query", e)
    
def deleteMatches():
    try:
        collection.delete_many({})
    except Exception as e:
        print("Failed to execute the above query", e)

def getMatch(match):
    try:
        result = collection.find_one({ '_id': match['matchId']})
        return result
    except Exception as e:
        print("Failed to execute the above query", e)
           
def getMatches():
    try:
        return collection.find()
    except Exception as e:
        print("Failed to execute the above query", e)
         
def getCodes():
    matches = getMatches()
    codes = []
    for match in matches:
        codes.append(match['code'])
    return codes

def getMatchIds():
    matches = getMatches()
    matchIds = []
    for match in matches:
        matchIds.append(match['matchId'])
    return matchIds

""" insertNewMatch({
  "matchId": "3540cb1a-18e2-4530-9608-9699f2421d2e",
  "gamemode": "matchmaking",
  "code": "CSGO-dM64E-AxM96-9eGsZ-NewxY-XZrKG",
  "mapName": "de_vertigo",
  "gameFinishedAt": "2023-04-30T13:16:44.000Z",
  "players": [
    {
      "matchId": "3540cb1a-18e2-4530-9608-9699f2421d2e",
      "steam64Id": "76561198255756814",
      "name": "Long Lick Dewis",
      "flashbangHitFoe": 11,
      "score": 32,
      "hsp": 0.6923,
      "mvps": 0,
      "totalKills": 13,
      "totalDeaths": 24,
      "kdRatio": 0.54,
      "multi5k": 0,
      "dpr": 52.52,
      "totalDamage": 1523
    },
    {
      "matchId": "3540cb1a-18e2-4530-9608-9699f2421d2e",
      "steam64Id": "76561198036739830",
      "name": "NicoPepe",
      "flashbangHitFoe": 12,
      "score": 36,
      "hsp": 0.5833,
      "mvps": 1,
      "totalKills": 12,
      "totalDeaths": 26,
      "kdRatio": 0.46,
      "multi5k": 0,
      "dpr": 56.52,
      "totalDamage": 1639
    }
  ]
}) """