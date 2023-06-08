import logging
from mongobot.matchservice import allRanksMessage
import os
import discord
from datetime import datetime
from discord import Webhook
import aiohttp

import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Update rank trigger running')
    async with aiohttp.ClientSession() as session:
        url = os.environ['DISCORD_WEBHOOK']
        webhook = Webhook.from_url(url, session=session)
        message = allRanksMessage()
        
        embed = discord.Embed(
            title='Update ranks', 
            url=os.environ['RANK_URL'],
            description="Click on the link above to update ranks", 
            timestamp=datetime.now()
            )
        
        embed.set_thumbnail(url="https://pokebase.dk/media/icons/badges/gbl/combat_rank_1.png")
        await webhook.send(embed=embed, content=message, username="CSGO Ranks", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")

    logging.info("Time trigger finished")
    return func.HttpResponse(f"Leaderboard updated successfully.")
