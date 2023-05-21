import logging

ranks = {
    1: 'Silver 1',
    2: 'Silver 2', 
    3: 'Silver 3', 
    4: 'Silver 4', 
    5: 'Silver Elite', 
    6: 'Silver Elite Master', 
    7: 'Gold Nova 1', 
    8: 'Gold Nova 2', 
    9: 'Gold Nova 3', 
    10: 'Gold Nova Master', 
    11: 'Master Guardian 1', 
    12: 'Master Guardian 2',
    13: 'Master Guardian Elite',
    14: 'Distiguished Master Guardian',
    15: 'Legendary Eagle',
    16: 'Legendary Eagle Master',
    17: 'Supreme Master First Class',
    18: 'Global Elite'
}

def isRankedUp(data):
    currentRank = data['matchmakingGameStats']['rank'] # int
    oldRank = data['matchmakingGameStats']['oldRank'] # int
    rankChanged = data['matchmakingGameStats']['rankChanged'] # boolean
    if rankChanged and oldRank < currentRank:
        return True
    return False

def isRankedDown(data):
    currentRank = data['matchmakingGameStats']['rank'] # int
    oldRank = data['matchmakingGameStats']['oldRank'] # int
    rankChanged = data['matchmakingGameStats']['rankChanged'] # boolean
    if rankChanged and oldRank > currentRank:
        return True
    return False

def convertToStringRank(rank):
    return ranks[rank]

def clean_match_details(friends, data):
    # Match Details
    match = {}
    match['matchId'] = data['id'] # string
    match['gamemode'] = data['dataSource'] # string
    match['mapName'] = data['mapName'] # string
    match['code'] = data['steamShareCode'] # string
    match['gameFinishedAt'] = data['details']['gameFinishedAt'] # timestamp

    # Player.Stats
    players = []
    for player in data['playerStats']:
        friend = {}
        if (int(player['steam64Id']) in friends or str(player['steam64Id']) in friends):
            friend['matchId'] = data['id'] # string
            friend['steam64Id'] = player['steam64Id'] # int
            friend['name'] = player['name'] # string
            friend['flashbangHitFoe'] = player['flashbangHitFoe'] # int
            friend['score'] = player['score'] # int
            friend['hsp'] = player['hsp'] # decimal 4
            friend['mvps'] = player['mvps'] # int
            friend['totalKills'] = player['totalKills'] # int
            friend['totalDeaths'] = player['totalDeaths'] # int
            friend['kdRatio'] = player['kdRatio'] # decimal 2
            friend['multi5k'] = player['multi5k'] # int
            friend['dpr'] = player['dpr'] # decimal 2
            friend['totalDamage'] = player['totalDamage'] # int

            for player in data['matchmakingGameStats']:
                if (int(player['steam64Id']) in friends or str(player['steam64Id']) in friends):
                    if friend['steam64Id'] == player['steam64Id']:
                        friend['rank'] = player['rank'] # int
            players.append(friend)
    
    match['players'] = players
    return match

def map_leaderboard(leaderboard):
    result = []
    for player in leaderboard:
        result.append({
            "Name": player["name"],
            "Kills": round(player["avgTotalKills"]),
            "K/D": round(player["avgKdratio"], 2),
            "#Aces": player["totalAces"],
            "ADR": round(player["avgAdr"]),
            "#DMG": player["totalDamage"],
            "HS": str(round(player["avgHsp"] * 100)) + "%",
            "EFs": round(player["avgFlashbangHitFoe"]),
            "#MVPs": player["totalMvps"],
            "#Matches": player["matchesPlayed"],
        })
    return result