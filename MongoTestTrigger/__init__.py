import logging
from pymongo import MongoClient
import os

import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Test mongo running')
    logging.info('Get dabase')
    uri = os.environ['MONGO_URI']
    client = MongoClient(uri)
    dbname = client[os.environ['CSGOSTATS_DATABASE']]
    collection = dbname["players"]
    players = []
    try:
        result = collection.find()
        players = []
        for player in result:
            players.append(player)
    except Exception as e:
        print("Failed to execute the above query", e)
    playerName = players[0]['name']
    return func.HttpResponse(f"Player name: {playerName}", status_code=200)
