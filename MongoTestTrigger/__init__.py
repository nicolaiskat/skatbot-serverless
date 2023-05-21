import logging
from pymongo import MongoClient
import os
from mongobot.dbs.players import getPlayers

import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Test mongo running')
    logging.info('Get dabase')
    uri = os.environ['MONGO_URI']
    client = MongoClient(uri)
    dbname = client[os.environ['CSGOSTATS_DATABASE']]
    collection = dbname["players"]
    players = getPlayers()
    playerName = players[0]['name']
    return func.HttpResponse(f"Player name: {playerName}", status_code=200)
