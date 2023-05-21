import logging
from pymongo import MongoClient
import os
from mongobot.matchservice import serviceGetPlayers
import aiohttp

import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Test mongo running')
    logging.info('Get dabase')
    uri = os.environ['MONGO_URI']
    
    async with aiohttp.ClientSession() as session:
        players = serviceGetPlayers()
        playerName = players[0]['name']
    return func.HttpResponse(f"Player name: {playerName}", status_code=200)
