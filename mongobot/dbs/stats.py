import logging
from .database import get_database
from .players import getPlayer, getPlayers
from bson.objectid import ObjectId
from datetime import datetime
from calendar import monthrange
dbname = get_database()
collection = dbname["stats"]

# Stats structure: 
example = {
  "_id": "1f5eba1e-e62b-4f15-bab1-b2294274e344",    # ObjectId - Not required
  "steam64Id": 76561198255756814,                   # Int
  "matchId": "1f5eba1e-e62b-4f15-bab1-b2294274e344",# String
  "name": "Long Lick Dewis",                        # String
  "flashbangHitFoe": 18,                            # Int
  "score": 68,                                      # Int
  "hsp": 0.5385,                                    # Decimal 4
  "mvps": 4,                                        # Int
  "totalKills": 26,                                 # Int
  "totalDeaths": 16,                                # Int
  "kdRatio": 1.63,                                  # Decimal 2
  "multi5k": 0,                                     # Int
  "dpr": 112.76,                                    # Decimal 2
  "totalDamage": 2819,                               # Int
  "rank": 6                               # Int
}
def updateStat(stat):
    try:
        collection.update_one({ '_id': stat['_id']}, { '$set': stat})
    except Exception as e:
        print("Failed to execute the above query", e)
     

def insertNewStat(stat):
    try:
        stat['steam64Id'] = int(stat['steam64Id'])
        collection.insert_one(stat)
    except Exception as e:
        print("Failed to execute the above query", e)

def getStat(stat):
    try:
        result = collection.find_one({ '_id': stat['_id']})
        return result
    except Exception as e:
        print("Failed to execute the above query", e)


def getStats():
    try:
        return collection.find()
    except Exception as e:
        print("Failed to execute the above query", e)


def deleteStat(stat):
    try:
        collection.delete_one({ '_id': stat['_id']})
    except Exception as e:
        print("Failed to execute the above query", e)
            

def deleteStats():
    try:
        collection.delete_many({})
    except Exception as e:
        print("Failed to execute the above query", e)

def getStatsByMonth(month):
    try:
        year = datetime.now().year
        monthRange = monthrange(year, month)
        firstDayOfMonth = datetime(year=year, month=month, day=1, hour=0, minute=0, second=0,)
        lastDayOfMonth = datetime(year=year,  month=month, day=monthRange[1], hour=0, minute=0, second=0,)
        firstDayOfMonthId = ObjectId.from_datetime(firstDayOfMonth)
        lastDayOfMonthId = ObjectId.from_datetime(lastDayOfMonth)
        
        stats = []
        for player in getPlayers():
            result = collection.aggregate([
                {
                    '$match' : 
                        {
                            '_id': {'$gt':firstDayOfMonthId, '$lt':lastDayOfMonthId},
                            'steam64Id': player['steam64Id'],
                        }
                },
                {
                    '$group' : 
                        { 
                            '_id': '$steam64Id', 
                            'avgFlashbangHitFoe': { '$avg': '$flashbangHitFoe'} ,
                            'avgHsp': { '$avg': '$hsp'} ,
                            'totalMvps': { '$sum': '$mvps'} ,
                            'avgTotalKills': { '$avg': '$totalKills'} ,
                            'avgTotalDeaths': { '$avg': '$totalDeaths'} ,
                            'avgKdratio': { '$avg': '$kdRatio'} ,
                            'totalAces': { '$sum': '$multi5k'} ,
                            'avgAdr': { '$avg': '$dpr'} ,
                            'totalDamage': { '$sum': '$totalDamage'},
                            'matchesPlayed': { '$count': { } }
                        }
                }
            ])
            if result:
                for stat in result:
                    stat['name'] = player['name']
                    stats.append(stat)
        return stats
    except Exception as e:
        print("Failed to execute the above query", e)

def singlePlayersLast2Matches(steam64Id):
    try:
        player = getPlayer({ 'steam64Id': steam64Id})
        result = collection.find({ 'steam64Id': player['steam64Id']}).sort("_id", -1).limit(2)
        stats = []
        if result:
            for stat in result:
                stats.append({
                    "name": player['name'],
                    "steam64Id": stat['steam64Id'],
                    "rank": stat['rank']
                }) 
        return stats
    except Exception as e:
        print("Failed to execute the above query", e)