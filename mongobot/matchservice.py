import time
import logging
from .csgostats.steam import find_matches
from .csgostats.leetify import get_matches
from .csgostats.matchmapper import clean_match_details, map_leaderboard, convertToStringRank
from .dbs.players import updatePlayer, getPlayerIds, getPlayers
from .dbs.matches import insertNewMatch, getCodes
from .dbs.stats import insertNewStat, getStatsByMonth, singlePlayersLast2Matches
from datetime import datetime
from tabulate import tabulate

# 2
def find_friends_from_matches(matches):
    friends = getPlayerIds()
    new_matches = []
    for match in matches:
        new_matches.append(clean_match_details(friends, match))
    return new_matches

# 1
def get_last_match_details():
    new_match_codes = []
    new_match_details = []
    old_match_codes = getCodes()
    for friend in getPlayers():
        if friend['authCode'] == '':
            continue
        newest_code = 'n/a'
        result = find_matches(friend)
        # Finds new match codes not analyzed
        if result is not None:
            for code in result:
                if code not in old_match_codes and code not in new_match_codes:
                    newest_code = code
                    new_match_codes.append(code)
                else:
                    pass
                
        # If any, analyze new matches
        if new_match_codes:
            matches = get_matches(friend['steam64Id'], new_match_codes)
            for match in find_friends_from_matches(matches):
                new_match_details.append(match)
                        
        # Sets latest knownCode for player
        if newest_code != 'n/a':
            friend['knownCode'] = newest_code
            updatePlayer(friend)
        time.sleep(1)
        
    return new_match_details

# 3
def update_leaderboard(matches):
    for match in matches:
        insertNewMatch(match)
        for player in match['players']:
            insertNewStat(player)

# 4
def get_leaderboards_this_month():
    currentMonth = datetime.now().month
    leaderboard = getStatsByMonth(currentMonth)
    leaderboard = map_leaderboard(leaderboard)
    return leaderboard

def start():
    logging.info('Get matches started')
    new_matches = get_last_match_details()
    if not new_matches:
        return
    update_leaderboard(new_matches)
    leaderboard = get_leaderboards_this_month()
    return leaderboard

def generateLeaderboard():
    leaderboard = get_leaderboards_this_month()
    return leaderboard

def findAnyDeranked():
    playerIds = getPlayerIds()
    deranks = []
    for id in playerIds:
        ranksLast2Matches = singlePlayersLast2Matches(id)
        if ranksLast2Matches:
            newest = ranksLast2Matches[0]
            oldest = ranksLast2Matches[1]
            if newest['rank'] < oldest['rank']:
                newRank = convertToStringRank(newest['rank'])
                oldRank = convertToStringRank(oldest['rank'])
                deranks.append({'name': newest['name'],  'oldRank': oldRank, 'newRank': newRank})
    return deranks

def findAnyRankedUp():
    playerIds = getPlayerIds()
    rankups = []
    for id in playerIds:
        ranksLast2Matches = singlePlayersLast2Matches(id)
        if ranksLast2Matches:
            newest = ranksLast2Matches[0]
            oldest = ranksLast2Matches[1]
            if newest['rank'] > oldest['rank']:
                newRank = convertToStringRank(newest['rank'])
                oldRank = convertToStringRank(oldest['rank'])
                rankups.append({'name': newest['name'], 'oldRank': oldRank, 'newRank': newRank})
    return rankups

def findAllCurrentRanks():
    playerIds = getPlayerIds()
    ranks = []
    for id in playerIds:
        ranksLast2Matches = singlePlayersLast2Matches(id)
        if ranksLast2Matches:
            player = ranksLast2Matches[0]
            player['rank'] = convertToStringRank(player['rank'])
            ranks.append({'name': player['name'], 'rank': player['rank']})
    return ranks


def allRanksMessage():
    ranks = findAllCurrentRanks()
    if not ranks:
        return
    message = '```\n'
    table = [ranks[0].keys()]
    for rank in ranks:
        table.append(rank.values())
    message += tabulate(table, headers='firstrow')
        
    message += f'\n\nLast updated: {datetime.now().date()} {datetime.now().time()}```'
    return message

def generateDerankMessage():
    deranks = findAnyDeranked()
    if not deranks:
        return
    message = '```\n'
    table = [deranks[0].keys()]
    message += f'Deranked:'
    for deranked in deranks:
        table.append(deranked.values())
    message += tabulate(table, headers='firstrow')
        
    message += f'\n\nLast updated: {datetime.now().date()} {datetime.now().time()}```'
    return message

def generateRankupMessage():
    rankedups = findAnyRankedUp()
    if not rankedups:
        return
    message = '```\n'
    table = [rankedups[0].keys()]
    message += f'Ranked up:'
    for rankedup in rankedups:
        table.append(rankedup.values())
    message += tabulate(table, headers='firstrow')
        
    message += f'\n\nLast updated: {datetime.now().date()} {datetime.now().time()}```'
    return message


def generateLeaderboardMessage(leaderboard):
    table = [leaderboard[0].keys()]
    for player in leaderboard:
        table.append(player.values())
    
    message = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
    return f"""
```
{message}
```
"""