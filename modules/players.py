import logging
from .database import get_database
import base64

dbname = get_database()
collection = dbname["players"]

# Players structure: 
example = {
    '_id': 76561198255756814,                           # INT
    'steam64Id': 76561198255756814,                     # INT
    'name': 'Skat',                                     # STRING
    'knownCode': 'CSGO-dM64E-AxM96-9eGsZ-NewxY-XZrKG',  # STRING
    'authCode': 'NzMzSC0zTVhIMy02VFpB',                 # STRING
}

def insertNewPlayer(player):
    try:
        player['_id'] = player['steam64Id']
        collection.insert_one(player)
    except Exception as e:
        print("Failed to execute the above query", e)

def deletePlayers():
    try:
        collection.delete_many({})
    except Exception as e:
        print("Failed to execute the above query", e)
        
def deletePlayer(player):
    try:
        collection.delete_one({ '_id': player['steam64Id']})
    except Exception as e:
        print("Failed to execute the above query", e)

def getPlayer(player):
    try:
        result = collection.find_one({ '_id': player['steam64Id']})
        result['authCode'] = base64.b64decode(result['authCode']).decode('utf-8')
        return result
    except Exception as e:
        print("Failed to execute the above query", e)

def getPlayers():
    try:
        result = collection.find()
        players = []
        for player in result:
            player['authCode'] = base64.b64decode(player['authCode']).decode('utf-8')
            players.append(player)
        return players
    except Exception as e:
        print("Failed to execute the above query", e)

def getPlayerIds():    
    try:
        result = collection.find()
        steam64Ids = []
        for player in result:
            steam64Ids.append(player['steam64Id'])
        return steam64Ids
    except Exception as e:
        print("Failed to execute the above query", e)

def updatePlayer(player):
    try:
        player['authCode'] = base64.b64encode(player['authCode'].encode("ascii")).decode('ascii')
        collection.update_one({ '_id': player['steam64Id']}, { '$set': player})
    except Exception as e:
        print("Failed to execute the above query", e)
        
        
# Missing:
# updatePlayer(hoj)
# updatePlayer(g)
