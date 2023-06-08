import logging
import os
from modules.matchservice import serviceGetPlayers
from tabulate import tabulate
import time
import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Test mongo running')
    
    players = serviceGetPlayers()
    playerName = players[0]['name']
    return func.HttpResponse(f"Player name: {playerName}", status_code=200)
