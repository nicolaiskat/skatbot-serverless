import logging
from modules.matchservice import start, generateLeaderboardMessage, get_leaderboards_this_month, generateDerankMessage, generateRankupMessage
import os
import discord
from datetime import datetime
from discord import Webhook
import aiohttp

import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Update matches trigger running')
    async with aiohttp.ClientSession() as session:
        url = os.environ['DISCORD_WEBHOOK']
        webhook = Webhook.from_url(url, session=session)
        result = start()
        if result == None:
            logging.info("Result is none")
            return
        
        embed = discord.Embed(
            title='Update leaderboard', 
            url=os.environ['LEADERBOARD_URL'],
            description="Click on the link above to update leaderboard", 
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="https://images.freeimages.com/fic/images/icons/2799/flat_icons/256/trophy.png")
        await webhook.send(embed=embed, username="CSGO Leaderboard", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")
        
        message = generateLeaderboardMessage(result)
        await webhook.send(content=message, username="CSGO Leaderboard", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")
        
    return func.HttpResponse(f"Updated matches successfully.")
