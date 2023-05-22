import logging
import os
from mongobot import serviceGetPlayers

import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Test mongo running')
    logging.info('Get dabase')
    uri = os.environ['MONGO_URI']
    
    players = serviceGetPlayers()
    playerName = players[0]['name']
    return func.HttpResponse(f"Player name: {playerName}", status_code=200)
